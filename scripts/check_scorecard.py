#!/usr/bin/env python3
"""Check that a Hill Causation scorecard is complete.

This script checks COMPLETENESS ONLY. It verifies that a scorecard file
lists all 9 Bradford Hill viewpoints, each with a verdict of
Pass / Weak / Fail / Unknown, one line of evidence, and a source, and
that Temporality is filled in.

It does NOT judge whether the evidence is medically correct, whether
the verdict tier is right, or whether the claim is truly causal.
That judgement is the human's job (see SKILL.md).

Usage:
    python scripts/check_scorecard.py FILE [FILE ...]
    python scripts/check_scorecard.py --format json FILE

Exit code 0: every file is complete.
Exit code 1: at least one file is incomplete, or a file cannot be read.
Exit code 2: usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

VALID_VERDICTS = ("Pass", "Weak", "Fail", "Unknown")

# (display name, keywords that identify the viewpoint in a row/heading)
CRITERIA = [
    ("Strength", ("strength",)),
    ("Consistency", ("consistency",)),
    ("Specificity", ("specificity",)),
    ("Temporality", ("temporality",)),
    ("Biological gradient", ("biological gradient", "dose-response", "dose response")),
    ("Plausibility", ("plausibility",)),
    ("Coherence", ("coherence",)),
    ("Experiment", ("experiment",)),
    ("Analogy", ("analogy",)),
]

PLACEHOLDER_TOKENS = ("todo", "tbd", "lorem", "xxx", "[insert", "[fill")


def _is_placeholder(text: str) -> bool:
    lowered = text.strip().lower()
    if not lowered or lowered in ("-", "--", "—", "n/a", "na", "none"):
        return True
    return any(token in lowered for token in PLACEHOLDER_TOKENS)


def _split_table_row(line: str) -> list[str]:
    """Split a Markdown table row into cells, ignoring leading/trailing pipes."""
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def _find_verdict(text: str) -> str | None:
    """Return the verdict token in text, or None if there is none / more than one."""
    found = []
    for verdict in VALID_VERDICTS:
        if re.search(rf"\b{re.escape(verdict)}\b", text, re.IGNORECASE):
            found.append(verdict)
    if len(found) == 1:
        return found[0]
    return None


@dataclass
class CriterionResult:
    name: str
    present: bool = False
    verdict: str | None = None
    evidence: str = ""
    source: str = ""
    errors: list[str] = field(default_factory=list)


@dataclass
class CheckResult:
    path: str
    complete: bool
    results: list[CriterionResult] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "complete": self.complete,
            "errors": self.errors,
            "criteria": [
                {
                    "name": r.name,
                    "present": r.present,
                    "verdict": r.verdict,
                    "errors": r.errors,
                }
                for r in self.results
            ],
        }


def _check_table_rows(lines: list[str]) -> dict[str, CriterionResult]:
    """Parse Markdown table rows; return results keyed by criterion name."""
    found: dict[str, CriterionResult] = {}
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = _split_table_row(stripped)
        if len(cells) < 4:
            continue
        first = cells[0].lower()
        # Skip the header row and the separator row.
        if "viewpoint" in first or "criterion" in first:
            continue
        if set(stripped.replace("|", "").replace("-", "").strip()) == set():
            continue
        for name, keywords in CRITERIA:
            if name in found:
                continue
            # The criterion name usually sits in column 1 (after an optional # column).
            haystack = " ".join(cells[:2]).lower()
            if any(kw in haystack for kw in keywords):
                result = CriterionResult(name=name, present=True)
                # Columns: [#, Viewpoint, Verdict, Evidence, Source]
                # or: [Viewpoint, Verdict, Evidence, Source]
                if len(cells) >= 5 and cells[0].strip().isdigit():
                    verdict_cell, evidence, source = cells[2], cells[3], cells[4]
                elif len(cells) >= 4:
                    verdict_cell, evidence, source = cells[1], cells[2], cells[3]
                else:
                    verdict_cell, evidence, source = "", "", ""
                result.verdict = _find_verdict(verdict_cell)
                result.evidence = evidence.strip()
                result.source = source.strip()
                found[name] = result
                break
    return found


def _check_sections(text: str) -> dict[str, CriterionResult]:
    """Fallback: parse `## <criterion>` sections with Verdict/Evidence/Source lines."""
    found: dict[str, CriterionResult] = {}
    # Split on level-2/3 headings.
    parts = re.split(r"(?m)^#{2,3}\s+(.+)$", text)
    # parts: [preamble, heading1, body1, heading2, body2, ...]
    for i in range(1, len(parts) - 1, 2):
        heading = parts[i].strip().lower()
        body = parts[i + 1]
        for name, keywords in CRITERIA:
            if name in found:
                continue
            if any(kw in heading for kw in keywords):
                result = CriterionResult(name=name, present=True)
                verdict_match = re.search(
                    r"^[ \t]*verdict[ \t]*:[ \t]*([^\r\n]*)",
                    body, re.IGNORECASE | re.MULTILINE,
                )
                evidence_match = re.search(
                    r"^[ \t]*evidence[ \t]*:[ \t]*([^\r\n]*)",
                    body, re.IGNORECASE | re.MULTILINE,
                )
                source_match = re.search(
                    r"^[ \t]*source[ \t]*:[ \t]*([^\r\n]*)",
                    body, re.IGNORECASE | re.MULTILINE,
                )
                if verdict_match:
                    result.verdict = _find_verdict(verdict_match.group(1))
                if evidence_match:
                    result.evidence = evidence_match.group(1).strip()
                if source_match:
                    result.source = source_match.group(1).strip()
                found[name] = result
                break
    return found


def check_scorecard(path: str | Path) -> CheckResult:
    """Check one scorecard file for completeness."""
    path = Path(path)
    result = CheckResult(path=str(path), complete=False)
    if not path.is_file():
        result.errors.append(f"File not found: {path}")
        return result
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        result.errors.append(f"Cannot read file: {exc}")
        return result

    lines = text.splitlines()
    found = _check_table_rows(lines)
    if len(found) < len(CRITERIA):
        section_found = _check_sections(text)
        for name, entry in section_found.items():
            found.setdefault(name, entry)

    for name, _keywords in CRITERIA:
        entry = found.get(name)
        if entry is None:
            entry = CriterionResult(name=name, present=False)
            entry.errors.append(f"Missing criterion: {name}")
            result.results.append(entry)
            continue
        result.results.append(entry)
        if entry.verdict is None:
            entry.errors.append(
                f"{name}: verdict must be one of Pass / Weak / Fail / Unknown"
            )
        if len(entry.evidence) < 10 or _is_placeholder(entry.evidence):
            entry.errors.append(
                f"{name}: evidence is missing or too short (write one line of evidence)"
            )
        if len(entry.source) < 5 or _is_placeholder(entry.source):
            entry.errors.append(
                f"{name}: source is missing (cite the study or source for this row)"
            )
        if name == "Temporality" and (
            entry.verdict is None or not entry.evidence or _is_placeholder(entry.evidence)
        ):
            entry.errors.append(
                "Temporality: must be filled in — it is the only absolute viewpoint"
            )

    all_errors = [err for entry in result.results for err in entry.errors]
    result.errors.extend(all_errors)
    result.complete = not all_errors
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check Hill Causation scorecard(s) for completeness."
    )
    parser.add_argument("files", nargs="+", help="Scorecard Markdown file(s) to check")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format (default: text)",
    )
    args = parser.parse_args(argv)
    if not args.files:
        parser.error("at least one file is required")

    results = [check_scorecard(path) for path in args.files]
    if args.format == "json":
        print(json.dumps([r.to_dict() for r in results], indent=2))
    else:
        for result in results:
            status = "COMPLETE" if result.complete else "INCOMPLETE"
            print(f"{result.path}: {status}")
            for entry in result.results:
                mark = "ok" if not entry.errors else "MISSING/INVALID"
                verdict = entry.verdict or "-"
                print(f"  [{mark}] {entry.name}: {verdict}")
            for error in result.errors:
                print(f"  - {error}")
    return 0 if all(r.complete for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())

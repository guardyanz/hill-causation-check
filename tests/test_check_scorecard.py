"""Tests for scripts/check_scorecard.py.

The checker verifies COMPLETENESS ONLY: all 9 Bradford Hill viewpoints
present, each with a verdict (Pass / Weak / Fail / Unknown), one line
of evidence, and a source, with Temporality filled in. It does not
judge medical correctness.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from check_scorecard import check_scorecard, main

ROOT = Path(__file__).resolve().parents[1]

CRITERIA = [
    "Strength",
    "Consistency",
    "Specificity",
    "Temporality",
    "Biological gradient (dose-response)",
    "Plausibility",
    "Coherence",
    "Experiment",
    "Analogy",
]


def build_scorecard(verdicts=None, evidence="Effect was measured in the cited study population.", source="Hill (1965)"):
    """Build a minimal valid table scorecard; verdicts maps criterion -> verdict."""
    verdicts = verdicts or {}
    lines = [
        "# Hill Causation Scorecard",
        "",
        "| # | Viewpoint | Verdict | Evidence (one line) | Source |",
        "|---|---|---|---|---|",
    ]
    for i, name in enumerate(CRITERIA, start=1):
        verdict = verdicts.get(name, "Pass")
        lines.append(f"| {i} | {name} | {verdict} | {evidence} | {source} |")
    return "\n".join(lines) + "\n"


def write_scorecard(tmp_path, text, name="scorecard.md"):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def test_complete_scorecard_passes(tmp_path):
    path = write_scorecard(tmp_path, build_scorecard())
    result = check_scorecard(path)
    assert result.complete is True
    assert result.errors == []
    assert len(result.results) == 9
    assert all(r.verdict == "Pass" for r in result.results)


def test_one_criterion_missing_fails(tmp_path):
    text = build_scorecard()
    # Remove the Analogy row entirely.
    text = "\n".join(line for line in text.splitlines() if "Analogy" not in line) + "\n"
    path = write_scorecard(tmp_path, text)
    result = check_scorecard(path)
    assert result.complete is False
    assert any("Analogy" in e for e in result.errors)


def test_unknown_verdict_token_fails(tmp_path):
    path = write_scorecard(tmp_path, build_scorecard({"Strength": "Maybe"}))
    result = check_scorecard(path)
    assert result.complete is False
    assert any("Strength" in e and "verdict" in e for e in result.errors)


def test_empty_temporality_fails(tmp_path):
    text = build_scorecard({"Temporality": "Unknown"}, evidence="Effect was measured.")
    # Blank out the Temporality evidence cell.
    lines = []
    for line in text.splitlines():
        if "Temporality" in line:
            line = "| 4 | Temporality | Unknown |  | Hill (1965) |"
        lines.append(line)
    path = write_scorecard(tmp_path, "\n".join(lines) + "\n")
    result = check_scorecard(path)
    assert result.complete is False
    assert any("Temporality" in e for e in result.errors)


def test_missing_source_fails(tmp_path):
    text = build_scorecard()
    lines = []
    for line in text.splitlines():
        if "Plausibility" in line:
            line = "| 6 | Plausibility | Pass | A mechanism is described in the study. |  |"
        lines.append(line)
    path = write_scorecard(tmp_path, "\n".join(lines) + "\n")
    result = check_scorecard(path)
    assert result.complete is False
    assert any("Plausibility" in e and "source" in e for e in result.errors)


def test_missing_evidence_fails(tmp_path):
    text = build_scorecard()
    lines = []
    for line in text.splitlines():
        if "Coherence" in line:
            line = "| 7 | Coherence | Pass |  | Hill (1965) |"
        lines.append(line)
    path = write_scorecard(tmp_path, "\n".join(lines) + "\n")
    result = check_scorecard(path)
    assert result.complete is False
    assert any("Coherence" in e and "evidence" in e for e in result.errors)


def test_missing_file_fails(tmp_path):
    result = check_scorecard(tmp_path / "does-not-exist.md")
    assert result.complete is False
    assert any("not found" in e.lower() for e in result.errors)


def test_weak_and_fail_verdicts_are_valid(tmp_path):
    # Weak / Fail / Unknown are legitimate scores; completeness still passes.
    verdicts = {
        "Strength": "Weak",
        "Consistency": "Fail",
        "Specificity": "Unknown",
    }
    path = write_scorecard(tmp_path, build_scorecard(verdicts))
    result = check_scorecard(path)
    assert result.complete is True


def test_example_smoking_scorecard_passes():
    result = check_scorecard(ROOT / "examples" / "smoking-lung-cancer.md")
    assert result.complete is True, result.errors


def test_example_rr_1_3_scorecard_passes():
    result = check_scorecard(ROOT / "examples" / "observational-rr-1-3.md")
    assert result.complete is True, result.errors


def test_example_empty_scorecard_fails():
    result = check_scorecard(ROOT / "examples" / "empty-scorecard.md")
    assert result.complete is False
    assert len(result.errors) > 0


def test_template_scorecard_fails_until_filled():
    # The shipped template has no evidence/sources, so it must fail.
    result = check_scorecard(ROOT / "templates" / "scorecard.md")
    assert result.complete is False


def test_cli_exit_zero_on_complete(tmp_path):
    path = write_scorecard(tmp_path, build_scorecard())
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_scorecard.py"), str(path)],
        capture_output=True, text=True, check=False,
    )
    assert proc.returncode == 0
    assert "COMPLETE" in proc.stdout


def test_cli_exit_one_on_incomplete(tmp_path):
    text = build_scorecard()
    text = "\n".join(line for line in text.splitlines() if "Analogy" not in line) + "\n"
    path = write_scorecard(tmp_path, text)
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_scorecard.py"), str(path)],
        capture_output=True, text=True, check=False,
    )
    assert proc.returncode == 1
    assert "INCOMPLETE" in proc.stdout


def test_cli_json_format(tmp_path):
    path = write_scorecard(tmp_path, build_scorecard())
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_scorecard.py"),
         "--format", "json", str(path)],
        capture_output=True, text=True, check=False,
    )
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert data[0]["complete"] is True
    assert len(data[0]["criteria"]) == 9


def test_main_returns_zero_and_one(tmp_path):
    good = write_scorecard(tmp_path, build_scorecard(), "good.md")
    assert main([str(good)]) == 0
    bad_text = "\n".join(
        line for line in build_scorecard().splitlines() if "Analogy" not in line
    ) + "\n"
    bad = write_scorecard(tmp_path, bad_text, "bad.md")
    assert main([str(bad)]) == 1


@pytest.mark.parametrize("blank_field", [None, "Verdict", "Evidence", "Source"])
def test_section_fields_cannot_borrow_the_next_line(tmp_path, blank_field):
    sections = []
    for name in CRITERIA:
        fields = {
            "Verdict": "Pass",
            "Evidence": "Effect was measured in the cited study population.",
            "Source": "Hill (1965)",
        }
        if name == "Strength" and blank_field is not None:
            fields[blank_field] = ""
        body = "\n".join(f"{field}: {value}" for field, value in fields.items())
        sections.append(f"## {name}\n{body}\nNotes: Pass reported in the study.\n")
    path = write_scorecard(tmp_path, "\n".join(sections))
    result = check_scorecard(path)
    if blank_field is None:
        assert result.complete is True, result.errors
    else:
        assert result.complete is False
        assert any("Strength" in error and blank_field.lower() in error for error in result.errors)


def test_invalid_utf8_is_reported_as_unreadable(tmp_path):
    path = tmp_path / "invalid.md"
    path.write_bytes(b"\xff\xfe\x00")
    result = check_scorecard(path)
    assert result.complete is False
    assert any("Cannot read file" in error for error in result.errors)


def test_cli_invalid_utf8_returns_json_error(tmp_path, capsys):
    path = tmp_path / "invalid.md"
    path.write_bytes(b"\xff\xfe\x00")
    assert main(["--format", "json", str(path)]) == 1
    data = json.loads(capsys.readouterr().out)
    assert data[0]["complete"] is False
    assert data[0]["errors"]

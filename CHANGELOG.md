# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] - 2026-11-06

### Fixed

- Section-format scorecards no longer borrow the next line when an evidence or source field is blank.
- Unreadable UTF-8 input returns an incomplete result and exit code 1 instead of a traceback.
- Claude plugin discovery now points to the skill directory; a marketplace catalog and the install command are included.

### Added

- `SKILL.md`: Agent Skill for assessing whether X causes Y with the 9 Bradford Hill viewpoints (1965), including the 5-step mechanism (claim with numbers and design; Temporality gate; per-viewpoint scoring; verdict tiers STRONG / PLAUSIBLE / WEAK ASSOCIATION / NOT ESTABLISHED; "what would change this verdict"), and two worked examples with complete scorecards (smoking → lung cancer, STRONG; single observational study RR 1.3, WEAK ASSOCIATION).
- `templates/scorecard.md`: blank 9-viewpoint scorecard.
- `scripts/check_scorecard.py`: mechanical completeness checker (Python standard library only) — verifies all 9 viewpoints have a verdict, one line of evidence, and a source, and that Temporality is filled in; text and JSON output; exit 0 when complete, 1 when incomplete.
- `examples/smoking-lung-cancer.md`: complete scorecard, STRONG.
- `examples/observational-rr-1-3.md`: complete scorecard, WEAK ASSOCIATION.
- `examples/empty-scorecard.md`: blank scorecard, intentionally incomplete.
- `tests/test_check_scorecard.py`: 22 pytest cases covering the checker, including blank section fields and invalid UTF-8 input.
- GitHub Actions CI on Linux and Windows with Python 3.10 and 3.14, plus pinned test dependencies in `requirements-dev.txt`.
- `.claude-plugin/plugin.json`: Claude plugin manifest.
- `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `LICENSE` (MIT).

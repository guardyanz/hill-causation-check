# Contributing to Hill Causation Check

Thank you for contributing. This project is a small, focused Agent Skill: one authoritative source (Bradford Hill, 1965), one procedure, one checker. Please keep contributions in that spirit.

## How to contribute

1. Fork the repository and create a branch from `main`.
2. Make your change, then run the tests:
   ```bash
   python -m pip install -r requirements-dev.txt
   python -m pytest -q
   python scripts/check_scorecard.py examples/smoking-lung-cancer.md
   python scripts/check_scorecard.py examples/observational-rr-1-3.md
   ```
   All tests must pass, and both complete example scorecards must still pass the checker.
3. Open a pull request describing what changed and why.

## Rules

- **Cite sources for factual changes.** Corrections to the worked examples (effect sizes, study designs, verdicts) must come with a cited source — a paper, a textbook, or an authoritative review — not an assertion. Uncited factual changes will not be merged.
- **Do not add personal medical advice.** This skill assesses strength of evidence for general claims. Never add content that diagnoses, treats, or recommends a course of action for an individual.
- **Keep the checker mechanical.** `scripts/check_scorecard.py` checks completeness only (all 9 viewpoints present, with verdict, evidence, and source). Do not turn it into a medical judge; that judgement belongs to the human using the skill.
- **No placeholders.** Do not submit TODOs, lorem ipsum, or unfinished examples.
- **English only.** All repository content is in English.
- **Small scope.** This skill deliberately covers one framework. Do not add other causal frameworks, fact-checking, or fallacy detection to this repository; those belong in separate skills.

## Reporting issues

Open an issue with the claim, the scorecard (or the step in `SKILL.md`) that is wrong, and the source that shows the correction. For security issues, see `SECURITY.md` — do not open a public issue for those.

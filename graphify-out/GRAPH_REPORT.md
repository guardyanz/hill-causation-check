# Graph Report - hill-causation-check  (2026-11-06)

## Corpus Check
- 13 files · ~8,110 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 3)

## Summary
- 124 nodes · 169 edges · 11 communities
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 17 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- test_check_scorecard.py
- Hill Causation Check
- check_scorecard.py
- Hill Causation Check
- main
- [1.0.0] - 2026-11-06
- Hill Causation Scorecard
- Hill Causation Scorecard
- Hill Causation Scorecard
- Security Policy
- Hill Causation Scorecard

## God Nodes (most connected - your core abstractions)
1. `check_scorecard()` - 23 edges
2. `Hill Causation Check` - 16 edges
3. `build_scorecard()` - 13 edges
4. `write_scorecard()` - 13 edges
5. `Hill Causation Check` - 10 edges
6. `_check_table_rows()` - 6 edges
7. `The mechanism — 5 steps` - 6 edges
8. `_check_sections()` - 5 edges
9. `main()` - 5 edges
10. `_find_verdict()` - 4 edges

## Surprising Connections (you probably didn't know these)
- `How to contribute` --references--> `main()`  [INFERRED]
  CONTRIBUTING.md → scripts/check_scorecard.py
- `test_example_empty_scorecard_fails()` --calls--> `check_scorecard()`  [INFERRED]
  tests/test_check_scorecard.py → scripts/check_scorecard.py
- `test_example_rr_1_3_scorecard_passes()` --calls--> `check_scorecard()`  [INFERRED]
  tests/test_check_scorecard.py → scripts/check_scorecard.py
- `test_example_smoking_scorecard_passes()` --calls--> `check_scorecard()`  [INFERRED]
  tests/test_check_scorecard.py → scripts/check_scorecard.py
- `test_invalid_utf8_is_reported_as_unreadable()` --calls--> `check_scorecard()`  [INFERRED]
  tests/test_check_scorecard.py → scripts/check_scorecard.py

## Import Cycles
- None detected.

## Communities (11 total, 0 thin omitted)

### Community 0 - "test_check_scorecard.py"
Cohesion: 0.16
Nodes (27): parametrize, Path, pytest, check_scorecard(), Check one scorecard file for completeness., subprocess, build_scorecard(), Tests for scripts/check_scorecard.py. The checker verifies COMPLETENESS ONLY:… (+19 more)

### Community 1 - "Hill Causation Check"
Cohesion: 0.10
Nodes (21): A. Smoking → lung cancer: STRONG (positive control), B. One observational headline, RR 1.3, no replication: WEAK, Contributing, Development, Hill Causation Check, How this differs from nearby tools, Install — 30 seconds, License (+13 more)

### Community 2 - "check_scorecard.py"
Cohesion: 0.13
Nodes (18): argparse, dataclasses, json, pathlib, re, _check_sections(), _check_table_rows(), CheckResult (+10 more)

### Community 3 - "Hill Causation Check"
Cohesion: 0.12
Nodes (15): Hill Causation Check, Medical disclaimer, Source, Step 1 — State the claim, with numbers and design, Step 2 — The Temporality gate, Step 3 — Score the remaining 8 viewpoints, Step 4 — Assign a verdict tier, Step 5 — Say what would change the verdict (+7 more)

### Community 4 - "main"
Cohesion: 0.22
Nodes (7): Contributing to Hill Causation Check, How to contribute, Reporting issues, Rules, main(), test_cli_invalid_utf8_returns_json_error(), test_main_returns_zero_and_one()

### Community 5 - "[1.0.0] - 2026-11-06"
Cohesion: 0.40
Nodes (4): [1.0.0] - 2026-11-06, Added, Changelog, Fixed

### Community 6 - "Hill Causation Scorecard"
Cohesion: 0.40
Nodes (4): Hill Causation Scorecard, Notes, Scorecard, Verdict

### Community 7 - "Hill Causation Scorecard"
Cohesion: 0.40
Nodes (4): Hill Causation Scorecard, Notes, Scorecard, Verdict

### Community 8 - "Hill Causation Scorecard"
Cohesion: 0.40
Nodes (4): Hill Causation Scorecard, Notes, Scorecard, Verdict

### Community 9 - "Security Policy"
Cohesion: 0.40
Nodes (4): Reporting a vulnerability, Scope note, Security Policy, Supported versions

### Community 10 - "Hill Causation Scorecard"
Cohesion: 0.40
Nodes (4): Hill Causation Scorecard, Notes, Scorecard, Verdict

## Knowledge Gaps
- **50 isolated node(s):** `Fixed`, `Added`, `Rules`, `Reporting issues`, `Why this exists` (+45 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 73 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `main` to `test_check_scorecard.py`, `check_scorecard.py`?**
  _High betweenness centrality (0.183) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `check_scorecard()` (e.g. with `test_complete_scorecard_passes()` and `test_empty_temporality_fails()`) actually correct?**
  _`check_scorecard()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Fixed`, `Added`, `Rules` to the rest of the system?**
  _50 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Hill Causation Check` be split into smaller, more focused modules?**
  _Cohesion score 0.09523809523809523 - nodes in this community are weakly interconnected._
- **Should `check_scorecard.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12631578947368421 - nodes in this community are weakly interconnected._
- **Should `Hill Causation Check` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._
# Hill Causation Check

> **Every day, headlines say X causes or cures Y — and neither most readers nor most AI answers can say whether that is a real cause or only a correlation.**

**Hill Causation Check** is an Agent Skill that assesses whether X really causes Y using the nine viewpoints of Sir Austin Bradford Hill (1965). It produces a structured scorecard and a strength-of-evidence verdict — **STRONG / PLAUSIBLE / WEAK ASSOCIATION / NOT ESTABLISHED** — instead of a yes/no guess from a headline.

## Why this exists

Health headlines, social-media posts, and chatbot answers routinely turn a single observational association into a causal claim: a food "causes" a disease, a supplement "prevents" one, a habit "cures" another. Readers — and AI assistants — usually have no disciplined way to answer the follow-up question: *is the evidence strong enough to call this causation?*

Hill's nine viewpoints are the classic, still-cited framework for exactly that question. They are used in epidemiology textbooks and in causal-inference teaching sixty years after publication, yet — as of 6 November 2026 — no Agent Skill (SKILL.md) existed for them: searches of GitHub and skills.sh found no skill for the Bradford Hill criteria, only a single lesson sub-section in a course repository and flashcards. This skill fills that gap, in the same pattern as other source-grounded skills: one authoritative, numbered, public source, turned into a sharp, mechanical procedure.

## The source

- Sir Austin Bradford Hill, "The Environment and Disease: Association or Causation?", *Proceedings of the Royal Society of Medicine*, 1965;58(5):295–300.
  - Overview: https://en.wikipedia.org/wiki/Bradford_Hill_criteria
  - 50-year review: https://pmc.ncbi.nlm.nih.gov/articles/PMC4462877/

Hill called his nine points "viewpoints", not a checklist and not proof. This skill preserves that caution.

## The 9 viewpoints

1. **Strength** — how large is the association?
2. **Consistency** — has it been replicated by different researchers, in different places and times?
3. **Specificity** — one cause, one outcome? (The weakest viewpoint — failing it alone never sinks a verdict.)
4. **Temporality** — did the cause come before the effect? (The only absolute viewpoint.)
5. **Biological gradient (dose-response)** — does more exposure mean more effect?
6. **Plausibility** — is there a biologically plausible mechanism?
7. **Coherence** — does the claim fit what is already known about the disease?
8. **Experiment** — does intervening change the outcome?
9. **Analogy** — is there a similar, already-accepted causal relationship?

## Install — 30 seconds

### Option A: skills CLI

```bash
npx skills add guardyanz/hill-causation-check
```

### Option B: Claude plugin marketplace

```text
/plugin marketplace add guardyanz/hill-causation-check
/plugin install hill-causation-check@hill-causation-check
```

### Option C: manual clone

```bash
git clone https://github.com/guardyanz/hill-causation-check.git
cp -r hill-causation-check ~/.claude/skills/hill-causation-check
# or point your agent's skills directory at the cloned folder
```

The checker requires Python 3.10 or newer and uses only the standard library. It needs no API keys and makes no network calls. The skill itself is a Markdown procedure; install it in an agent that supports Agent Skills.

## Usage

1. Ask your agent to assess a claim, for example:
   > "Use hill-causation-check: does eating food Z cause disease W, based on this study?"
2. The agent follows the 5 steps in `SKILL.md`:
   1. State the claim as X → Y, with the effect size (RR/OR) and the study design. **No numbers and no design → every score is Unknown, not guessed.**
   2. **Temporality gate:** if X did not precede Y, stop — verdict NOT ESTABLISHED.
   3. Score the other 8 viewpoints Pass / Weak / Fail / Unknown, one line of evidence each.
   4. Assign a verdict tier (STRONG needs Temporality + Strength + Consistency passing and ≥7 Pass; PLAUSIBLE is 4–6 Pass; WEAK ASSOCIATION is ≤3 Pass; NOT ESTABLISHED is Temporality failing, or Strength and Consistency both failing).
   5. Say what would change the verdict — the missing study, named specifically.
3. Fill in the scorecard from `templates/scorecard.md` and check it:

```bash
python scripts/check_scorecard.py examples/smoking-lung-cancer.md
```

Real output:

```text
examples/smoking-lung-cancer.md: COMPLETE
  [ok] Strength: Pass
  [ok] Consistency: Pass
  [ok] Specificity: Weak
  [ok] Temporality: Pass
  [ok] Biological gradient: Pass
  [ok] Plausibility: Pass
  [ok] Coherence: Pass
  [ok] Experiment: Pass
  [ok] Analogy: Pass
```

An incomplete scorecard fails with a per-criterion list of what is missing:

```bash
python scripts/check_scorecard.py examples/empty-scorecard.md
# examples/empty-scorecard.md: INCOMPLETE
#   - Strength: evidence is missing or too short (write one line of evidence)
#   - Strength: source is missing (cite the study or source for this row)
#   ... (one pair of errors per empty row; exit code 1)
```

**The checker verifies completeness only.** It checks that all 9 viewpoints have a verdict, evidence, and a source, and that Temporality is filled in. It does **not** judge whether the evidence is medically correct. That judgement is the human's job.

## Worked examples

Both examples are in `examples/` and in `SKILL.md`, with a full scorecard per viewpoint.

### A. Smoking → lung cancer: STRONG (positive control)

Effect: lung-cancer death rate among male smokers about 24 times that of non-smokers (+2,300%); about 8 times for women (+700%); heavy smokers RR ~10–20. Design: prospective cohort studies (Doll & Hill). Verdict: **STRONG** — Temporality, Strength, and Consistency all pass, 8 of 9 viewpoints Pass (only Specificity is Weak).

### B. One observational headline, RR 1.3, no replication: WEAK

Effect: a single cohort study reports RR 1.3 (95% CI 1.05–1.6), no replication, no dose-response. Verdict: **WEAK ASSOCIATION** — only 1 of 9 viewpoints Pass. This is an association, not proven causation. Do not change behaviour on the basis of this alone.

## Why this matters — who needs it

- **Health-news readers, parents, and patients** deciding whether a headline deserves a behaviour change.
- **Health journalists and creators** who want to report a study without overstating it.
- **Users of AI chatbots for health advice** — a KFF survey (March 2026) found 32% of US adults had used an AI chatbot for health advice in the past year, and a 2026 JAMA study found 21.6% of US adults had made a health decision based on social media. Those answers need an evidence-strength discipline, not just a confident tone.

## How this differs from nearby tools

| Tool | Question it answers | What it does not do |
|---|---|---|
| **Fact-checker** | Is this single claim true or false? | It does not assess causation. A claim can be factually correct as an association and still misleading as a cause. |
| **Fallacy detector** | Is the argument's structure valid? | It does not assess the evidence base for a causal claim against empirical viewpoints. |
| **Hill Causation Check (this skill)** | Given the published evidence, how strong is the case that X *causes* Y? | It does not fact-check individual statements, detect fallacies, or give personal medical advice. |

The nearest competitors are not duplicates: they answer different questions. This skill's job is the causal question specifically.

## Limitations — read before trusting a verdict

- **Hill's viewpoints are not proof.** A STRONG verdict means the evidence base is strong, not that causation is proven with certainty. A WEAK verdict means the causal case is not established, not that the association is false.
- **Specificity is weak by design.** Many real causes have many effects. Do not treat a Specificity Fail as a veto.
- **Plausibility depends on the knowledge of the day.** A missing mechanism is not proof against causation — and a plausible mechanism is not proof for it.
- **The skill is only as good as the sources it is given.** If the agent cannot fetch the study, the honest output is Unknown, not a guess. Headlines, press releases, and social posts are never sufficient evidence.
- **Confounding and bias are assessed through the viewpoints (especially Strength and Consistency), not by a separate statistical test.** This skill does not re-analyse raw data.
- **Scope is general claims, not individuals.** See the disclaimer below.

## Medical disclaimer

This skill assesses the strength of published evidence for a general claim. It does **not** give personal medical advice, diagnose, or recommend treatment. Medical decisions belong with a qualified clinician. If a claim concerns a specific person's health, the agent must say so and stop at the evidence verdict.

## Repository layout

```text
hill-causation-check/
├── SKILL.md                    # The skill: 5-step mechanism + worked examples
├── .claude-plugin/             # Claude plugin manifest and marketplace catalog
├── .github/workflows/ci.yml    # Tests on Linux and Windows
├── requirements-dev.txt       # Test dependencies
├── templates/scorecard.md      # Blank 9-viewpoint scorecard
├── scripts/check_scorecard.py  # Completeness checker (Python stdlib only)
├── examples/
│   ├── smoking-lung-cancer.md  # Complete scorecard — STRONG
│   ├── observational-rr-1-3.md # Complete scorecard — WEAK ASSOCIATION
│   └── empty-scorecard.md      # Blank scorecard (intentionally incomplete)
└── tests/test_check_scorecard.py
```

## Development

```bash
python -m venv .venv
# Activate: source .venv/bin/activate (Linux/macOS)
# Activate: .venv\Scripts\Activate.ps1 (PowerShell)
python -m pip install -r requirements-dev.txt
python -m pytest -q
python scripts/check_scorecard.py examples/smoking-lung-cancer.md
python scripts/check_scorecard.py --format json examples/observational-rr-1-3.md
```

CI runs the test suite and both complete examples on Python 3.10 and 3.14, on Linux and Windows. The blank template and `examples/empty-scorecard.md` intentionally return exit code 1 until filled in.

## Roadmap

- [ ] Worked scorecards for two more classic cases (a contested association and a reversed verdict after replication).
- [ ] A `--strict` checker mode that also requires an effect size and study design in the scorecard header.
- [ ] Translations of the template (not the verdict logic) for non-English newsrooms.
- [ ] An optional GitHub Action that runs the completeness checker on scorecards in a pull request.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Corrections to the worked examples are welcome — with a cited source, not an assertion.

## License

MIT — see [LICENSE](LICENSE).

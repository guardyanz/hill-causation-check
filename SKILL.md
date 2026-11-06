---
name: hill-causation-check
description: Assess whether X really causes Y — or is only correlated with it — using the 9 Bradford Hill viewpoints (1965). Use when a headline, post, paper, or chatbot claims that something causes, prevents, or cures a disease or health outcome, or when you need a structured evidence-strength verdict (STRONG / PLAUSIBLE / WEAK ASSOCIATION / NOT ESTABLISHED) with a scorecard. This skill judges strength of evidence, not personal medical advice.
---

# Hill Causation Check

## The problem in one sentence

Every day, headlines say X causes or cures Y, and neither most readers — nor most AI answers — can say whether that is a real cause or only a correlation.

## Source

This skill is built on one authoritative public source, not on vibes:

- Sir Austin Bradford Hill, "The Environment and Disease: Association or Causation?", *Proceedings of the Royal Society of Medicine*, 1965;58(5):295–300.
  - Overview: https://en.wikipedia.org/wiki/Bradford_Hill_criteria
  - 50-year review: https://pmc.ncbi.nlm.nih.gov/articles/PMC4462877/

Hill called his nine points "viewpoints", not a checklist and not proof. No single viewpoint proves causation, and no single failure — except Temporality, see Step 2 — disproves it. This skill preserves that caution. It produces a **strength-of-evidence verdict**, never a medical recommendation for an individual.

## Medical disclaimer

This skill assesses the strength of published evidence for a general claim. It does **not** give personal medical advice, diagnose, or recommend treatment. Medical decisions belong with a qualified clinician. If a claim concerns a specific person's health, say so and stop at the evidence verdict.

## The 9 viewpoints

1. **Strength** — How large is the association? A large effect (for example, a relative risk of 10) is harder to explain away by bias or confounding than a small one (for example, RR 1.1).
2. **Consistency** — Has the association been observed repeatedly, by different researchers, in different places, circumstances, and times?
3. **Specificity** — Is the outcome linked to one particular cause, and the cause to one particular outcome? **This is the weakest viewpoint.** A cause can have many effects and an outcome many causes. Failing Specificity alone never sinks a verdict.
4. **Temporality** — Did the cause come before the effect? This is the **only absolute viewpoint** (see Step 2).
5. **Biological gradient (dose-response)** — Does more exposure lead to more of the effect (or a clear gradient, including a threshold)?
6. **Plausibility** — Is there a biologically plausible mechanism? Plausibility depends on the knowledge of the day; lack of a known mechanism is not proof against causation.
7. **Coherence** — Does the causal interpretation conflict with what is already known about the natural history and biology of the disease? A claim should not contradict established facts without explaining why.
8. **Experiment** — Does intervening change the outcome? For example, does removing the exposure lower the risk, or does a randomised trial show an effect?
9. **Analogy** — Is there a similar, already-accepted cause-and-effect relationship that makes this one more credible?

## The mechanism — 5 steps

Follow these steps in order. Do not skip Step 1 or Step 2.

### Step 1 — State the claim, with numbers and design

Write the claim as **X → Y**, then fetch the source study (not the headline) and record:

- **Effect size with a number:** relative risk (RR), odds ratio (OR), hazard ratio (HR), or absolute risk difference, with its confidence interval. Quote it exactly.
- **Study design:** randomised controlled trial (RCT), cohort, case-control, cross-sectional, meta-analysis, or case report. Record the sample size and population.
- **Who, where, when:** population, setting, follow-up time.

**Rule: no numbers and no design → every score is Unknown, not guessed.** Do not infer an effect size from a headline, a press release, or a social-media post. If you cannot fetch the study, say "source not retrieved — verdict Unknown" and stop. A headline alone is never evidence.

Example of a well-formed claim:

> Claim: Smoking (X) → lung cancer (Y). Effect: heavy smokers have a lung-cancer mortality rate roughly 10–20 times that of non-smokers (RR ~10–20). Design: prospective cohort studies, including Doll & Hill's British doctors study and many replications. Source: Hill (1965); Doll & Hill (1950, 1956).

Example of a claim that fails Step 1:

> Claim: "Coffee causes heart disease." No effect size quoted, no study design named, source is a headline. → All scores Unknown. Stop.

### Step 2 — The Temporality gate

Ask one question: **did X come before Y?**

- If the evidence shows X preceded Y → continue to Step 3.
- If X did **not** precede Y, or the study cannot establish the order (for example, a cross-sectional study measuring exposure and outcome at the same time) → **STOP. Verdict: NOT ESTABLISHED.** No other score can rescue a causal claim when the supposed cause follows the effect.

Temporality is the only viewpoint Hill treated as essential in this sense. Every other viewpoint is supporting evidence, not a veto.

### Step 3 — Score the remaining 8 viewpoints

Score each of the other 8 viewpoints as **Pass / Weak / Fail / Unknown**, with **exactly one line of evidence** per viewpoint. One line means one sentence (or one short clause) stating the fact that justifies the score — not a paragraph, not an opinion.

- **Pass** — the evidence clearly supports the viewpoint.
- **Weak** — there is some supporting evidence, but it is thin, indirect, or mixed.
- **Fail** — the evidence goes against the viewpoint.
- **Unknown** — no usable evidence was found. Unknown is a legitimate score, not a failure to look.

Record the scorecard using `templates/scorecard.md`. Every row needs a verdict, one line of evidence, and a source. A row without a source is incomplete — see `scripts/check_scorecard.py`.

### Step 4 — Assign a verdict tier

Count the **Pass** scores across all 9 viewpoints, then apply the tiers:

| Tier | Rule |
|---|---|
| **STRONG** | Temporality passes, **and** Strength passes, **and** Consistency passes, **and** at least 7 of the 9 viewpoints are Pass |
| **PLAUSIBLE** | Temporality passes, and 4–6 of the 9 viewpoints are Pass |
| **WEAK ASSOCIATION** | Temporality passes, but at most 3 of the 9 viewpoints are Pass |
| **NOT ESTABLISHED** | Temporality fails, **or** Strength and Consistency both fail |

Notes on the tiers:

- A claim can be a real, replicated association and still be WEAK ASSOCIATION as a *causal* claim. That is the point: association is not causation.
- Specificity failing does not block STRONG. It is the weakest viewpoint.
- If most scores are Unknown because the source study could not be retrieved, the honest tier is WEAK ASSOCIATION at best — never PLAUSIBLE or STRONG on missing evidence.
- State the tier in one line, then the scorecard. Do not bury the verdict in prose.

### Step 5 — Say what would change the verdict

End every assessment with one line of the form:

> **What would change this verdict:** [the missing study or evidence].

Be specific. Name the study design, not a vague wish. Examples:

- "An RCT, or a large prospective cohort with measured exposure before outcome, showing a consistent effect."
- "Independent replication in a different population."
- "A dose-response gradient across at least three exposure levels."
- "Evidence that risk falls after the exposure is removed (Experiment)."

If the verdict is STRONG, say what would *weaken* it instead (for example, "a large, well-conducted study finding no association after full adjustment for confounding").

## Worked example A — Positive control: smoking → lung cancer (STRONG)

Source: Hill (1965); Doll & Hill, "Smoking and carcinoma of the lung" (1950) and the British doctors prospective study (1956); U.S. Surgeon General (1964). Effect sizes below are the figures Hill himself cited.

Claim: Smoking (X) → lung cancer (Y).
Effect: lung-cancer death rate among male smokers about 24 times that of non-smokers in Hill's cited data — a rise of roughly 2,300% for men and about 700% for women; heavy smokers show RR ~10–20 versus non-smokers. Design: prospective cohort studies plus case-control studies.

| # | Viewpoint | Verdict | Evidence (one line) |
|---|---|---|---|
| 1 | Strength | Pass | Effect is very large: male smokers' lung-cancer death rate ~24× non-smokers (+2,300%), women ~8× (+700%), heavy smokers RR ~10–20. |
| 2 | Consistency | Pass | Association replicated in dozens of studies, in different countries and populations, by different investigators. |
| 3 | Specificity | Weak | Smoking is linked to many diseases and lung cancer has other causes, so specificity is limited — the weakest viewpoint, and it does not block the verdict. |
| 4 | Temporality | Pass | Smoking precedes lung cancer by years in prospective cohorts; exposure was measured before the outcome. |
| 5 | Biological gradient | Pass | Risk rises with amount smoked: heavier smokers have higher lung-cancer rates than light smokers. |
| 6 | Plausibility | Pass | Tobacco smoke contains known carcinogens that reach lung tissue. |
| 7 | Coherence | Pass | The rise in lung cancer follows the rise in cigarette smoking and fits the known biology of the disease. |
| 8 | Experiment | Pass | Risk falls after quitting smoking, and rises again with resumed heavy smoking. |
| 9 | Analogy | Pass | Other inhaled carcinogens (for example, occupational exposures) are accepted causes of lung cancer. |

**Verdict: STRONG** — Temporality, Strength, and Consistency all pass, and 8 of 9 viewpoints are Pass (only Specificity is Weak).

**What would change this verdict:** a large, well-conducted prospective study finding no association between smoking and lung cancer after full adjustment — no such study exists in the cited literature.

## Worked example B — One observational headline: RR 1.3, no replication (WEAK)

Claim: Eating food Z (X) → disease W (Y), as reported in a single news headline.
Effect: one observational (cohort) study reports RR 1.3 (95% CI 1.05–1.6). Design: single prospective cohort; no RCT, no meta-analysis, no replication yet.

| # | Viewpoint | Verdict | Evidence (one line) |
|---|---|---|---|
| 1 | Strength | Weak | RR 1.3 is a small effect that confounding or measurement error could plausibly explain. |
| 2 | Consistency | Fail | No independent replication; a single study in one population. |
| 3 | Specificity | Unknown | No evidence presented on whether Z is linked specifically to W. |
| 4 | Temporality | Pass | Exposure was measured at baseline, before the outcome occurred. |
| 5 | Biological gradient | Unknown | The study reports one exposure level only; no dose-response gradient is shown. |
| 6 | Plausibility | Weak | A mechanism is proposed but not demonstrated in humans. |
| 7 | Coherence | Unknown | No check against the known natural history of the disease is presented. |
| 8 | Experiment | Unknown | No trial or cessation study; nobody has shown removing Z lowers risk. |
| 9 | Analogy | Weak | A related food is loosely analogous, but no accepted causal analogue is cited. |

**Verdict: WEAK ASSOCIATION** — Temporality passes, but only 1 of 9 viewpoints is Pass. This is an association, not proven causation.

**What would change this verdict:** independent replication in a different population, a dose-response gradient across exposure levels, and ideally an RCT or a trial showing risk falls when Z is removed.

**Do not change behaviour on the basis of this alone.** A single RR 1.3 from one observational study is the kind of result that routinely fails to replicate.

## What this skill is not

- **Not a fact-checker.** A fact-checker answers "is this single claim true or false?" This skill answers a different question: "even if the association is real, is it causal?" A claim can be factually correct as an association and still misleading as a cause.
- **Not a fallacy detector.** A fallacy detector checks the structure of an argument. This skill checks the *evidence base* for a causal claim against nine empirical viewpoints.
- **Not a diagnosis or treatment tool.** See the medical disclaimer above.
- **Not a substitute for reading the study.** If you cannot fetch the study, the verdict is Unknown — the skill does not guess from headlines.

## Using the scorecard template

1. Copy `templates/scorecard.md` to a new file for your claim.
2. Fill in the claim, effect size, study design, and source in the header.
3. Fill in all 9 rows: verdict, one line of evidence, source.
4. Run the completeness checker: `python scripts/check_scorecard.py your-scorecard.md`
5. Assign the verdict tier (Step 4) and write the "what would change this verdict" line (Step 5).

The checker verifies **completeness only** — that all 9 viewpoints have a verdict, evidence, and a source, and that Temporality is filled in. It does not judge whether the evidence is medically correct. That judgement is the human's (and the skill's) job.

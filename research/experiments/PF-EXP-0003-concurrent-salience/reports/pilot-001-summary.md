# PF-EXP-0003 pilot-001 summary

> Aggregate audit summary  
> Raw Interpretation remains local/private.

## Outcome

- Stimulus pretest: **16 / 16 succeeded; all pretest gates passed**
- Main generation: **96 / 96 succeeded**
- Blind evaluation: **96 / 96 succeeded**
- Overall gate: **FAIL**
- Passed: **G1, G2, G5**
- Failed: **G3, G4**

Pre-frozen thresholds were not changed after observing results.

## Research question

> OpportunityとDangerが同時に存在するとき、High Seeking ReactivityはOpportunity Salienceを高めながら、Danger Salienceを失わずに保持するか。

Primary interaction:

`C_D = ΔD_T11 - ΔD_T01`

Hypothesized direction: **`C_D > 0`**.

## Pretest

| Measure | Observed | Threshold | Result |
|---|---:|---:|---|
| Opportunity main effect | 2.125 | >= 1.50 | PASS |
| Opportunity→Danger cross effect (absolute mean) | 0.500 | <= 0.50 | PASS |
| Opportunity direction | 8/8 families | >= 7/8 | PASS |

The Danger stability gate passed exactly at its upper boundary. In F01, F03, F04, and F05, the Opportunity manipulation changed evaluator-rated Danger Value by +1 despite identical Danger wording within the family. This is retained as an interpretation caveat; stimuli and thresholds were not changed post hoc.

## Cell means

| Condition | Opportunity | n | Opportunity Salience | Danger Salience | Seeking Activation | Negative Activation | Joint Salience | Concurrent Rate |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| T01 Low S / High N | Low | 24 | 0.792 | 2.958 | 0.000 | 2.167 | 0.792 | 0.083 |
| T01 Low S / High N | High | 24 | 2.125 | 3.083 | 0.250 | 2.375 | 2.125 | 1.000 |
| T11 High S / High N | Low | 24 | 1.917 | 2.583 | 1.417 | 2.083 | 1.875 | 0.792 |
| T11 High S / High N | High | 24 | 3.000 | 2.792 | 1.542 | 2.042 | 2.792 | 1.000 |

## Main effects and frozen gates

| Gate | Result | Key observation |
|---|---|---|
| G1 Pretest | PASS | All stimulus pretest gates passed |
| G2 Seeking / Opportunity uptake | PASS | Seeking main = 1.354; T11 Opportunity delta = 1.083 |
| G3 Danger preservation | FAIL | T11 Danger delta = +0.208 passed its component threshold, but primary interaction = **+0.083**, below required +0.20 |
| G4 Family generalization | FAIL | Positive family interactions = **4/8** after numerical zero normalization; minimum leave-one-family-out mean = **-0.048** |
| G5 Concurrent Salience state | PASS | T11/O-high Opportunity = 3.000, Danger = 2.792, Concurrent Rate = 1.000 |

Overall: **`all_gates_pass = false`**.

## Family-level primary interaction

`C_family = ΔD_T11 - ΔD_T01`

| Family | C |
|---|---:|
| F01 | -0.333 |
| F02 | +0.333 |
| F03 | -0.333 |
| F04 | +0.333 |
| F05 | 0.000 |
| F06 | +1.000 |
| F07 | +0.333 |
| F08 | -0.667 |

Positive direction: **4/8 families**. The family pattern is heterogeneous rather than consistently positive.

Leave-one-family-out means ranged from **-0.048 to +0.190**. Omitting F06 changes the mean interaction to a negative value, so the positive aggregate interaction does not generalize robustly across families.

## Numerical audit correction

The first analysis output represented the mathematically zero F05 interaction as `4.440892098500626e-16` due to floating-point arithmetic and therefore counted it as `> 0`.

The analyzer was corrected after gate inspection to normalize values with absolute magnitude `<= 1e-12` to zero. This changes only the displayed/derived positive-family count from 5 to **4**. It does **not** alter any stimulus, response, score, frozen threshold, primary interaction, or overall gate conclusion. G4 was already FAIL because its leave-one-family-out criterion failed.

## Interpretation

The primary hypothesis is **not supported**. High Seeking Reactivity did not reliably preserve Danger Salience more strongly than Low Seeking Reactivity when Opportunity increased.

At the same time, G5 shows that high Opportunity Salience and high Danger Salience can coexist clearly within one Interpretation. However, this concurrent state was not unique to High S: T01/O-high also had Concurrent Rate = 1.000.

The most conservative result is therefore:

> **OpportunityとDangerはInterpretation内で同時に高いSalienceを持ち得るが、その同時保持がHigh Seeking Reactivityによって特別に強化されるという証拠は得られなかった。**

This result is consistent with the current canonical model, which permits S/N-related tendencies to coexist without requiring a new internal Concurrent Salience mechanism.

## Model boundary and next step

- Do **not** add a new Concurrent Salience / Attention / Salience Competition variable to the canonical Personality Formation Model from this pilot.
- Treat PF-EXP-0003 as a completed gate-fail pilot.
- Next research step should move downstream in the canonical process and test what determines **Response** when Opportunity and Danger are simultaneously salient in Interpretation.
- Regulation should be introduced only as required by that Response experiment, consistent with the canonical `Interpretation -> Regulation -> Response` structure.

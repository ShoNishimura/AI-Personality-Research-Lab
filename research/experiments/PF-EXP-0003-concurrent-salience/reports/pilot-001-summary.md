# PF-EXP-0003 pilot-001 summary

> Aggregate audit summary  
> Execution-time term: `Interpretation`  
> Current conceptual term: **Perception**

## Terminology alignment

本pilotはPersonality Formation Model v1.0時点で実行され、生成対象を `Interpretation` と呼んでいた。

v1.1では、Opportunity / Danger SalienceおよびSeeking / Negative Activationを **Perceptionの観測**として再位置づける。実行済みデータ、Gate、閾値、hash、集計値は変更しない。

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
| Opportunity→Danger cross effect | 0.500 | <= 0.50 | PASS |
| Opportunity direction | 8/8 families | >= 7/8 | PASS |

## Cell means

| Condition | Opportunity | Opportunity Salience | Danger Salience | Concurrent Rate |
|---|---|---:|---:|---:|
| T01 Low S / High N | Low | 0.792 | 2.958 | 0.083 |
| T01 Low S / High N | High | 2.125 | 3.083 | 1.000 |
| T11 High S / High N | Low | 1.917 | 2.583 | 0.792 |
| T11 High S / High N | High | 3.000 | 2.792 | 1.000 |

## Frozen gates

| Gate | Result | Key observation |
|---|---|---|
| G1 Pretest | PASS | All stimulus pretest gates passed |
| G2 Seeking / Opportunity uptake | PASS | Seeking main = 1.354; T11 Opportunity delta = 1.083 |
| G3 Danger preservation | FAIL | T11 Danger delta = +0.208, but primary interaction = **+0.083 < +0.20** |
| G4 Family generalization | FAIL | Positive family interactions = **4/8**; minimum leave-one-family-out = **-0.048** |
| G5 Concurrent Salience state | PASS | T11/O-high Opportunity = 3.000, Danger = 2.792, Concurrent Rate = 1.000 |

Overall: **`all_gates_pass = false`**.

## Family-level interaction

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

## Numerical audit correction

The first analysis output represented the mathematically zero F05 interaction as a tiny positive floating-point residue. The analyzer normalized values with absolute magnitude `<= 1e-12` to zero. This changed the positive-family count from 5 to **4** and did not change the overall gate conclusion.

## v1.1 interpretation of the result

The primary hypothesis is **not supported**.

> **OpportunityとDangerはPerception内で同時に高いSalienceを持ち得るが、その同時保持がHigh Seeking Reactivityによって特別に強化されるという証拠は得られなかった。**

PF-EXP-0003は現行モデルの `P=f(E,T0)` に対応するPerception実験として位置づける。

このpilotから新しいConcurrent Salience機構を追加しない。また、Response、History、Relationshipについての結論は含まない。
# PF-EXP-0002 pilot-001 summary

> Aggregate audit summary  
> Execution-time term: `Interpretation`  
> Current conceptual term: **Perception**

## Terminology alignment

本pilotはPersonality Formation Model v1.0時点で実行され、生成対象を `Interpretation` と呼んでいた。

v1.1では、Opportunity / Danger SalienceおよびSeeking / Negative Activationを **Perceptionの観測**として再位置づける。実行済みデータ、Gate、閾値、hash、集計値は変更しない。

## Outcome

- Stimulus pretest: **24 / 24 succeeded; all pretest gates passed**
- Main generation: **192 / 192 succeeded**
- Blind evaluation: **192 / 192 succeeded**
- Overall gate: **FAIL**
- Passed: G1, G2
- Failed: G3, G4

The pre-frozen thresholds are not changed after observing results.

## Pretest

| Measure | Observed | Threshold | Result |
|---|---:|---:|---|
| Opportunity main effect | 2.000 | >= 1.50 | PASS |
| Danger main effect | 2.167 | >= 1.50 | PASS |
| Opportunity→Danger cross contamination | 0.167 | <= 0.75 | PASS |
| Danger→Opportunity cross contamination | 0.000 | <= 0.75 | PASS |
| Family direction | 6/6 each | >= 5/6 | PASS |

## Main effects and frozen gates

| Gate | Result | Key observation |
|---|---|---|
| G1 Pretest | PASS | All stimulus pretest gates passed |
| G2 Temperament replication | PASS | Seeking main = 1.271; Negative main = 1.021 |
| G3 Target interaction | FAIL | Primary interaction = **+0.250**, while hypothesis required <= -0.50; 0/6 families were negative |
| G4 Generalization | FAIL | Leave-one-family-out means = +0.20 to +0.30, while threshold required <= -0.25 |

The original hypothesis was:

> Increasing Opportunity Value would reduce Danger Salience more strongly under High Seeking Reactivity.

That directional hypothesis was **not supported**.

## Family-level target interaction

| Family | C |
|---|---:|
| F01 | +0.50 |
| F02 | 0.00 |
| F03 | 0.00 |
| F04 | +0.50 |
| F05 | +0.50 |
| F06 | 0.00 |

## Post-gate descriptive analysis

| Condition | Opportunity | Opportunity Salience | Danger Salience |
|---|---|---:|---:|
| T01 Low S / High N | Low | 0.917 | 3.250 |
| T01 Low S / High N | High | 2.333 | 3.083 |
| T11 High S / High N | Low | 2.083 | 2.750 |
| T11 High S / High N | High | 3.000 | 2.833 |

The post-gate pattern is exploratory only. It motivated [PF-EXP-0003 — Concurrent Salience](../../PF-EXP-0003-concurrent-salience/).

## v1.1 interpretation of the result

PF-EXP-0002は、現行モデルの `P=f(E,T0)` の内部で、Opportunity / DangerというExperience特性とS/NがPerceptionのsalienceへどう作用するかを検証したpilotとして位置づける。

Response、History、Relationshipについての結論は含まない。
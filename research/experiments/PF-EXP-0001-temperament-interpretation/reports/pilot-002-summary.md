# PF-EXP-0001 pilot-002 summary

> Aggregate audit summary  
> Execution-time term: `Interpretation`  
> Current conceptual term: **Perception**

## Terminology alignment

本pilotはPersonality Formation Model v1.0時点で実行され、生成対象を `Interpretation` と呼んでいた。

Personality Formation Model v1.1では、同じ生成対象とSeeking / Negative Activationの評価を **Perceptionの観測**として再位置づける。

実行済みデータ、Gate、閾値、hash、集計値は変更しない。

## Outcome

- Generation: **96 / 96 succeeded**
- Blind evaluation: **96 / 96 succeeded**
- Overall gate: **FAIL**
- Passed: G1, G2, G3, G5
- Failed: G4 only

| Gate | Result | Key observation |
|---|---|---|
| G1 Seeking main effect | PASS | 2.00 >= 0.75 |
| G2 Negative main effect | PASS | 1.9167 >= 0.75 |
| G3 Discriminant validity | PASS | cross/main ratios 0.125 and 0.217 |
| G4 Conflict coactivation | FAIL | T11 Negative mean 1.833 < 2.0; joint activation 0.833 |
| G5 Neutrality | PASS | condition mean ranges: Seeking 0.333, Negative 0.0 |

The pre-frozen threshold is not changed after observing results.

## Post-gate exploratory inspection

G4の未達要因を診断するため、Gate判定後にConflict × T11をscoreだけでunblindした。生成本文は読んでいない。

`ST-C-01` の4条件平均:

| Condition | Seeking | Negative |
|---|---:|---:|
| T00 | 1.0 | 0.0 |
| T01 | 1.0 | 2.5 |
| T10 | 3.0 | 0.0 |
| T11 | 2.5 | 1.5 |

Exploratory interaction contrasts:

- Seeking: **-0.50**
- Negative: **-1.00**

This does **not** establish a general S×N antagonistic interaction because it was discovered post hoc from one stimulus with two replicates.

It motivated the next independent pilot:

> [PF-EXP-0002 — Opportunity × Danger Interaction](../../PF-EXP-0002-opportunity-danger-interaction/)

## v1.1 interpretation of the result

PF-EXP-0001は現行モデルの `P=f(E,T0)` に対応するpilotとして読む。

すなわち、同一Experienceに対してS/NがPerceptionを系統的に偏らせ得るかを検証した結果であり、TemperamentからResponseへの直接効果を示すものではない。
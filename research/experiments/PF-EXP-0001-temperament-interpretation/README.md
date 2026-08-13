# PF-EXP-0001 — Temperament → Perception

> Status: **pilot-002 completed — 4/5 gates passed; G4 failed**  
> Current Canonical Model: [Personality Formation Model v1.1](../../../docs/models/Personality_Formation_Model.md)  
> Execution-time term: **Interpretation**

## Terminology alignment

PF-EXP-0001はPersonality Formation Model v1.0時点で実行され、生成対象を `Interpretation` と呼んでいた。

v1.1では、その生成対象とSeeking Activation / Negative Activationの評価を **Perceptionの観測**として再位置づける。

実行済みprompt、schema、config、artifactのfield名、Gate、閾値、hash、集計結果は変更しない。ディレクトリ名も監査性のため保持する。

## Research Question

**同一のExperienceに対し、Seeking Reactivity（S）とNegative Affectivity（N）は、想定した方向へ独立かつ再現可能なPerceptionの偏りを生むか。**

```text
Temperament T0 = (S, N)
          │
          ▼
Experience ──► Perception
```

現行v1.1の `P=f(E,T0)` に対応する実験として扱う。Response、History、Relationshipは扱わない。

## Design

S / NをHigh / Lowにした2×2 factorial design。

| Condition | S | N |
|---|---|---|
| T00 | Low | Low |
| T01 | Low | High |
| T10 | High | Low |
| T11 | High | High |

12 stimuli × 4 conditions × 2 replicates = **96 generation runs**。

blind evaluatorは実行時名称 `Interpretation` の生成テキストからSeeking Activation / Negative Activationを0–4で評価した。v1.1ではこれをPerceptionの観測として読む。

## Frozen gates and result

| Gate | Criterion | Result |
|---|---|---|
| G1 | Seeking-targetのS High − S Low平均差 ≥ 0.75 | PASS — **2.00** |
| G2 | Negative-targetのN High − N Low平均差 ≥ 0.75 | PASS — **1.9167** |
| G3 | cross-effect / main effect ≤ 0.50 | PASS — **0.125 / 0.217** |
| G4 | Conflict T11で両軸平均 ≥2.00、joint rate ≥0.67 | **FAIL** — Negative **1.833**、joint **0.833** |
| G5 | Neutral condition mean range ≤0.75 | PASS — Seeking **0.333** / Negative **0.0** |

Overall: **FAIL (4/5 gates passed)**。事前Gateは変更しない。

詳細は [`reports/pilot-002-summary.md`](reports/pilot-002-summary.md) を参照する。

## Post-gate observation

`ST-C-01` の探索的S×N interactionはPF-EXP-0002の仮説生成にのみ使用した。一般的な相互作用の証拠とは扱わない。

## v1.1 interpretation of the result

PF-EXP-0001はTemperamentがResponseを直接変えることを検証した実験ではない。

現行モデルでは、**S/Nが同一ExperienceのPerceptionを系統的に偏らせ得るかを検証したpilot**として位置づける。

数値、Gate判定、結論は変更しない。

## Audit boundary

実行済みのprompt、schema、config、status、raw artifact field、thresholds、hashは実行時記録のまま保持する。用語変更のために過去の実験条件を書き換えない。
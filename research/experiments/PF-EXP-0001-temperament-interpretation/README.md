# PF-EXP-0001 — Temperament → Interpretation

> Status: **pilot-002 completed — 4/5 gates passed; G4 failed**  
> Research Track: **Personality Formation**  
> Canonical Framework: [APRL Research Framework v1.0](../../../docs/APRL_Research_Framework.md)  
> Canonical Model: [APRL Personality Formation Model v1.0](../../../docs/models/Personality_Formation_Model.md)

## Research Question

**同一のExperienceに対し、Seeking Reactivity（S）とNegative Affectivity（N）は、想定した方向へ独立かつ再現可能なInterpretationの偏りを生むか。**

```text
Temperament T0 = (S, N)
          │
          ▼
Experience ──► Interpretation
```

本実験はこの最初の接続だけを対象とし、Regulation、Response、History / Biography、Relationship、Audience / Resonanceは扱わない。

## Design

S / NをHigh / Lowにした2×2 factorial design。

| Condition | S | N |
|---|---|---|
| T00 | Low | Low |
| T01 | Low | High |
| T10 | High | Low |
| T11 | High | High |

Pilot stimuliは12件、各condition × stimulusを2 replicateとし、96 generation runsを行う。

| Class | Count | Primary purpose |
|---|---:|---|
| Seeking-target | 3 | Sの主効果 |
| Negative-target | 3 | Nの主効果 |
| Conflict | 3 | S / Nのcoactivation |
| Neutral | 3 | 不要なcondition effect |

各runは `H0 = ∅` の独立context。CharacterはInterpretationのみを生成し、別のblind evaluatorがSeeking Activation / Negative Activationを0–4で評価する。

## Frozen gates

| Gate | Frozen criterion |
|---|---|
| G1 | Seeking-targetのS High − S Low平均差 ≥ **0.75** |
| G2 | Negative-targetのN High − N Low平均差 ≥ **0.75** |
| G3 | 各cross-effect / 対応するmain effect ≤ **0.50** |
| G4 | ConflictのT11で両軸平均 ≥ **2.00**、かつ両軸2以上の割合 ≥ **0.67** |
| G5 | Neutralのcondition mean rangeが各軸 ≤ **0.75** |

Gateはpilot response観測前に [`thresholds.yaml`](thresholds.yaml) へ固定し、結果観測後には変更していない。

## Pilot history

### pilot-001 — technical incomplete

- planned generation: 96
- unique succeeded: 89
- missing: 7
- failed attempt records: 20
- JSONDecodeError: truncated JSON 16、empty/non-JSON start 4
- generation `max_output_tokens`: 220
- blind evaluation / Gate analysis: 未実施

output token budget不足が主要因と推定したが、当時は `response.status` / `incomplete_details.reason` を保存していなかったため原因は推定として扱う。設定は [`runs/pilot-001/executed-config.yaml`](runs/pilot-001/executed-config.yaml)、状態は [`runs/pilot-001/status.yaml`](runs/pilot-001/status.yaml) に保持する。

### pilot-002 — completed

pilot-001と同じ研究条件・刺激・Gateを維持し、技術的出力上限のみ事前修正して96件を最初から再実行した。

- generation `max_output_tokens`: 800
- evaluation `max_output_tokens`: 400
- generation: **96 / 96 succeeded**
- blind evaluation: **96 / 96 succeeded**
- G1: PASS — Seeking main effect **2.00**
- G2: PASS — Negative main effect **1.9167**
- G3: PASS — cross/main ratios **0.125 / 0.217**
- G4: **FAIL** — T11 Negative mean **1.833 < 2.0**。ただしjoint activation rate **0.833**
- G5: PASS — Neutral condition ranges: Seeking **0.333** / Negative **0.0**
- overall: **FAIL (4/5 gates passed)**

詳細は [`reports/pilot-002-summary.md`](reports/pilot-002-summary.md) と [`runs/pilot-002/status.yaml`](runs/pilot-002/status.yaml) を参照する。

## Post-gate exploratory observation

G4診断のため、Gate判定後にConflict × T11の**scoreだけ**をunblindした。Interpretation本文は読んでいない。

`ST-C-01` の4条件平均:

| Condition | Seeking | Negative |
|---|---:|---:|
| T00 | 1.0 | 0.0 |
| T01 | 1.0 | 2.5 |
| T10 | 3.0 | 0.0 |
| T11 | 2.5 | 1.5 |

加算予測に対する探索的interaction contrastは、Seeking **-0.50**、Negative **-1.00** だった。

これは1 stimulus × 2 replicatesをGate判定後に見つけたpost-hoc observationであり、一般的なS×N antagonistic interactionの証拠とは扱わない。独立したfollow-up pilotとして [PF-EXP-0002 — Opportunity × Danger Interaction](../PF-EXP-0002-opportunity-danger-interaction/) を設計する仮説生成にのみ使用する。

## Reproducibility

pilot-002の実行設定は [`experiment.yaml`](experiment.yaml) に保持する。raw results、blind set、blind key、private analysisはGit管理外。

再現手順:

```powershell
uv sync --frozen
uv run python -m src.validate
uv run python -m src.pilot --dry-run
uv run python -m src.pilot
uv run python -m src.blind
uv run python -m src.evaluate --dry-run
uv run python -m src.evaluate
uv run python -m src.analyze
```

## API / data policy

- `https://api.openai.com/v1` を明示
- `OPENAI_API_KEY` は環境変数から使用
- `store=false`
- raw response / blind files / private analysisはGitHubへ含めない
- 公開repositoryには設計、固定条件、集計、監査metadataのみを残す

## Next

PF-EXP-0001の事前Gateを事後変更してPASS扱いにはしない。ST-C-01で得られた探索的相互作用はPF-EXP-0002で新しいscenario familiesを使って独立に検証する。PF-EXP-0001 stimuliはconfirmatory datasetへ再利用しない。

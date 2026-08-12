# PF-EXP-0001 — Temperament → Interpretation

> Status: **pilot-002 ready to run**  
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

本実験ではこの最初の接続だけを検証する。Regulation、Response、History / Biography、Relationship、Audience / Resonanceは対象外とする。

## Experimental design

S / NをHigh / Lowにした2×2 factorial designを用いる。

| Condition | S | N |
|---|---|---|
| T00 | Low | Low |
| T01 | Low | High |
| T10 | High | Low |
| T11 | High | High |

Temperament操作文にはActionを含めない。「High Sなら近づく」「High Nなら逃げる」のようなResponse直接指定は禁止する。

Pilot stimuliは12件。

| Class | Count | Primary purpose |
|---|---:|---|
| Seeking-target | 3 | Sの主効果 |
| Negative-target | 3 | Nの主効果 |
| Conflict | 3 | S / Nのcoactivation |
| Neutral | 3 | 不要なcondition effect |

各runは `H0 = ∅` の独立contextとし、過去経験・価値観・Relationship等を与えない。

## Blind evaluation

CharacterはInterpretationだけを生成する。Seeking / Negativeの自己採点は行わせない。

生成後、condition / stimulus / stimulus class / hypothesisを隠したblind setを作り、別のEvaluatorが次の2軸を0–4で評価する。

- Seeking Activation
- Negative Activation

## Frozen hypotheses and gates

数値Gateはpilot response観測前に [`thresholds.yaml`](thresholds.yaml) へ固定済み。

| Gate | Frozen criterion |
|---|---|
| G1 | Seeking-targetのS High − S Low平均差 ≥ **0.75** |
| G2 | Negative-targetのN High − N Low平均差 ≥ **0.75** |
| G3 | 各cross-effect / 対応するmain effect ≤ **0.50** |
| G4 | ConflictのT11で両軸平均 ≥ **2.00**、かつ両軸2以上の割合 ≥ **0.67** |
| G5 | Neutralのcondition mean rangeが各軸 ≤ **0.75** |

Pilot結果を見た後にGateを変更しない。

## Pilot history

### pilot-001 — technical incomplete

pilot-001はgeneration 96件を開始したが、技術的に完了しなかった。

- planned: 96
- unique succeeded: 89
- missing: 7
- failed attempt records: 20
- failure type: JSONDecodeError
  - truncated JSON (`Unterminated string`): 16
  - empty/non-JSON start (`Expecting value`): 4
- generation `max_output_tokens`: 220
- blind evaluation: not started
- Gate analysis: not run
- confirmatory eligible: no

raw Interpretationは研究者が閲覧していない。失敗パターンからoutput token budget不足が主要因と推定したが、pilot-001 runnerは `response.status` / `incomplete_details.reason` を保存していなかったため、原因は**推定**として記録する。

pilot-001の実行設定は [`runs/pilot-001/executed-config.yaml`](runs/pilot-001/executed-config.yaml)、監査状態は [`runs/pilot-001/status.yaml`](runs/pilot-001/status.yaml) に保存する。ローカルのraw結果は削除せず保持する。

### pilot-002 — active

pilot-002は同じ研究条件・刺激・Gateを維持し、技術的出力上限だけを事前に修正して96件を最初から再実行する。

- generation `max_output_tokens`: **800**
- evaluation `max_output_tokens`: **400**
- generation runs: 96
- blind evaluation runs: 96
- randomization seed: `20260813`
- blind randomization seed: `2026081301`

`max_output_tokens` は上限であり、必ずそのtoken数を消費する意味ではない。

runnerは次回から以下を監査保存する。

- `response.status`
- `incomplete_details.reason`
- returned model / response ID / x-request-id
- usage / reasoning token details
- output text length on technical failure

これにより、max-token由来のincomplete responseをJSON parse errorと混同しない。

## Current execution config

Active configは [`experiment.yaml`](experiment.yaml) = **pilot-002**。

生成物はpilotごとに分離する。

```text
runs/
├─ pilot-001/   # technical incomplete; preserve locally
└─ pilot-002/   # active
```

raw results、blind set、blind key、private analysisはGit管理外。

## Execution — pilot-002

実験ディレクトリで実行する。

```powershell
uv sync --frozen
```

### 1. Static validation

```powershell
uv run python -m src.validate
```

期待結果：

```text
PASS: PF-EXP-0001 pilot-002 static validation
```

### 2. Generation dry-run

```powershell
uv run python -m src.pilot --dry-run
```

期待結果：

```text
manifest: ...\runs\pilot-002\manifest.jsonl (96 runs)
dry-run: no API requests sent
```

### 3. Generation run

ここからOpenAI APIを使用する。

```powershell
uv run python -m src.pilot
```

最後に必ずsummaryを表示する。

```text
generation summary:
  planned:   96
  succeeded: 96
  missing:   0
```

`missing > 0` の場合はblindへ進まない。

### 4. Create blind set

```powershell
uv run python -m src.blind
```

期待結果：

```text
blind set: 96 records
```

### 5. Evaluation dry-run

```powershell
uv run python -m src.evaluate --dry-run
```

### 6. Blind evaluation

```powershell
uv run python -m src.evaluate
```

最後に、

```text
evaluation summary:
  planned:   96
  succeeded: 96
  missing:   0
```

を確認する。

### 7. Gate analysis

```powershell
uv run python -m src.analyze
```

G1〜G5を自動判定する。全Gate passはexit code `0`、1つ以上failはexit code `2`。

## Validation / tests

```powershell
uv run pytest -q
uv run ruff check .
```

主な検証対象：

- manifestが96 runで均衡・決定論的
- `experiment.yaml` がpilot-002を指す
- output schemaがInterpretationのみ
- Windows CRLFでもthreshold hashが一致
- incomplete response理由を監査できる
- stale SDK routingを継承しない
- blind setにcondition / stimulus / hypothesisが混入しない
- synthetic patternでG1〜G5がpassする

## API / data policy

- API base URLは `https://api.openai.com/v1` を明示する。
- `OPENAI_API_KEY` を環境変数から使用する。
- Organization / Project routing metadataは継承しない。
- `store=false`。
- raw response、blind files、private analysisはGitHubへ含めない。
- 公開repositoryには設計、seed、checksum、集計、監査metadataだけを残す。

## Failure policy

技術エラーが出た場合、条件の一部だけを変更して穴埋めしない。

1. pilotをtechnical incompleteとして保存
2. 原因と変更点を記録
3. 次pilotとして96件すべてを同一条件で再実行

研究Gateを通らない場合は別であり、モデルをすぐ複雑化せず、Temperament操作文 → stimulus → generation instruction → evaluation rubricの順に検討する。

## Confirmatory boundary

pilot-002が技術的に完了しG1〜G5を評価できた後にのみ、別holdout stimuliによるconfirmatory studyを設計する。Pilot stimuliはconfirmatory datasetへ再利用しない。

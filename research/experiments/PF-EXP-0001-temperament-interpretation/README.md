# PF-EXP-0001 — Temperament → Interpretation

> Status: **Ready to run / pilot-001 frozen**  
> Research Track: **Personality Formation**  
> Canonical Framework: [APRL Research Framework v1.0](../../../docs/APRL_Research_Framework.md)  
> Canonical Model: [APRL Personality Formation Model v1.0](../../../docs/models/Personality_Formation_Model.md)

---

## 1. Purpose

APRL Personality Formation Model v1.0では、Temperamentを刺激に対する基礎的な motivational-emotional reactivity の初期条件として扱い、最小モデルを次の2次元で表す。

- **S = Seeking Reactivity**
- **N = Negative Affectivity**

TemperamentはResponseを直接決める行動規則ではなく、ExperienceのInterpretationからResponse形成へ確率的な偏りを与える初期条件である。

本実験では最初の接続だけを切り出して検証する。

```text
Temperament T0 = (S, N)
          │
          ▼
Experience ──► Interpretation
```

### Research Question

**同一のExperienceに対し、Seeking Reactivity（S）とNegative Affectivity（N）は、想定した方向へ独立かつ再現可能なInterpretationの偏りを生むか。**

---

## 2. Scope

### In scope

- `T0=(S,N)` のHigh / Low操作
- 同一Experienceに対するInterpretation
- Seeking Activationの盲検評価
- Negative Activationの盲検評価
- S / Nの同時活性化
- Neutral刺激における不要なcondition effect

### Out of scope

- History / Biography形成
- Relationship
- Regulationの個人差
- ResponseのAction / Intensity / Latencyの主要検証
- Creator / Communicator / Audience / Resonance

`H0 = ∅` とし、過去経験、信念、価値観、Relationship、Personality label等を与えない。

Regulationは条件間で操作しない。

---

## 3. Conditions

S / NをHigh / Lowにした2×2 factorial designとする。

| Condition | S | N |
|---|---|---|
| T00 | Low | Low |
| T01 | Low | High |
| T10 | High | Low |
| T11 | High | High |

操作文にはActionを含めない。

禁止例：

- High S = 「未知のものへすぐ近づく」
- High N = 「危険なら逃げる」

High / Lowはreactivityの活性化しやすさだけを操作し、特定の行動・判断・感情を必須にしない。

---

## 4. Pilot stimuli

Pilotでは12 Experienceを固定した。

| Class | Count | 主に検証するもの |
|---|---:|---|
| Seeking-target | 3 | Sの主効果 |
| Negative-target | 3 | Nの主効果 |
| Conflict | 3 | S / Nの同時活性化 |
| Neutral | 3 | 不要なcondition effect |

刺激本文は [`stimuli.yaml`](stimuli.yaml) に固定する。

各刺激は [`reviews/stimulus-review.yaml`](reviews/stimulus-review.yaml) の5観点で事前レビューし、10点中8点以上かつ0点項目なしをpilot実行条件とする。

---

## 5. Generation protocol

各runは独立した新規contextで実行する。

Characterへ与えるのは以下のみ。

1. 共通system instruction
2. Temperament condition
3. Experience
4. Interpretationのみを返すoutput instruction

Character自身にはSeeking / Negativeの数値評価をさせない。

生成outputは次だけを含む。

```json
{
  "interpretation": "..."
}
```

ResponseはPF-EXP-0002以降で扱う。

---

## 6. Blind evaluation

生成結果はcondition、stimulus ID、stimulus class、hypothesisを外したblind setへ変換する。

Blind EvaluatorはInterpretation本文だけを見て、次の2軸を独立に0〜4で評価する。

### Seeking Activation

- 0: 見られない
- 1: 弱く示唆される
- 2: 明確だが中程度
- 3: 強い
- 4: 非常に強く中心的

### Negative Activation

- 0: 見られない
- 1: 弱く示唆される
- 2: 明確だが中程度
- 3: 強い
- 4: 非常に強く中心的

同じInterpretationで両方が高くてもよい。

---

## 7. Hypotheses

### H1 — Seeking validity

Seeking-target Experienceで、S HighはS LowよりSeeking Activationが高い。

### H2 — Negative validity

Negative-target Experienceで、N HighはN LowよりNegative Activationが高い。

### H3 — Discriminant validity

S操作のNegative Activationへのcross-effect、およびN操作のSeeking Activationへのcross-effectは、それぞれ対応する主効果より十分小さい。

### H4 — Coactivation

Conflict ExperienceでT11はSeeking ActivationとNegative Activationを同時に示す。

### H5 — Neutrality

Neutral Experienceでは4条件間に大きなsystematic differenceが生じない。

---

## 8. Frozen pilot design

```text
4 Temperament conditions
× 12 Experiences
× 2 independent replicates
= 96 generation runs

+ 96 blind evaluation runs
```

各conditionは24 generation runs、各stimulusは8 generation runsとなる。

Pilotは測定設計・操作妥当性の確認用であり、confirmatory evidenceとして使用しない。

### Numeric gates

数値Gateはpilot responseを見る前に [`thresholds.yaml`](thresholds.yaml) へ固定した。

| Gate | Frozen criterion |
|---|---|
| G1 | Seeking-targetのS High − S Low平均差 ≥ **0.75** |
| G2 | Negative-targetのN High − N Low平均差 ≥ **0.75** |
| G3 | 各cross-effect / 対応するmain effect ≤ **0.50** |
| G4 | ConflictのT11で両軸平均 ≥ **2.00**、かつ両軸2以上の割合 ≥ **0.67** |
| G5 | Neutralのcondition mean rangeが各軸 ≤ **0.75** |

これらはpilot結果を見た後に都合よく変更しない。

---

## 9. Frozen manifest definition

96 runの順序・ID・prompt hash・stimulus hashは、committedされたprompt / condition / stimulusとrandomization seedから決定論的に生成する。

- Randomization seed: `20260813`
- Blind randomization seed: `2026081301`
- Expected Manifest SHA-256: `68eb99bd3f361033651a15453c4ef5b8d27c5b80b9d5b2ee3f8c3a336f6bbb8a`
- Thresholds SHA-256: `e88a6d29cb25ace271dede271efcb33ffa2606079f565013ad772c2177b39e08`

`src.pilot --dry-run` が `runs/pilot-001/manifest.jsonl` を生成する。`src.validate` は生成前でも決定論的manifestのhashを検証し、生成後は内容一致も検証する。

Runnerは同じpathに異なるmanifestを上書きしない。manifest本体はgenerated artifactとしてGit管理外とし、正本側には生成規則・seed・expected hashを固定する。

---

## 10. Execution

実験ディレクトリへ移動する。

```bash
cd research/experiments/PF-EXP-0001-temperament-interpretation
```

依存関係を同期する。

```bash
uv sync --frozen
```

### 10.1 Static validation

```bash
uv run python -m src.validate
```

期待結果：

```text
PASS: PF-EXP-0001 static validation
```

### 10.2 Generation dry-run

APIを呼ばず、frozen manifestとの一致を確認する。

```bash
uv run python -m src.pilot --dry-run
```

期待結果：

```text
manifest: .../runs/pilot-001/manifest.jsonl (96 runs)
dry-run: no API requests sent
```

### 10.3 Generation run

`OPENAI_API_KEY` が環境変数として設定されていることを確認して実行する。

```bash
uv run python -m src.pilot
```

成功済みrunは再実行時にskipされる。

raw resultは `runs/pilot-001/results.jsonl` に保存され、Git管理外となる。

### 10.4 Create blind set

96 generation runsがすべて成功した後に実行する。

```bash
uv run python -m src.blind
```

blind setと対応keyは `runs/pilot-001/private/` に生成され、Git管理外となる。

Blind EvaluatorにはInterpretation本文とblind IDだけを渡す。

### 10.5 Evaluation dry-run

```bash
uv run python -m src.evaluate --dry-run
```

### 10.6 Blind evaluation

```bash
uv run python -m src.evaluate
```

評価結果は `runs/pilot-001/evaluation-results.jsonl` へ保存する。condition情報は含まない。

### 10.7 Gate analysis

```bash
uv run python -m src.analyze
```

G1〜G5を自動計算し、private analysis JSONを生成する。

全Gate pass時はexit code `0`、1つ以上fail時はexit code `2` とする。

---

## 11. Validation and tests

```bash
uv run pytest -q
uv run ruff check .
```

テストでは少なくとも以下を確認する。

- manifestが96 runで固定・均衡している
- output schemaがInterpretationだけを含む
- stale `OPENAI_BASE_URL` / Organization / Project設定を継承しない
- blind setにcondition / stimulus / hypothesis情報が混入しない
- 明確なsynthetic patternでG1〜G5がpassする
- 刺激事前レビューとfrozen manifest/hashが一致する

---

## 12. API and data policy

- OpenAI clientは `https://api.openai.com/v1` を明示して初期化する。
- `OPENAI_API_KEY` を明示的に使用する。
- Organization / Project routing metadataは継承しない。
- `store=false` を固定する。
- HTTP error、API error、`x-request-id` を可能な範囲で監査記録する。
- raw response、blind set、blind key、private analysisはGitHubへ含めない。
- GitHubへ公開するのは設計、生成規則、seed、expected checksum、集計、監査metadataに限定する。

---

## 13. Failure handling

Gateを通らない場合、モデルをすぐ複雑化せず、次の順に疑う。

1. Temperament操作文
2. Experience stimulus
3. generation instruction
4. evaluation rubric

失敗結果も研究履歴として保持する。

---

## 14. Confirmatory boundary

Pilotを通過した場合のみ、pilotとは別のholdout stimuliでconfirmatory studyを設計する。

Confirmatory実行前には、hypotheses、condition definitions、prompt、rubric、holdout stimuli、exclusion/retry rules、model parameters、sample size、analysis plan、practical-effect / equivalence thresholdを改めて凍結する。

Pilot stimuliはconfirmatory datasetへ再利用しない。

---

## 15. Next experiment

PF-EXP-0001通過後は、次の接続を扱う。

```text
Interpretation → Regulation → Response
```

PF-EXP-0002ではTemperamentがResponseを直接指定しないことを維持したまま、Interpretation差がResponse形成へどのように接続するかを検証する。

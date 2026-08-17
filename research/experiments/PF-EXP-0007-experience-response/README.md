# PF-EXP-0007 — Experience → Response

> Status: **implementation ready / pilot-001 not run**  
> Canonical Model: [APRL Personality Formation Model v1.2](../../../docs/models/Personality_Formation_Model.md)  
> Target relation: `R_t = g(E_t, Sit_t)`  
> Isolated contribution: `E_t → R_t`

## Research Question

> **同一のSituationのもとで、Experienceの主観的意味の違いは、Responseを再現可能かつ方向整合的に変えるか。**

PF-EXP-0005 / 0006でExperienceへの上流入力を個別検証した後、その下流に位置する `Experience → Response` を単独操作で検証する。

詳細な設計原則と解釈境界は [`protocol.md`](protocol.md) を正とする。

## Frozen pilot-001 design

Situationを固定し、Experienceだけを次の2条件で操作する。

- **E-B — Benign / Low-risk Experience**
- **E-A — Adverse / High-risk Experience**

Experience packetは現在の出来事がCharacterにとって持つ主観的意味までに限定する。Action、意思決定、行動計画、Intensity / Latency、および `警戒する`、`身構える`、`距離を取りたい` 等のResponse tendency / behavioral readinessは含めない。

Response生成時に与えるのは次だけである。

1. current Situation
2. fixed Experience packet

Temperament、Perception、Values & Beliefs、Relationship、Historyは与えない。

## Situation bank

PF-EXP-0006で使用した8つのrelationship-generic Situationを再利用する。

- F01 案への見直し指摘
- F02 予定変更の申し出
- F03 作業中資料の共有依頼
- F04 遅れて届いた返答
- F05 異なる進め方の提案
- F06 作業の一部を引き受ける申し出
- F07 判断の再確認要求
- F08 話題の持ち越し

Situation自体がResponse方向をほぼ強制していないことをP5で確認する。

## Response

正本v1.2に従い、Responseは次で取得する。

`Response_t = (Action_t, Intensity_t, Latency_t)`

pilot-001のconfirmatory targetは **Actionの意味方向** のみとする。

- `constructive_engagement` 0–4
- `protective_distancing` 0–4

Intensity / Latencyはsecondary outcomeとして記録するが、blind evaluatorには提示しない。

## Pretest

合計24件。

- Experience quality: `8 families × 2 conditions = 16`
- Situation affordance boundary: `8 families = 8`

Gates:

- **P1 Experience separation**
  - Benign separation `>= 2.0`
  - Adverse separation `>= 2.0`
  - correct family direction `>= 7 / 8`
- **P2 No Response-tendency preload**
  - mean `<= 0.50`, max `<= 1`
- **P3 No external-fact leakage**
  - mean `<= 0.50`, max `<= 1`
- **P4 Upstream-state isolation**
  - Values & Beliefs / Relationship / Temperament preloadを個別監査
  - 各 mean `<= 0.50`, max `<= 1`
- **P5 Situation affordance boundary**
  - response-direction constraint mean `<= 0.50`, max `<= 1`

**P1〜P5のいずれかがFAILした場合、main generationへ進まない。**

## Main

- 8 scenario families
- 2 Experience conditions
- 3 replicates
- generation: `48 Responses`
- blind evaluation: `48 Actions`

Blind evaluatorが見るのは **fixed Situation + generated Action only**。Experience condition、Experience packet、Intensity、Latency、pair identity、generation orderはblind化する。

Confirmatory gates:

- **G1** `Delta_C >= 0.75`
- **G2** `Delta_P >= 0.75`
- **G3** 8 family中6以上でdual-positive
- **G4** 全leave-one-family-outで両effect `> 0`
- **G5 Response boundary quality**
  - `action_validity_failure` mean `<= 0.50`, max `<= 1`
  - `external_fact_invention` mean `<= 0.50`, max `<= 1`

**Overall PASSはG1〜G5の全PASSとする。**

## Implementation

主要ファイル:

- `experiment.yaml` — model、seed、run path、replicate設定
- `stimuli.yaml` — E-B / E-A packetと8 Situation
- `thresholds.yaml` — pretest / main Gateの数値固定
- `output.schema.json` — Action / Intensity / Latency
- `evaluation.schema.json` — blind Action評価
- `pretest.schema.json` — P1〜P5評価
- `prompts/` — generation / pretest / blind evaluation prompt
- `src/` — manifest、API実行、blind化、分析、freeze監査
- `tests/` — design / schema static tests

Main runnerはpretest PASSとdesign hash一致の両方を確認し、不一致なら実行を拒否する。Raw responses、blind key、gate出力等は `runs/` 以下に保存し、Git管理しない。

## Execution order

Windows PowerShell等でこのディレクトリへ移動後、次の順で実行する。

```text
python -m src.validate
pytest -q
python -m src.pretest
python -m src.pretest_analyze
```

P1〜P5がすべてPASSした場合のみ続ける。

```text
python -m src.pilot
python -m src.blind
python -m src.evaluate
python -m src.analyze
```

APIを呼ばずmanifestだけ確認する場合は `src.pretest` / `src.pilot` / `src.evaluate` に `--dry-run` を付ける。

## Static validation before pilot

実装作成時に以下を確認済み。

- `python -m compileall -q src`: PASS
- `python -m src.validate`: PASS
  - families = 8
  - pretest = 24（Experience 16 / Situation 8）
  - main generation = 48
  - blind evaluation = 48
- `pytest -q`: **6 passed**

これはAPI pretest / mainの結果ではない。

## Interpretation boundary

PASSした場合に直接支持するのは、固定されたSituationのもとで、Benign / Low-risk と Adverse / High-risk というExperienceの主観的意味差がResponseのAction意味を方向整合的に変え得る、という限定された `E_t → R_t` の寄与である。

本実験だけでは、ExperienceがResponseの唯一の原因であること、`Situation → Response` が不要であること、PF-EXP-0005 / 0006からResponseまでの媒介経路全体、人間への一般化、独立Evaluatorでの再現を主張しない。

## Audit policy

- Gate / threshold / stimulus / prompt / schema / seedはAPI実行前に固定する
- pretest開始後に同pilotのdesignを変更しない
- pretest FAIL時はmainを実行しない
- 実行後にGateを緩和しない
- secondary analysisをconfirmatory resultへ昇格しない
- Raw responsesは公開しない
- PF-EXP-0001〜0006の実行済み記録を変更しない

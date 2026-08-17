# PF-EXP-0007 — Experience → Response

> Status: **plan ready / implementation not started**  
> Canonical Model: [APRL Personality Formation Model v1.2](../../../docs/models/Personality_Formation_Model.md)  
> Target relation: `R_t = g(E_t, Sit_t)`  
> Isolated contribution: `E_t → R_t`

## Research Question

> **同一のSituationのもとで、Experienceの主観的意味の違いは、Responseを再現可能かつ方向整合的に変えるか。**

PF-EXP-0005では `Values & Beliefs → Experience`、PF-EXP-0006ではRelationship内のTrust状態による `Relationship → Experience` の条件付き寄与が支持された。

PF-EXP-0007では、その下流に位置する `Experience → Response` を単独操作で検証する。

## pilot-001 scope

Situationを固定し、Experienceの意味だけを2条件で操作する。

- **E-B — Benign / Low-risk Experience**: 現在の出来事を、主観的に悪意・脅威・不利益の可能性が低い意味として経験している状態
- **E-A — Adverse / High-risk Experience**: 同じ出来事を、主観的に悪意・脅威・不利益の可能性が高い意味として経験している状態

このcontrastはExperience全体の普遍的分類を定義するものではない。pilot-001で `E_t → R_t` を検出できるかを見るための最小操作である。

Experience packetにはAction、意思決定、行動計画、ResponseのIntensity / Latencyに加え、`警戒する`、`身構える`、`距離を取りたい`、`関わり続けたい`等の**Response tendency / behavioral readiness**を含めない。Experienceは、現在の出来事がCharacterにとって持つ主観的意味までに限定する。

Response生成時には、Temperament、Perception、Values & Beliefs、Relationshipを入力しない。これら上流状態の効果を再検証するのではなく、既知のExperience状態を与えたときのResponse差を検証するためである。

## Situation bank policy

PF-EXP-0006の8つのrelationship-generic Situationを候補bankとして優先的に再利用する。

ただし再利用自体を目的にはしない。各Situationは、Experienceを与えない状態でConstructive Engagement / Protective Distancingのどちらか一方を外部条件だけでほぼ強制していないことをpretestする。

実装前レビューでResponse選択余地が不十分なfamilyがあれば、pilot-001のAPI実行前に置換する。pilot-001のstimuliをfreezeしてpretestを開始した後は、同pilot内で変更しない。

## Response definition

正本v1.2に従い、ResponseはCharacterが選択・開始する反応として扱う。

`Response_t = (Action_t, Intensity_t, Latency_t)`

pilot-001のconfirmatory targetは **Actionの意味方向** とする。

主要評価軸：

- `constructive_engagement` 0–4
  - 対話、確認、協力、接近、関与継続等へ向かう程度
- `protective_distancing` 0–4
  - 距離確保、保留、拒否、情報制限、回避、防御等へ向かう程度

両軸は単一尺度の両極とは仮定しない。「警戒しながら質問する」のようなResponseでは、Actionとして両方向が一定程度共存し得る。

Intensity / Latencyは記録するが、pilot-001では方向を事前仮定せずsecondary analysisとする。blind evaluatorには提示しない。

## Confirmatory Hypothesis

### H-ER01 — Experience meaning effect on Response

Situationを固定したとき、

- E-BはE-AよりConstructive Engagementを高める
- E-AはE-BよりProtective Distancingを高める

主要効果量：

`Delta_C = mean(C_E-B) - mean(C_E-A)`

`Delta_P = mean(P_E-A) - mean(P_E-B)`

## Sample size

- 8 scenario families
- 2 Experience conditions
- 3 replicates per cell

Main generation:

`8 × 2 × 3 = 48 Responses`

Blind evaluation:

`48 Actions`

Pretestは測定対象を分離する。

- Experience quality: `8 × 2 = 16`
- Situation affordance boundary: `8`
- total: `24`

予定最小API評価単位は **24 + 48 + 48 = 120**。

## Planned pretest gates

数値は実装PRでmachine-readableなthresholdとして固定し、pilot-001のAPI実行後には変更しない。

- **P1 Experience separation**
  - Benign meaning separation `>= 2.0`
  - Adverse meaning separation `>= 2.0`
  - correct family direction `>= 7 / 8`
- **P2 No Response-tendency preload**
  - Action、意思決定、行動計画、Intensity / Latencyだけでなく、Response方向を先取りするbehavioral readinessも評価対象とする
  - mean `<= 0.50`, max `<= 1`
- **P3 No external-fact leakage**
  - mean `<= 0.50`, max `<= 1`
- **P4 Upstream-state isolation**
  - Values & Beliefs preload mean `<= 0.50`, max `<= 1`
  - Relationship preload mean `<= 0.50`, max `<= 1`
  - Temperament preload mean `<= 0.50`, max `<= 1`
- **P5 Situation affordance boundary**
  - response-direction constraint mean `<= 0.50`, max `<= 1`

P1〜P4はSituation + Experience packetを評価する。P5はSituationだけを提示し、Experienceを与えない。

**P1〜P5のどれかがFAILした場合、main generationへ進まない。**

## Planned confirmatory gates

- **G1 Constructive Engagement effect**: `Delta_C >= 0.75`
- **G2 Protective Distancing effect**: `Delta_P >= 0.75`
- **G3 Family generalization**: 8 family中6以上で両effect `> 0`
- **G4 Leave-one-family-out robustness**: 全LOOで両effect `> 0`
- **G5 Response boundary quality**
  - `action_validity_failure` mean `<= 0.50`, max `<= 1`
  - `external_fact_invention` mean `<= 0.50`, max `<= 1`

`action_validity_failure` は、Action欄が具体的なResponseとして成立せず、Situation / Experienceの解釈説明や言い換えだけになっている程度を測る。Intensity / LatencyはこのGateの対象に含めない。

**Overall PASSはG1〜G5の全PASSとする。**

## Blind evaluation

Evaluatorには次だけを与える。

1. fixed Situation
2. generated **Action only**

Experience condition、Experience packet、Intensity、Latency、family内pair identity、generation orderはblind化する。

主要評価軸は `constructive_engagement` / `protective_distancing` とし、Actionのboundary qualityを別尺度で監査する。Intensity / Latencyを隠すことで、confirmatory targetでない強度・潜時がAction意味評価へ混入することを避ける。

## Interpretation boundary

PASSした場合に支持するのは、

> **固定されたSituationのもとで、Benign / Low-risk と Adverse / High-risk というExperienceの主観的意味の違いが、ResponseのAction意味を再現可能かつ方向整合的に変え得る。**

という限定された主張である。

本実験だけでは次を主張しない。

- ExperienceがResponseを完全に決定する
- `Situation → Response` の直接寄与が不要である
- PF-EXP-0005 / 0006の上流操作からResponseまでの媒介経路全体が検証済みである
- Benign / Adverse以外のExperience次元へ一般化できる
- Intensity / Latencyの方向効果が確立した
- 人間へ一般化できる
- 独立Evaluatorまたは人手評価でも再現する

## Audit policy

- Gate / threshold / stimulus / prompt / schemaをAPI実行前に固定する
- pretest FAIL時はmainへ進まない
- FAIL後に同pilotのGateを緩和しない
- Raw responsesは公開しない
- blind keyはevaluation完了までanalysisから分離する
- secondary analysisをconfirmatory resultへ昇格しない
- PF-EXP-0001〜0006の実行済み記録を変更しない

詳細な設計ルールは [`protocol.md`](protocol.md) を参照する。

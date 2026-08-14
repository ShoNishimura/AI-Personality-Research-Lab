# PF-EXP-0005 — Values & Beliefs → Experience

> Status: **implementation ready / pretest not run**  
> Canonical Model: [APRL Personality Formation Model v1.2](../../../docs/models/Personality_Formation_Model.md)  
> Target relation: `E_t = h(P_t, VB_t, Rel_t)`  
> Isolated contribution: `VB_t → E_t`

## Research Question

> **同一のSituationとPerception、同一のRelationshipのもとで、Values & Beliefsの違いは、その出来事がCharacterにとって持つExperienceの意味を再現可能かつ方向整合的に変えるか。**

Personality Formation Model v1.2では、PerceptionとExperienceを分離し、

```text
Situation → Perception → Experience
                         ▲
                 Values & Beliefs
                 Relationship
```

と整理した。

PF-EXP-0001〜0003は、SituationとTemperamentによるPerception側の偏りに経験的支持を与えた一方、実行時の`Interpretation`はv1.2でPerception / Experienceを分離する以前の概念であり、**両者の境界そのものは直接検証していない**。

PF-EXP-0005は、v1.2で新たに独立させたExperienceを最初に検証する実験とする。

## Confirmatory Hypothesis

### H-VB01 — Values & Beliefs effect on Experience

Situation、Perception、Relationshipを固定したとき、**Values & Beliefsの違いは、生成されるExperienceの意味を対応する方向へ変化させる。**

pilot-001では一つのValues & Beliefs contrastに絞る。

- **VB-L: Learning / Improvement orientation**  
  誤り、指摘、不十分さ等を、学習・修正・能力向上に利用できる情報として捉えやすいValues & Beliefs
- **VB-E: Evaluation / Competence-protection orientation**  
  能力不足を示さないこと、評価を損なわないことを重視し、明確な失敗・指摘・不足を自己評価上の重要な出来事として捉えやすいValues & Beliefs

主要評価軸をblind evaluatorによる次の2軸とする。

- `learning_improvement_meaning` 0–4
- `evaluation_threat_meaning` 0–4

主要効果量は、

$$
\Delta L = \overline{L}_{VB-L} - \overline{L}_{VB-E}
$$

$$
\Delta E = \overline{E}_{VB-E} - \overline{E}_{VB-L}
$$

とする。

H-VB01は `ΔL > 0` かつ `ΔE > 0` を予測する。

一方の意味が高まると他方が必ず低下するとは仮定しない。PF-EXP-0001〜0003で複数のsalienceが共存し得たことを踏まえ、2軸を独立に評価する。

## Why Values & Beliefs first

現行モデルは、

$$
E_t=h(P_t,VB_t,Rel_t)
$$

とする。

Values & BeliefsとRelationshipを同時に操作すると、Experience差の原因を切り分けにくい。そこでPF-EXP-0005では、

- Situation：固定
- Perception：固定
- Values & Beliefs：操作
- Relationship：`none / neutral` に固定
- Temperament：Experience生成時には与えない

とし、まず `VB → Experience` の寄与だけを検証する。

Relationshipの独立効果は後続実験候補とする。

## Experimental Design

### Fixed Situation and Perception

各scenario familyについて、現在のSituationとPerception packetを1つ固定する。

Perceptionは生成し直さず、Experience generatorへ既知の状態として直接与える。これにより本実験は、自然な全過程の再現ではなく、**固定されたPerceptionに条件づけたExperience形成の検証**として扱う。

Perception packetは、何がsalientか、どのようなmotivational-emotional significanceとして感じ取られているかまでを記述するが、次を含めない。

- 学習機会としての意味づけ
- 自己評価・能力評価への脅威としての意味づけ
- 現在のResponse、意思決定、行動計画
- Values & Beliefs自体の言い換え

### Values & Beliefs manipulation

VB-L / VB-Eは、現在Situationに固有の事実や現在行動への指示を含めず、**一般化された現在の内的状態**として記述する。

条件間で、能力、知識、資源、身体状態、Relationship、現在の外的制約は変えない。

pilot-001では内部妥当性を優先し、Values & Beliefs contrastはLearning / Improvement vs Evaluation / Competence-protectionの一組に限定する。別のValues & Beliefs次元への一般化は後続実験で扱う。

### Relationship control

Relationshipは全条件で `none / neutral` とする。

特定人物との信頼、親密さ、敵対、義務、愛着等がExperienceの意味を左右しやすい継続的人間関係を避ける。

## Scenario families and sample size

- **8 independent scenario families**
- 2 Values & Beliefs conditions: VB-L / VB-E
- 3 replicates per cell

Main generation:

`8 families × 2 VB conditions × 3 replicates = 48 Experiences`

Blind evaluation:

`48 Experiences`

Manipulation / boundary pretest:

`8 families × 2 VB conditions = 16 packets`

予定される最小API評価単位は、pretest 16 + generation 48 + blind evaluation 48 = **112**。

scenario familyは、批評、失敗、知識不足、成果不足、修正要求、不確実な課題等、Learning / Evaluation双方の意味が成立し得る状況へ分散する。ただし、各family内ではSituationとPerceptionを完全同一とする。

## Experience representation

生成対象はExperienceのみとする。

Experienceは、

> **PerceptionされたSituationが、そのCharacterにとってどのような意味を持つ経験となったか**

を1〜3文程度で記述する。

生成物に次を含めない。

- Action
- 意思決定
- 行動計画
- ResponseのIntensity / Latency
- Characterの固定trait label
- 現在Situationに存在しない新規外部事実

## Blind evaluation

blind evaluatorにはValues & Beliefs condition（VB-L / VB-E）を見せない。

Evaluatorには、

1. current Situation
2. fixed Perception
3. generated Experience

のみを提示する。

主要評価軸：

- `learning_improvement_meaning` 0–4：出来事が学習、修正、改善、能力向上につながる経験として意味づけられている程度
- `evaluation_threat_meaning` 0–4：出来事が能力不足、自己評価、他者評価、立場の毀損等に関わる脅威として意味づけられている程度

品質評価：

- `response_leakage` 0–4：Action、意思決定、行動計画等のResponse内容が混入している程度

## Frozen gates

Gateの数値は [`thresholds.yaml`](thresholds.yaml) を正とする。

### Pretest

- **P1 VB separation**：VB-L / VB-EがLearning / Evaluationの両軸で十分に分離する
- **P2 No current-response directiveness**：Values & Beliefsが現在のResponseを直接指示しない
- **P3 No current-situation leakage**：Values & Beliefsが現在Situation固有の事実を含まない
- **P4 Perception boundary**：固定PerceptionがLearning / EvaluationのExperience-level meaningを先取りしていない
- **P5 Relationship neutrality**：継続的なRelationship差がExperienceを左右する要素として顕在化していない

PretestがFAILした場合、main Experience generationへ進まない。

### Main confirmatory gates

- **G1 Learning meaning effect**：`mean(L_VB-L) - mean(L_VB-E) >= 0.75`
- **G2 Evaluation-threat meaning effect**：`mean(E_VB-E) - mean(E_VB-L) >= 0.75`
- **G3 Family generalization**：8 family中6以上で `ΔL_f > 0` かつ `ΔE_f > 0`
- **G4 Leave-one-family-out robustness**：全LOOで `ΔL > 0` かつ `ΔE > 0`
- **G5 Experience boundary quality**：Response leakageが事前閾値以下

**Overall PASSはG1–G5をすべて満たすこと**とする。

## Interpretation boundary

PASSした場合に支持するのは、

> **固定されたSituation・Perception・neutral Relationshipのもとで、Values & Beliefsの違いがExperienceの意味を再現可能かつ方向整合的に変え得る。**

という限定された主張である。

これは、同じPerceptionから異なるExperienceが形成され得ることを示すため、v1.2でPerceptionとExperienceを機能的に分離したことへの経験的支持にもなる。

ただし、以下は本実験だけでは主張しない。

- Values & Beliefsが自然なPerception形成へ影響しないこと
- Relationshipの効果
- `Experience → Response` の効果
- Values & Beliefsが過去Episodeから自然に形成・更新されること
- Learning / Evaluation以外のValues & Beliefs次元への一般化
- 実世界の人間に同じ効果量が成立すること

FAILした場合も直ちにPerception / Experienceの分離や `VB → Experience` を否定しない。Values & Beliefs操作、Perception固定法、Experience生成境界、評価尺度、scenario依存性を切り分ける。

## Audit policy

- Gate、threshold、stimulus、prompt、schemaはmain generation前に固定する
- Pretest FAIL時はmain generationへ進まない
- Raw responsesは公開しない現行方針を維持する
- Blind keyは評価完了までanalysisから分離する
- Gate判定後の探索分析はconfirmatory resultと分離して記録する
- Gate未達後に同pilotの閾値を緩和しない
- 実行済みPF-EXP-0001〜0004の監査記録は変更しない

## Implementation status

pilot-001の実行系を実装済みである。

- 8 scenario families
- VB-L / VB-Eを共通の一般化されたValues & Beliefs packetとして操作
- pretest 16件、main generation 48件、blind evaluation 48件の決定的manifest
- Experience-only generator
- manipulation / boundary pretest
- blind evaluator
- confirmatory analyzer（G1〜G5）
- design hash固定とpretest PASS後のhash一致チェック
- static validationとtests

main generationは、pretestがP1〜P5をすべてPASSし、pretest時のdesign hashとmain実行時のdesign hashが一致した場合にのみ開始できる。

現時点では**pretest未実行**であり、main generationも実行していない。

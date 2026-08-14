# PF-EXP-0005 — Values & Beliefs → Experience

> Status: **pilot-001 pretest FAIL / main not run; pilot-002 implementation ready / pretest not run**  
> Canonical Model: [APRL Personality Formation Model v1.2](../../../docs/models/Personality_Formation_Model.md)  
> Target relation: `E_t = h(P_t, VB_t, Rel_t)`  
> Isolated contribution: `VB_t → E_t`

## Research Question

> **同一のSituationとPerception、同一のRelationshipのもとで、Values & Beliefsの違いは、その出来事がCharacterにとって持つExperienceの意味を再現可能かつ方向整合的に変えるか。**

Personality Formation Model v1.2では、

```text
Situation → Perception → Experience
                         ▲
                 Values & Beliefs
                 Relationship
```

と整理する。

PF-EXP-0001〜0003はSituationとTemperamentによるPerception側の偏りに経験的支持を与えた一方、実行時の `Interpretation` はv1.2でPerception / Experienceを分離する以前の概念であり、両者の境界そのものは直接検証していない。

PF-EXP-0005は、v1.2で独立させたExperienceを検証する最初の実験である。

## Confirmatory Hypothesis

### H-VB01 — Values & Beliefs effect on Experience

Situation、Perception、Relationshipを固定したとき、**Values & Beliefsの違いは、生成されるExperienceの意味を対応する方向へ変化させる。**

pilot系列では一つのValues & Beliefs contrastに絞る。

- **VB-L: Learning / Improvement orientation**  
  誤り、不十分さ等を、学習・発達に関わる情報として捉えるValues & Beliefs
- **VB-E: Evaluation / Competence-protection orientation**  
  能力が十分であると評価される状態や、評価・立場・能力の確かさを重視するValues & Beliefs

主要評価軸はblind evaluatorによる次の2軸とする。

- `learning_improvement_meaning` 0–4
- `evaluation_threat_meaning` 0–4

主要効果量：

$$
\Delta L = \overline{L}_{VB-L} - \overline{L}_{VB-E}
$$

$$
\Delta E = \overline{E}_{VB-E} - \overline{E}_{VB-L}
$$

H-VB01は `ΔL > 0` かつ `ΔE > 0` を予測する。一方の意味が高まると他方が必ず低下するとは仮定しない。

## Experimental Design

### Fixed Situation and Perception

各scenario familyについてSituationとPerception packetを固定する。

Perceptionは生成し直さず、Experience generatorへ既知の状態として直接与える。Perception packetは、何がsalientか、どのようなmotivational-emotional significanceとして感じ取られているかまでを記述するが、次を含めない。

- 学習・改善にとって何を意味するか
- 自己評価・能力評価にとって何を意味するか
- 現在のResponse、意思決定、行動計画
- Values & Beliefs自体の言い換え

### Values & Beliefs manipulation

VB-L / VB-Eは、現在Situationに固有の事実や現在行動への指示を含めず、**一般化された現在の内的状態**として記述する。

条件間で、能力、知識、資源、身体状態、Relationship、現在の外的制約は変えない。

### Relationship control

Relationshipは全条件で `none / neutral` とする。

## Scenario families and sample size

- **8 independent scenario families**
- 2 Values & Beliefs conditions: VB-L / VB-E
- 3 replicates per cell

Main generation:

`8 families × 2 VB conditions × 3 replicates = 48 Experiences`

Blind evaluation:

`48 Experiences`

pilot-002 pretestは、測定対象を交絡させないため2種類に分離する。

- **VB quality pretest**: `8 families × 2 VB conditions = 16`
- **Perception boundary pretest**: `8 families = 8`

合計pretestは **24**。pilot-002の予定最小API評価単位は、24 + 48 + 48 = **120**。

## Experience representation

生成対象はExperienceのみとする。

> **PerceptionされたSituationが、そのCharacterにとってどのような意味を持つ経験となったか**

を1〜3文程度で記述する。

生成物にAction、意思決定、行動計画、ResponseのIntensity / Latency、固定trait label、現在Situationに存在しない新規外部事実を含めない。

## Blind evaluation

blind evaluatorにはVB conditionを見せず、current Situation、fixed Perception、generated Experienceのみを提示する。

主要評価軸：

- `learning_improvement_meaning` 0–4
- `evaluation_threat_meaning` 0–4

品質評価：

- `response_leakage` 0–4

## Frozen gates

Gateの数値は [`thresholds.yaml`](thresholds.yaml) を正とする。**pilot-001 FAIL後も閾値は変更しない。**

### Pretest

- **P1 VB separation**
- **P2 No current-response directiveness**
- **P3 No current-situation leakage**
- **P4 Perception boundary**
- **P5 Relationship neutrality**

pilot-002では、P1〜P3をVB quality pretestで、P4〜P5をPerception boundary pretestで評価する。P4評価時にはValues & Beliefsを提示しない。

PretestがFAILした場合、main Experience generationへ進まない。

### Main confirmatory gates

- **G1 Learning meaning effect**：`mean(L_VB-L) - mean(L_VB-E) >= 0.75`
- **G2 Evaluation-threat meaning effect**：`mean(E_VB-E) - mean(E_VB-L) >= 0.75`
- **G3 Family generalization**：8 family中6以上で `ΔL_f > 0` かつ `ΔE_f > 0`
- **G4 Leave-one-family-out robustness**：全LOOで `ΔL > 0` かつ `ΔE > 0`
- **G5 Experience boundary quality**：Response leakageが事前閾値以下

**Overall PASSはG1〜G5をすべて満たすこと**とする。

## Pilot history

### pilot-001 — pretest FAIL / main not run

pretestは16 / 16 succeeded。結果は次のとおり。

- P1 VB separation: **PASS**
  - Learning separation: 3.125
  - Evaluation-protection separation: 4.0
  - family direction: 8/8
- P2 No current-response directiveness: **FAIL**
  - mean 0.5625 / threshold <= 0.50
  - max 1.0 / threshold <= 1
- P3 No current-situation leakage: **PASS**
  - mean 0.0 / max 0.0
- P4 Perception boundary: **FAIL**
  - mean 0.625 / threshold <= 0.50
  - max 2.0 / threshold <= 1
- P5 Relationship neutrality: **PASS**
  - mean 0.0 / max 0.0

事前プロトコルどおり、main generationは実行していない。したがってH-VB01はpilot-001では未検証であり、支持・棄却の対象になっていない。

詳細は [`reports/pilot-001-summary.md`](reports/pilot-001-summary.md) に記録する。

### pilot-002 — boundary-isolated pretest

pilot-001の監査結果を受け、次を変更する。

- P1〜P3とP4〜P5のpretestを別API評価へ分離
- P4評価時にValues & Beliefsを提示しない
- VB packetから現在Responseを想起させやすい行動表現を弱める
- F03 / F06のPerceptionを、Experience-level meaningを先取りしにくい表現へ修正
- Gateとthresholdは変更しない
- phase / run path / randomization seedをpilot-002として分離

## Interpretation boundary

PASSした場合に支持するのは、

> **固定されたSituation・Perception・neutral Relationshipのもとで、Values & Beliefsの違いがExperienceの意味を再現可能かつ方向整合的に変え得る。**

という限定された主張である。

同じPerceptionから異なるExperienceが得られるため、PerceptionとExperienceを機能的に分けるv1.2の境界への支持にもなる。

ただし、Relationship効果、`Experience → Response`、VBの自然な形成・更新、他のVB次元、人間への一般化は本実験だけでは主張しない。

FAILした場合も、直ちに `VB → Experience` またはPerception / Experience分離を否定しない。操作強度、境界、評価方法、scenario依存性を切り分ける。

## Audit policy

- Gate、threshold、stimulus、prompt、schemaはmain generation前に固定する
- Pretest FAIL時はmain generationへ進まない
- Raw responsesは公開しない
- Blind keyは評価完了までanalysisから分離する
- Gate判定後の探索分析はconfirmatory resultと分離する
- Gate未達後に同pilotの閾値を緩和しない
- 実行済みPF-EXP-0001〜0004の監査記録は変更しない
- pilot-001の結果はpilot-002の事後的再判定に使用しない

## Implementation status

pilot-002の実行系を準備する。

- 8 scenario families
- VB-L / VB-E
- split pretest 24件
- main generation 48件
- blind evaluation 48件
- design hash固定
- pretest PASS後のhash一致チェック
- static validation / tests

pilot-002 pretestは未実行である。

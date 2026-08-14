# PF-EXP-0005 — Values & Beliefs → Experience

> Status: **pilot-001 pretest FAIL / main not run; pilot-002 completed / overall PASS**  
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

合計pretestは **24**。pilot-002の最小API評価単位は、24 + 48 + 48 = **120**。

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

Gateの数値は [`thresholds.yaml`](thresholds.yaml) を正とする。**pilot-001 FAIL後も閾値は変更していない。**

### Pretest

- **P1 VB separation**
- **P2 No current-response directiveness**
- **P3 No current-situation leakage**
- **P4 Perception boundary**
- **P5 Relationship neutrality**

pilot-002では、P1〜P3をVB quality pretestで、P4〜P5をPerception boundary pretestで評価した。P4評価時にはValues & Beliefsを提示していない。

### Main confirmatory gates

- **G1 Learning meaning effect**：`mean(L_VB-L) - mean(L_VB-E) >= 0.75`
- **G2 Evaluation-threat meaning effect**：`mean(E_VB-E) - mean(E_VB-L) >= 0.75`
- **G3 Family generalization**：8 family中6以上で `ΔL_f > 0` かつ `ΔE_f > 0`
- **G4 Leave-one-family-out robustness**：全LOOで `ΔL > 0` かつ `ΔE > 0`
- **G5 Experience boundary quality**：Response leakageが事前閾値以下

**Overall PASSはG1〜G5をすべて満たすこと**とした。

## Pilot history

### pilot-001 — pretest FAIL / main not run

pretestは16 / 16 succeeded。

- P1 VB separation: **PASS**
- P2 No current-response directiveness: **FAIL**
- P3 No current-situation leakage: **PASS**
- P4 Perception boundary: **FAIL**
- P5 Relationship neutrality: **PASS**

事前プロトコルどおりmain generationは実行しておらず、H-VB01はpilot-001では未検証である。

詳細は [`reports/pilot-001-summary.md`](reports/pilot-001-summary.md) に記録する。

### pilot-002 — completed / overall PASS

pilot-001の監査結果を受け、P1〜P3とP4〜P5のpretestを別API評価へ分離し、P4評価時にValues & Beliefsを提示しない設計へ変更した。Gateとthresholdは変更していない。

Pretestは24 / 24 succeeded、P1〜P5をすべてPASSした。

Main generation 48 / 48、blind evaluation 48 / 48を完了し、G1〜G5をすべてPASSした。

主要結果：

- `Δ Learning meaning = 3.5417`（threshold >= 0.75）
- `Δ Evaluation threat = 2.5833`（threshold >= 0.75）
- family generalization: **8 / 8 dual-positive**（threshold >= 6 / 8）
- min leave-one-family-out: `ΔL = 3.4762`, `ΔE = 2.4286`（both > 0）
- response leakage: mean `0.0417`, max `1.0`（threshold mean <= 0.50, max <= 1）

したがって、今回の実験条件ではH-VB01を支持する。

詳細は [`reports/pilot-002-summary.md`](reports/pilot-002-summary.md) に記録する。

## Interpretation boundary

pilot-002が直接支持するのは、

> **固定されたSituation・Perception・neutral Relationshipのもとで、Values & Beliefsの違いがExperienceの意味を再現可能かつ方向整合的に変え得る。**

という限定された主張である。

同じPerceptionを固定したままValues & Beliefsのみを変えてExperience差が生じたため、PerceptionとExperienceを機能的に分けるv1.2の境界にも限定的な経験的支持を与える。

ただし、Relationship効果、`Experience → Response`、VBの自然な形成・更新、他のVB次元、人間への一般化は本実験だけでは主張しない。またgenerationとblind evaluationの双方に`gpt-5.6`を用いているため、独立Evaluatorまたは人手評価による堅牢性確認は未実施である。

## Audit policy

- Gate、threshold、stimulus、prompt、schemaはmain generation前に固定した
- pilot-001の結果はpilot-002の事後的再判定に使用しない
- Raw responsesは公開しない
- Gate判定後の探索分析はconfirmatory resultと分離する
- 実行済みPF-EXP-0001〜0004の監査記録は変更しない

## Implementation status

pilot-002は完了した。

- pretest 24 / 24 succeeded
- main generation 48 / 48 succeeded
- blind evaluation 48 / 48 succeeded
- P1〜P5: all PASS
- G1〜G5: all PASS
- **overall PASS**

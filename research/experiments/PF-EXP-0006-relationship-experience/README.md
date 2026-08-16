# PF-EXP-0006 — Relationship → Experience

> Status: **plan ready / implementation not started**  
> Canonical Model: [APRL Personality Formation Model v1.2](../../../docs/models/Personality_Formation_Model.md)  
> Target relation: `E_t = h(P_t, VB_t, Rel_t)`  
> Isolated contribution: `Rel_t → E_t`

## Research Question

> **同一のSituationとPerception、同一のValues & Beliefsのもとで、Relationshipの違いは、その出来事がCharacterにとって持つExperienceの意味を再現可能かつ方向整合的に変えるか。**

PF-EXP-0005 pilot-002では、Situation・Perception・Relationshipを固定し、Values & Beliefsだけを操作することで `VB_t → E_t` の条件付き寄与を支持した。

PF-EXP-0006では、同じ式

$$
E_t = h(P_t, VB_t, Rel_t)
$$

のもう一つの未検証入力であるRelationshipを単独で操作する。

## Confirmatory Hypothesis

### H-REL01 — Relationship effect on Experience

Situation、Perception、Values & Beliefsを固定したとき、**Relationshipの信頼状態の違いは、生成されるExperienceの意味を対応する方向へ変化させる。**

pilot-001ではRelationshipの多次元性を一度に扱わず、**Trust** 一軸だけを操作する。

- **REL-T: Trusting Relationship**  
  特定の相手について、発言・説明・約束の信頼性を高く見積もる関係状態
- **REL-D: Distrustful Relationship**  
  同じ相手について、発言・説明・約束の信頼性を低く見積もる関係状態

Relationship packetは、現在Situation固有の出来事や現在Responseを含めず、過去Episodeそのものではなく、相互作用履歴から形成された**現在の関係状態**として記述する。

## Experimental Design

各scenario familyで次を固定する。

- Situation
- Perception
- Values & Beliefs: target meaningに対して `none / neutral`
- counterpart role / external constraints
- generation prompt template

操作するのはRelationshipだけとする。

Temperament T0はExperience生成時には与えない。Perceptionを既知の状態として固定し、`Rel → E` の条件付き効果だけを検証するためである。

### Perception boundary

固定Perceptionには、現在の相手の行動・発言の何がsalientか、どのような緊張・驚き・不快等が生じているかまでを含め得る。

ただし次を含めない。

- 「善意だ」「協力的だ」等の現在相手の意図の結論
- 「裏切りだ」「操作だ」「敵意だ」等のRelationship依存の意味づけ
- 現在のResponse、意思決定、行動計画

つまり、**同じPerceptionからREL-T / REL-DのどちらのExperienceも成立し得る余地**を残す。

## Planned sample size

- 8 independent social scenario families
- 2 Relationship conditions: REL-T / REL-D
- 3 replicates per cell

Main generation:

`8 families × 2 Relationship conditions × 3 replicates = 48 Experiences`

Blind evaluation:

`48 Experiences`

PretestはPF-EXP-0005 pilot-002と同様、測定対象を混ぜないため分離する。

- **Relationship quality pretest**: `8 families × 2 conditions = 16`
- **Perception boundary pretest**: `8 families = 8`

合計pretestは **24**。予定される最小API評価単位は 24 + 48 + 48 = **120**。

## Experience representation

生成対象はExperienceのみとする。

> **PerceptionされたSituationが、そのRelationship状態のもとでCharacterにとってどのような意味を持つ経験となったか**

を1〜3文程度で記述する。

生成物にAction、意思決定、行動計画、ResponseのIntensity / Latency、固定trait label、現在Situationに存在しない新規外部事実を含めない。

## Blind evaluation

blind evaluatorにはRelationship condition（REL-T / REL-D）を見せない。

Evaluatorには、

1. current Situation
2. fixed Perception
3. generated Experience

のみを提示する。

主要評価軸：

- `benign_good_faith_meaning` 0–4：現在の出来事が善意・協力・支持的意図に基づく経験として意味づけられている程度
- `suspicious_adverse_intent_meaning` 0–4：現在の出来事が不信・自己都合・操作・不利益につながり得る意図を含む経験として意味づけられている程度

品質評価：

- `response_leakage` 0–4

主要効果量は、

$$
\Delta B = \overline{B}_{REL-T} - \overline{B}_{REL-D}
$$

$$
\Delta S = \overline{S}_{REL-D} - \overline{S}_{REL-T}
$$

とする。H-REL01は `ΔB > 0` かつ `ΔS > 0` を予測する。

## Frozen gate plan

数値は実装PRで `thresholds.yaml` に固定し、実行後には変更しない。

### Pretest

- **P1 Relationship separation**：REL-T / REL-DがTrust / Distrustの両軸で十分に分離する
- **P2 No current-response directiveness**：Relationship packetが現在Responseを直接指示しない
- **P3 No current-situation leakage**：Relationship packetが現在Situation固有の事実を含まない
- **P4 Relationship specificity**：Relationship packetが「人一般・世界一般」に関するValues & Beliefsへ広がらず、特定相手との関係状態に限定される
- **P5 Perception boundary**：fixed Perceptionが善意 / 不信のExperience-level meaningを先取りしていない

planned thresholds:

- P1 Trust separation `>= 2.0`
- P1 Distrust separation `>= 2.0`
- P1 correct family direction `>= 7 / 8`
- P2 mean `<= 0.50`, max `<= 1`
- P3 mean `<= 0.50`, max `<= 1`
- P4 mean `<= 0.50`, max `<= 1`
- P5 mean `<= 0.50`, max `<= 1`

PretestがFAILした場合はmain generationへ進まない。

### Main confirmatory gates

- **G1 Benign / good-faith meaning effect**：`ΔB >= 0.75`
- **G2 Suspicious / adverse-intent meaning effect**：`ΔS >= 0.75`
- **G3 Family generalization**：8 family中6以上で `ΔB_f > 0` かつ `ΔS_f > 0`
- **G4 Leave-one-family-out robustness**：全LOOで `ΔB > 0` かつ `ΔS > 0`
- **G5 Experience boundary quality**：Response leakage mean `<= 0.50`、max `<= 1`

**Overall PASSはG1〜G5をすべて満たすこと**とする。

## Interpretation boundary

PASSした場合に支持するのは、

> **固定されたSituation・Perception・target-neutral Values & Beliefsのもとで、特定相手とのTrust状態の違いがExperienceの意味を再現可能かつ方向整合的に変え得る。**

という限定された主張である。

PF-EXP-0005と合わせて、`E_t = h(P_t, VB_t, Rel_t)` のうち `VB → E` と `Rel → E` の二つの条件付き寄与が個別に支持されるかを検証できる。

ただし、本実験だけでは次を主張しない。

- Relationshipが自然に形成・更新される機構
- Trust以外のRelationship次元（親密さ、敵対、役割等）への一般化
- Relationshipが自然なPerception形成へ影響しないこと
- `Experience → Response`
- 人間への一般化
- 独立Evaluatorまたは人手評価での再現

## Audit policy

- Gate、threshold、stimulus、prompt、schemaはmain generation前に固定する
- Pretest FAIL時はmain generationへ進まない
- Raw responsesは公開しない
- Blind keyはevaluation完了までanalysisから分離する
- Gate判定後の探索分析はconfirmatory resultと分離する
- Gate未達後に同pilotの閾値を緩和しない
- PF-EXP-0001〜0005の実行済み結果は変更しない

## Plan / implementation boundary

このPRではResearch Question、Hypothesis、操作、pretest、confirmatory gates、audit policyを固定する。

stimuli、Relationship packet、prompts、schemas、runner、evaluator、analyzer、manifest、tests等の実装は別PRとする。

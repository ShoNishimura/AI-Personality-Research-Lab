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

## Relationship dimensionality policy

現時点ではRelationshipを固定された多次元ベクトルとして定義しない。

pilot-001では **Trust一軸だけ**を検証する。将来、Trustだけでは説明できないExperience差が確認された場合に、候補としてCloseness、Power / Role等を個別に検証する。候補次元を事前に中核変数として採用しない。

入力セットはTrust専用の題材へ最適化せず、可能な範囲で**relationship-genericなscenario family**として設計する。ただし、将来の全Relationship次元で同一stimulusを必ず再利用することは要件としない。

再利用するのは、追加候補を `Rel_t` のみの操作として表現し、Situation・Perception・Values & Beliefsを固定できる場合に限る。たとえばClosenessは同一scenarioを再利用できる可能性がある。一方、Power / Roleの操作が外的な権限、資源、制度上の役割や制約そのものを変える場合、それは正本上Situation側の変更を伴い得るため、別scenarioまたは別実験設計を用いる。

## Confirmatory Hypothesis

### H-REL01 — Trust state effect on Experience

Situation、Perception、Values & Beliefsを固定したとき、**特定相手とのTrust状態の違いは、生成されるExperienceの意味を対応する方向へ変化させる。**

pilot-001ではRelationshipの多次元性を一度に扱わず、Trust一軸だけを操作する。

- **REL-T: Trusting Relationship**  
  特定の相手について、発言・説明・約束の信頼性を高く見積もる関係状態
- **REL-D: Distrustful Relationship**  
  同じ相手について、発言・説明・約束の信頼性を低く見積もる関係状態

Relationship packetは、現在Situation固有の出来事や現在Responseを含めず、過去Episodeそのものではなく、相互作用履歴から形成された**現在の関係状態**として記述する。

さらにTrust以外のRelationship候補を同時に動かさない。packetには、親密さ・愛情・付き合いの長さ、上下関係・権限、依存・資源関係等を条件差として含めない。

## Experimental Design

各scenario familyで次を固定する。

- Situation
- Perception
- Values & Beliefs: target meaningに対して `none / neutral`
- counterpart identity / external constraints
- generation prompt template

操作するのはRelationshipのTrust状態だけとする。

Temperament T0はExperience生成時には与えない。Perceptionを既知の状態として固定し、`Trust within Rel → E` の条件付き効果だけを検証するためである。

### Relationship-generic scenario bank

8 scenario familiesは、Trustの効果を測定できる一方で、Trustを答えとして埋め込まない社会的曖昧性から構成する。

各familyは次を満たす。

1. 特定のcounterpartによる現在の発言・行動・不作為が存在する
2. 現在事実だけでは相手の意図・信頼性が一意に決まらない
3. Situation自体に「嘘」「裏切り」「善意」「好意」「親密」「権威」等のRelationship-level結論を含めない
4. Perceptionを固定したまま、少なくともTrusting / Distrustfulの双方から異なるExperienceが成立し得る
5. 不要なCloseness、Affection、Power、Dependency等を前提にしない
6. 将来別次元を検証するとき、Sit / P / VBを固定したままその次元だけ操作できる場合には再利用可能な構造にする

このscenario bankは**再利用可能性を高めるための共通基盤**であり、将来の次元を無理に同じstimulusへ押し込むための固定資産ではない。

### Perception boundary

固定Perceptionには、現在の相手の行動・発言の何がsalientか、どのような緊張・驚き・不快等が生じているかまでを含め得る。

ただし次を含めない。

- 「善意だ」「協力的だ」等の現在相手の意図の結論
- 「裏切りだ」「操作だ」「敵意だ」等のTrust依存の意味づけ
- 「親しい相手だから傷つく」等のCloseness依存の意味づけ
- 上下関係、権限、依存関係を前提にした意味づけ
- 現在のResponse、意思決定、行動計画

つまり、**同じPerceptionからREL-T / REL-DのどちらのExperienceも成立し得る余地**を残し、将来の別Relationship次元を不必要に先取りしない。

## Planned sample size

- 8 independent relationship-generic social scenario families
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

- **P1 Trust separation**：REL-T / REL-DがTrust / Distrustの両軸で十分に分離する
- **P2 No current-response directiveness**：Relationship packetが現在Responseを直接指示しない
- **P3 No current-situation leakage**：Relationship packetが現在Situation固有の事実を含まない
- **P4 Trust isolation**：Relationship packetが一般化VBやCloseness / Power等の別Relationship候補を条件差として同時に操作しない
- **P5 Perception boundary**：fixed PerceptionがTrust依存のExperience-level meaningを先取りせず、別Relationship次元も不必要に埋め込まない

planned thresholds:

- P1 Trust separation `>= 2.0`
- P1 Distrust separation `>= 2.0`
- P1 correct family direction `>= 7 / 8`
- P2 mean `<= 0.50`, max `<= 1`
- P3 mean `<= 0.50`, max `<= 1`
- P4 generalized-VB leakage mean `<= 0.50`, max `<= 1`
- P4 closeness / affection leakage mean `<= 0.50`, max `<= 1`
- P4 power / dependency leakage mean `<= 0.50`, max `<= 1`
- P5 Trust-meaning preload mean `<= 0.50`, max `<= 1`

PretestがFAILした場合はmain generationへ進まない。

### Main confirmatory gates

- **G1 Benign / good-faith meaning effect**：`ΔB >= 0.75`
- **G2 Suspicious / adverse-intent meaning effect**：`ΔS >= 0.75`
- **G3 Family generalization**：8 family中6以上で `ΔB_f > 0` かつ `ΔS_f > 0`
- **G4 Leave-one-family-out robustness**：全LOOで `ΔB > 0` かつ `ΔS > 0`
- **G5 Experience boundary quality**：Response leakage mean `<= 0.50`、max `<= 1`

**Overall PASSはG1〜G5をすべて満たすこと**とする。

## Future reuse rule

pilot-001のscenario familyは、後続Relationship実験で次の条件を満たす場合に優先的に再利用する。

- 新しい候補次元だけをRelationship packetとして操作できる
- Situationを変更しない
- Perceptionを変更しない
- Values & Beliefsを変更しない
- 現在の評価軸をそのまま流用せず、新しい次元に対応するExperience評価軸を事前定義する

この条件を満たさない場合は、比較可能性のために無理に同じstimulusを使わない。

特にPower / Roleについては、外的な権限・制度上の役割・利用可能資源が変わるならSituation操作とみなし、Relationship単独効果とは別に設計する。

## Interpretation boundary

PASSした場合に支持するのは、

> **固定されたSituation・Perception・target-neutral Values & Beliefsのもとで、特定相手とのTrust状態の違いがExperienceの意味を再現可能かつ方向整合的に変え得る。**

という限定された主張である。

PF-EXP-0005と合わせて、`E_t = h(P_t, VB_t, Rel_t)` のうち `VB → E` と `Trust within Rel → E` の二つの条件付き寄与が個別に支持されるかを検証できる。

ただし、本実験だけでは次を主張しない。

- Relationshipが自然に形成・更新される機構
- Relationship全体がTrust一軸で十分であること
- Trust以外のRelationship次元への一般化
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
- 将来の再利用可能性を理由にpilot-001のstimulusを事後変更しない

## Plan / implementation boundary

このPRではResearch Question、Hypothesis、操作、scenario設計原則、pretest、confirmatory gates、future reuse rule、audit policyを固定する。

stimuli、Relationship packet、prompts、schemas、runner、evaluator、analyzer、manifest、tests等の実装は別PRとする。

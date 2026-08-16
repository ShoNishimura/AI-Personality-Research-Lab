# PF-EXP-0006 protocol

## 1. Purpose

PF-EXP-0006は、APRL Personality Formation Model v1.2の

`E_t = h(P_t, VB_t, Rel_t)`

のうち、`Relationship → Experience` の条件付き寄与を他要因からできるだけ分離して検証する。

PF-EXP-0005 pilot-002で `Values & Beliefs → Experience` は支持されたため、次にもう一つのExperience入力であるRelationshipを単独操作する。

ただしRelationshipを事前に多次元ベクトルとして固定しない。pilot-001ではTrust一軸のみを扱い、他の候補次元は必要性が確認された場合に後続実験で追加する。

## 2. Unit of comparison

比較単位はscenario family内のREL-T / REL-D pairとする。

同一familyでは次を完全に共通化する。

- current Situation
- supplied Perception packet
- Values & Beliefs control
- counterpart identity
- external constraints
- generation prompt template

操作するのはRelationship内のTrust状態だけとする。

Temperament T0はExperience生成時に与えない。Perceptionを既知の状態として固定し、`Trust within Rel → E` の条件付き効果を検証するためである。

## 3. Relationship dimensionality policy

現時点で採用するRelationship要素はTrustだけである。

将来候補としてCloseness、Power / Role等を検討し得るが、pilot-001の時点では独立変数として採用しない。

relationship-generic scenario bankを用意し、後続候補が次の条件を満たすときのみ同じSituation / Perceptionを再利用する。

1. 新しい候補次元をRelationship packetの差だけとして操作できる
2. Situationを変更しない
3. Perceptionを変更しない
4. Values & Beliefsを変更しない
5. 外的な制度・資源・権限等の制約を変更しない

この条件を満たさない候補へ同一stimulusを強制的に再利用しない。

特にPower / Roleは注意する。相手との主観的な役割期待をRelationshipとして操作できる場合は再利用可能性があるが、制度上の権限、利用可能資源、命令権等の外部事実まで変える場合はSituation操作となり得るため、Relationship単独実験とは分ける。

## 4. Trust construction rule

pilot-001ではRelationshipのうちTrust一軸だけを扱う。

### REL-T — Trusting Relationship

特定の相手との継続的関係について、相手の発言、説明、約束等の信頼性を高く見積もっている状態とする。

### REL-D — Distrustful Relationship

同じ相手との継続的関係について、相手の発言、説明、約束等の信頼性を低く見積もっている状態とする。

Trust packetは禁止事項として次を含めない。

- 現在Situation固有の人物の発言・行動・結果
- 「今回は信じるべき」「距離を取るべき」等の現在Response指示
- Action、意思決定、行動計画
- 現在Experienceの結論そのもの
- Characterの人一般・世界一般への信念
- Characterの価値観一般
- 具体的な過去Episodeの列挙
- 親密さ、愛情、好意、付き合いの長さを条件差として示す情報
- 上下関係、制度上の権限、役割上の優位を条件差として示す情報
- 依存、資源供給、不可欠性等を条件差として示す情報

Trustは、過去Episodeを直接再生する入力ではなく、相互作用履歴から形成された**特定相手との現在の関係状態**として記述する。

## 5. Values & Beliefs control

Values & Beliefsは条件間で完全に共通化し、target meaningに関して `none / neutral` とする。

本実験では、

- 人一般への信頼 / 不信
- 対立を避ける価値
- 協調を優先する価値
- 自己防衛を優先する価値
- 親密さを重視する価値
- 権威への服従 / 反発

等を操作しない。

特定相手についてのTrust状態だけをRelationshipへ置き、一般化されたValues & Beliefsとの境界を保つ。

## 6. Relationship-generic Situation bank

各familyに一つのsocial Situationを用意し、REL-T / REL-Dで完全同一とする。

SituationはCharacter外部の現在の事実・出来事・条件のみを記述し、Characterの内的意味づけやRelationship状態を含めない。

scenario bankはTrust専用の「疑わしい出来事集」にしない。各familyは次の条件を満たす。

1. 特定のcounterpartによる発言・行動・不作為がある
2. 現在事実だけでは意図や信頼性が一意に決まらない
3. 嘘、裏切り、善意、好意、親密さ、権威等のRelationship-level結論をSituationに含めない
4. 現在Outcomeを確定しすぎず、Relationship状態によってExperienceの意味が変わる余地がある
5. 不要なCloseness、Affection、Power、Dependencyを前提としない
6. 同一Sit / P / VBのまま別Relationship候補を操作できる場合には再利用可能な構造を保つ

familyは一つの題材に偏らないよう、社会的曖昧性の異なる形へ分散する。具体的なstimuliは実装PRで固定する。

scenario bankの再利用可能性は設計品質の一部だが、将来すべてのRelationship候補で同一bankを使えることはGateではない。

## 7. Perception fixation and generic boundary

本実験ではPerceptionをgeneration stepで再生成しない。

各familyに一つのPerception packetを用意し、REL-T / REL-Dへ同一文字列または同一構造データとして入力する。

Perceptionは、Situationの何がsalientになり、どのようなmotivational-emotional significanceとして感じ取られているかまでを記述する。

一方、次を含めない。

- 相手の現在意図が善意 / 悪意であるという結論
- 支持 / 協力 / 裏切り / 操作 / 敵意等のTrust依存の意味づけ
- 「親しい相手だから」「距離のある相手だから」等のCloseness依存の意味づけ
- 上下関係・権限・依存を前提にした意味づけ
- 現在のAction、意思決定、行動計画

同じPerceptionから、REL-Tならgood-faith寄り、REL-Dならsuspicious寄りのExperienceがどちらも成立し得る余地を残す。

また、将来別Relationship候補を検証する可能性を損なわないため、Perception自体が不要なCloseness / Power意味を先取りしないようにする。

## 8. Generation

Experience generatorには以下だけを与える。

1. current Situation
2. fixed Perception packet
3. common Values & Beliefs control
4. Trust packet
5. Experience output schema

生成対象はExperienceのみとし、1〜3文程度で記述させる。

禁止事項：

- Action
- 意思決定
- 行動計画
- ResponseのIntensity / Latency
- Characterの固定trait label
- 現在Situationに存在しない外部事実の追加
- Trust packetの単純な逐語反復

## 9. Blind evaluation

評価セット作成時に次をblind化する。

- REL-T / REL-D label
- family内pair identity
- generation order

Evaluatorにはcurrent Situation、fixed Perception、generated Experienceのみを与える。Trust packetとcondition labelは与えない。

主要評価軸：

- `benign_good_faith_meaning` 0–4
- `suspicious_adverse_intent_meaning` 0–4

品質評価：

- `response_leakage` 0–4

補助評価としてvalence / arousal等を記録してよいが、confirmatory gateの代替には用いない。

将来Closeness等を検証する場合は、このTrust用評価軸を流用せず、その候補次元がExperienceへ与える意味差を測る軸を新たに事前定義する。

## 10. Pretest

main generation前に二種類のpretestを別API評価として実施する。

### 10.1 Relationship quality pretest

`8 families × 2 Relationship conditions = 16 packets`

SituationとTrust packetを提示し、P1〜P4を評価する。PerceptionやExperience生成は提示しない。

#### P1 Trust separation

REL-TがREL-DよりTrustを強く表し、REL-DがREL-TよりDistrustを強く表すこと。

planned thresholds:

- Trust separation `>= 2.0`
- Distrust separation `>= 2.0`
- correct family direction `>= 7 / 8`

#### P2 No current-response directiveness

Trust packetが現在のAction、意思決定、行動計画を直接指示しないこと。

- mean `<= 0.50`
- max `<= 1`

#### P3 No current-situation leakage

Trust packetに現在Situation固有の事実が混入していないこと。

- mean `<= 0.50`
- max `<= 1`

#### P4 Trust isolation

Trust packetがTrust以外の状態差を同時に作っていないことを別尺度で確認する。

- generalized Values & Beliefs leakage: mean `<= 0.50`, max `<= 1`
- Closeness / Affection leakage: mean `<= 0.50`, max `<= 1`
- Power / Dependency leakage: mean `<= 0.50`, max `<= 1`

P4は「Relationshipであること」だけでなく、**今回操作したいRelationship次元がTrustに限定されていること**を確認するGateとする。

### 10.2 Perception boundary pretest

`8 families = 8 packets`

SituationとPerceptionのみを提示する。Trust packetは提示しない。

#### P5 Perception boundary

fixed Perceptionが現在の相手の意図や信頼性をgood-faith / adverse-intentのどちらかへ既に決め切っていないこと。

- Trust-meaning preload mean `<= 0.50`
- Trust-meaning preload max `<= 1`

Closeness / Power等を明示的に前提化するPerceptionも避ける。実装時にはこれらを設計監査項目として確認し、必要ならP5の補助尺度として記録する。ただしpilot-001のconfirmatory P5はTrust-meaning preloadを主Gateとする。

P1〜P5のいずれかがFAILした場合、main generationへ進まない。

## 11. Confirmatory analysis

主要効果量：

`Delta_B = mean(B_REL-T) - mean(B_REL-D)`

`Delta_S = mean(S_REL-D) - mean(S_REL-T)`

family別効果：

`Delta_B_f = mean(B_REL-T,f) - mean(B_REL-D,f)`

`Delta_S_f = mean(S_REL-D,f) - mean(S_REL-T,f)`

Leave-one-family-outでは各familyを一つずつ除外し、残り7 familyで `Delta_B` / `Delta_S` を再計算する。

## 12. Main confirmatory gates

### G1 Benign / good-faith meaning effect

`Delta_B >= 0.75`

### G2 Suspicious / adverse-intent meaning effect

`Delta_S >= 0.75`

### G3 Family generalization

8 family中6以上で同一family内において、

- `Delta_B_f > 0`
- `Delta_S_f > 0`

を同時に満たす。

### G4 Leave-one-family-out robustness

全leave-one-family-out集合で、

- `Delta_B > 0`
- `Delta_S > 0`

を維持する。

### G5 Experience boundary quality

生成Experienceの`response_leakage`が、

- mean `<= 0.50`
- max `<= 1`

を満たす。

Overall PASSはG1〜G5の全PASSとする。

## 13. Future reuse rule

pilot-001のscenario bankは後続Relationship実験の候補入力セットとして保存する。

再利用条件：

- 新候補だけをRelationship packetで操作できる
- Situation / Perception / Values & Beliefsを固定できる
- 外的権限・資源・制度的制約を変えない
- 新候補専用のpretestとExperience評価軸を実行前に固定する

条件を満たす場合、同一scenario familyを用いることでRelationship次元間の比較可能性を高める。

条件を満たさない場合、同じstimulusを使うことより因果分離を優先する。

## 14. Secondary analysis

以下は事前定義するがconfirmatory gateの代替には用いない。

- REL-T / REL-DでExperience valenceやarousalが変わるか
- benign meaningとsuspicious meaningが同一Experience内で共存する割合
- familyごとの効果量のばらつき
- ExperienceがTrust packetの語彙をどの程度直接反復するか

## 15. Interpretation boundary

PASSした場合、本実験が直接支持するのは、

> 固定されたSituation・Perception・target-neutral Values & Beliefsのもとで、特定相手とのTrust状態の違いがExperienceの意味を再現可能かつ方向整合的に変え得る。

という限定された主張である。

PF-EXP-0005の結果と合わせることで、`E_t = h(P_t, VB_t, Rel_t)` のうち、`VB_t` とRelationship内のTrust状態の条件付き寄与をそれぞれ個別に評価できる。

ただし次は本実験だけでは支持しない。

- Relationshipの自然な形成・更新機構
- Relationship全体がTrust一軸で十分であること
- Trust以外のRelationship次元への一般化
- Relationshipが自然なPerception形成に影響しないこと
- `Experience → Response`
- 人間への一般化
- 独立Evaluatorまたは人手評価での再現

## 16. Audit

- stimulus / prompt / schema / threshold hashをmain generation前に記録する
- pretest FAIL時はmain generationへ進まない
- raw generation textは非公開とする
- blind keyはevaluation完了まで分析から隔離する
- Gate判定後の新規指標はexploratoryと明示する
- FAIL後に同pilotのGateを緩和しない
- PF-EXP-0001〜0005の実行済み記録を変更しない
- 将来のRelationship次元追加を理由にpilot-001のstimulus / Gate / thresholdを事後変更しない

## 17. Plan / implementation boundary

この計画PRではResearch Question、Hypothesis、Trust操作、relationship-generic scenario設計、pretest、confirmatory gates、future reuse rule、audit policyを固定する。

stimuli、Trust packet、prompts、schemas、runner、evaluator、analyzer、manifest、tests等の実装は別PRとする。

# PF-EXP-0006 protocol

## 1. Purpose

PF-EXP-0006は、APRL Personality Formation Model v1.2の

`E_t = h(P_t, VB_t, Rel_t)`

のうち、`Relationship → Experience` の条件付き寄与を他要因からできるだけ分離して検証する。

PF-EXP-0005 pilot-002で `Values & Beliefs → Experience` は支持されたため、次にもう一つのExperience入力であるRelationshipを単独操作する。

## 2. Unit of comparison

比較単位はscenario family内のREL-T / REL-D pairとする。

同一familyでは次を完全に共通化する。

- current Situation
- supplied Perception packet
- Values & Beliefs control
- counterpart role
- external constraints
- generation prompt template

Relationshipだけを操作する。

Temperament T0はExperience生成時に与えない。Perceptionを既知の状態として固定し、`Rel → E` の条件付き効果を検証するためである。

## 3. Relationship construction rule

pilot-001ではRelationshipのうちTrust一軸だけを扱う。

### REL-T — Trusting Relationship

特定の相手との継続的関係について、相手の発言、説明、約束等の信頼性を高く見積もっている状態とする。

### REL-D — Distrustful Relationship

同じ相手との継続的関係について、相手の発言、説明、約束等の信頼性を低く見積もっている状態とする。

Relationship packetは禁止事項として次を含めない。

- 現在Situation固有の人物の発言・行動・結果
- 「今回は信じるべき」「距離を取るべき」等の現在Response指示
- Action、意思決定、行動計画
- 現在Experienceの結論そのもの
- Characterの人一般・世界一般への信念
- Characterの価値観一般
- 具体的な過去Episodeの列挙

Relationshipは、過去Episodeを直接再生する入力ではなく、相互作用履歴から形成された**特定相手との現在の関係状態**として記述する。

## 4. Values & Beliefs control

Values & Beliefsは条件間で完全に共通化し、target meaningに関して `none / neutral` とする。

本実験では、

- 人一般への信頼 / 不信
- 対立を避ける価値
- 協調を優先する価値
- 自己防衛を優先する価値

等を操作しない。

特定相手についての信頼状態だけをRelationshipへ置き、一般化されたValues & Beliefsとの境界を保つ。

## 5. Situation fixation

各familyに一つのsocial Situationを用意し、REL-T / REL-Dで完全同一とする。

SituationはCharacter外部の現在の事実・出来事・条件のみを記述し、Characterの内的意味づけやRelationship状態を含めない。

scenario familyは一つの題材に偏らないよう、例えば次のような社会的曖昧性へ分散する。

- 指摘 / 批評
- 予定変更
- 協力の申し出
- 情報や成果物へのアクセス要求
- 意見の不一致
- 返答の遅れ
- 役割の変更
- 判断への確認・異議

具体的なstimuliは実装PRで固定する。

## 6. Perception fixation and boundary

本実験ではPerceptionをgeneration stepで再生成しない。

各familyに一つのPerception packetを用意し、REL-T / REL-Dへ同一文字列または同一構造データとして入力する。

Perceptionは、Situationの何がsalientになり、どのようなmotivational-emotional significanceとして感じ取られているかまでを記述する。

一方、次を含めない。

- 相手の現在意図が善意 / 悪意であるという結論
- 支持 / 協力 / 裏切り / 操作 / 敵意等のRelationship依存の意味づけ
- 現在のAction、意思決定、行動計画

同じPerceptionから、REL-Tならgood-faith寄り、REL-Dならsuspicious寄りのExperienceがどちらも成立し得る余地を残す。

## 7. Generation

Experience generatorには以下だけを与える。

1. current Situation
2. fixed Perception packet
3. common Values & Beliefs control
4. Relationship packet
5. Experience output schema

生成対象はExperienceのみとし、1〜3文程度で記述させる。

禁止事項：

- Action
- 意思決定
- 行動計画
- ResponseのIntensity / Latency
- Characterの固定trait label
- 現在Situationに存在しない外部事実の追加
- Relationship packetの単純な逐語反復

## 8. Blind evaluation

評価セット作成時に次をblind化する。

- REL-T / REL-D label
- family内pair identity
- generation order

Evaluatorにはcurrent Situation、fixed Perception、generated Experienceのみを与える。Relationship packetとcondition labelは与えない。

主要評価軸：

- `benign_good_faith_meaning` 0–4
- `suspicious_adverse_intent_meaning` 0–4

品質評価：

- `response_leakage` 0–4

補助評価としてvalence / arousal等を記録してよいが、confirmatory gateの代替には用いない。

## 9. Pretest

main generation前に二種類のpretestを別API評価として実施する。

### 9.1 Relationship quality pretest

`8 families × 2 Relationship conditions = 16 packets`

SituationとRelationship packetを提示し、P1〜P4を評価する。PerceptionやExperience生成は提示しない。

#### P1 Relationship separation

REL-TがREL-DよりTrustを強く表し、REL-DがREL-TよりDistrustを強く表すこと。

planned thresholds:

- Trust separation `>= 2.0`
- Distrust separation `>= 2.0`
- correct family direction `>= 7 / 8`

#### P2 No current-response directiveness

Relationship packetが現在のAction、意思決定、行動計画を直接指示しないこと。

- mean `<= 0.50`
- max `<= 1`

#### P3 No current-situation leakage

Relationship packetに現在Situation固有の事実が混入していないこと。

- mean `<= 0.50`
- max `<= 1`

#### P4 Relationship specificity

Relationship packetが特定相手との関係状態を超えて、人一般・世界一般のValues & Beliefsへ広がっていないこと。

- mean `<= 0.50`
- max `<= 1`

### 9.2 Perception boundary pretest

`8 families = 8 packets`

SituationとPerceptionのみを提示する。Relationship packetは提示しない。

#### P5 Perception boundary

fixed Perceptionが現在の相手の意図をgood-faith / adverse-intentのどちらかへ既に決め切っていないこと。

- mean `<= 0.50`
- max `<= 1`

P1〜P5のいずれかがFAILした場合、main generationへ進まない。

## 10. Confirmatory analysis

主要効果量：

`Delta_B = mean(B_REL-T) - mean(B_REL-D)`

`Delta_S = mean(S_REL-D) - mean(S_REL-T)`

family別効果：

`Delta_B_f = mean(B_REL-T,f) - mean(B_REL-D,f)`

`Delta_S_f = mean(S_REL-D,f) - mean(S_REL-T,f)`

Leave-one-family-outでは各familyを一つずつ除外し、残り7 familyで `Delta_B` / `Delta_S` を再計算する。

## 11. Main confirmatory gates

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

## 12. Secondary analysis

以下は事前定義するがconfirmatory gateの代替には用いない。

- REL-T / REL-DでExperience valenceやarousalが変わるか
- benign meaningとsuspicious meaningが同一Experience内で共存する割合
- familyごとの効果量のばらつき
- ExperienceがRelationship packetの語彙をどの程度直接反復するか

## 13. Interpretation boundary

PASSした場合、本実験が直接支持するのは、

> 固定されたSituation・Perception・target-neutral Values & Beliefsのもとで、特定相手とのTrust状態の違いがExperienceの意味を再現可能かつ方向整合的に変え得る。

という限定された主張である。

PF-EXP-0005の結果と合わせることで、`E_t = h(P_t, VB_t, Rel_t)` の二つの内的入力の条件付き寄与をそれぞれ個別に評価できる。

ただし次は本実験だけでは支持しない。

- Relationshipの自然な形成・更新機構
- Trust以外のRelationship次元への一般化
- Relationshipが自然なPerception形成に影響しないこと
- `Experience → Response`
- 人間への一般化
- 独立Evaluatorまたは人手評価での再現

## 14. Audit

- stimulus / prompt / schema / threshold hashをmain generation前に記録する
- pretest FAIL時はmain generationへ進まない
- raw generation textは非公開とする
- blind keyはevaluation完了まで分析から隔離する
- Gate判定後の新規指標はexploratoryと明示する
- FAIL後に同pilotのGateを緩和しない
- PF-EXP-0001〜0005の実行済み記録を変更しない

## 15. Plan / implementation boundary

この計画PRではResearch Question、Hypothesis、操作、pretest、confirmatory gates、audit policyのみを固定する。

stimuli、Relationship packet、prompts、schemas、runner、evaluator、analyzer、manifest、tests等の実装は別PRとする。

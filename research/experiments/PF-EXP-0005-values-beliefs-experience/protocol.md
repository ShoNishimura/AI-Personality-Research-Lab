# PF-EXP-0005 protocol

## 1. Purpose

PF-EXP-0005は、APRL Personality Formation Model v1.2の

`E_t = h(P_t, VB_t, Rel_t)`

のうち、`Values & Beliefs → Experience` の寄与を他要因からできるだけ分離して検証する。

本実験は、PerceptionとExperienceを分離したv1.2の新しい境界を初めて直接扱う。

## 2. Unit of comparison

比較単位はscenario family内のVB-L / VB-E pairとする。

同一familyでは、次を完全に共通化する。

- current Situation
- supplied Perception packet
- Relationship state
- generation prompt template

Values & Beliefsのみを操作する。

Temperament T0はExperience生成時に与えない。Perceptionを既知の状態として固定し、`VB → E` の条件付き効果を検証するためである。

## 3. Values & Beliefs construction rule

pilot-001では次の2条件を用いる。

### VB-L — Learning / Improvement orientation

誤り、指摘、不十分さ、未熟さ等を、学習・修正・改善・能力向上に利用できる情報として捉えやすい一般化されたValues & Beliefsとする。

### VB-E — Evaluation / Competence-protection orientation

能力不足を示さないことや評価を損なわないことを重視し、失敗、指摘、不十分さ等を自己評価・能力評価上の重要な出来事として捉えやすい一般化されたValues & Beliefsとする。

VB packetは禁止事項として次を含めない。

- 現在Situation固有の人物、場所、出来事、結果
- 「今回は修正するべき」「反論するべき」等の現在行動への指示
- Action、意思決定、行動計画
- 条件間の能力、知識、資源、身体状態の差
- 特定人物との信頼、親密さ、敵対等のRelationship差
- 「この出来事は成長の機会だ」「これは評価への脅威だ」等、現在Experienceの結論そのもの

Values & Beliefsは、現在の出来事に対する回答ではなく、**出来事以前から保持されている一般化された内的状態**として記述する。

## 4. Situation fixation

各familyに1つのSituationを用意し、VB-L / VB-Eで完全同一とする。

SituationはCharacter外部の現在の事実・出来事・条件だけを記述し、Characterの内的意味づけ、感情、判断、行動を含めない。

scenario familyは一つの題材に偏らないよう、批評、失敗、知識不足、成果不足、修正要求、不確実な課題等へ分散する。

ただし全familyで、Learning / Evaluationのどちらの意味も成立し得る余地を残す。

## 5. Perception fixation and boundary

本実験ではPerceptionをgeneration stepで再生成しない。

各familyに1つのPerception packetを用意し、VB-L / VB-Eへ同一文字列または同一構造データとして入力する。

Perception packetは、Situationの何がsalientになり、どのようなmotivational-emotional significanceとして感じ取られているかまでを記述する。

一方、次を含めない。

- 学習・改善にとって何を意味するか
- 自己評価・能力評価にとって何を意味するか
- Characterが出来事を人生上どう位置づけるか
- 現在のAction、意思決定、行動計画

例えば、

> 「問題点の指摘が強くsalientになり、否定的な評価を受けたことに不快さを感じている」

はPerceptionとして許容する。

一方、

> 「改善点を得られた有益な経験だと感じる」

> 「自分の能力評価を脅かされた経験だと感じる」

はExperience-level meaningを先取りするため、固定Perceptionには含めない。

この操作は、Values & BeliefsやRelationshipが自然なPerceptionへ影響しないと主張するものではない。`P` を実験上固定し、条件付きの `VB → E` を検証するための介入である。

## 6. Relationship control

Relationshipは `none / neutral` に固定する。

現在Situationで他者が登場する場合も、固有の相互作用履歴、信頼、親密さ、敵対、義務、愛着等を付与しない。

Experience差がRelationshipに由来し得るscenarioはpretestで除外する。

## 7. Generation

Experience generatorには、以下のみを与える。

1. current Situation
2. fixed Perception packet
3. Values & Beliefs packet
4. fixed Relationship state (`none / neutral`)
5. Experience output schema

Temperament T0は与えない。

生成対象はExperienceのみとし、1〜3文程度で記述させる。

禁止事項：

- Action
- 意思決定
- 行動計画
- ResponseのIntensity / Latency
- Characterの固定trait label
- 現在Situationに存在しない外部事実の追加
- Values & Beliefs packetの単純な逐語反復

## 8. Blind evaluation

評価セット作成時に、以下をblind化する。

- VB-L / VB-E label
- family内pair identity
- generation order

Evaluatorにはcurrent Situation、fixed Perception、generated Experienceのみを与える。Values & Beliefs packetとcondition labelは与えない。

Evaluatorは少なくとも次を0–4で評価する。

- `learning_improvement_meaning`
- `evaluation_threat_meaning`
- `response_leakage`

主要confirmatory scoresは前二者とする。

`response_leakage` はExperience / Response境界の品質Gateとして用いる。

## 9. Pretest

main generation前に16 condition packetsをblind評価し、次を確認する。

### P1 VB separation

VB-LがVB-EよりLearning / Improvement orientationを強く表し、VB-EがVB-LよりEvaluation / Competence-protection orientationを強く表すこと。

### P2 No current-response directiveness

Values & Beliefs packetが現在のAction、意思決定、行動計画を直接指示しないこと。

### P3 No current-situation leakage

Values & Beliefs packetに現在Situation固有の事実が混入していないこと。

### P4 Perception boundary

fixed PerceptionがLearning / ImprovementまたはEvaluation ThreatというExperience-level meaningを既に決め切っていないこと。

### P5 Relationship neutrality

scenarioに継続的人間関係の履歴がなく、Relationship差がExperienceを説明する主要因になっていないこと。

閾値は `thresholds.yaml` から変更しない。

Pretest FAIL時はmain generationを実行せず、刺激修正後は新しいpretest versionとして履歴を残す。

## 10. Confirmatory analysis

各Experienceについてblind scoreを得る。

Learning effect：

`Delta_L = mean(L_VB-L) - mean(L_VB-E)`

Evaluation-threat effect：

`Delta_E = mean(E_VB-E) - mean(E_VB-L)`

family別効果：

`Delta_L_f = mean(L_VB-L,f) - mean(L_VB-E,f)`

`Delta_E_f = mean(E_VB-E,f) - mean(E_VB-L,f)`

Leave-one-family-outでは各familyを1つずつ除外し、残り7 familyの `Delta_L` / `Delta_E` を再計算する。

Overall PASS条件はREADME / thresholds.yamlに定義したG1–G5の全PASSとする。

## 11. Main confirmatory gates

### G1 Learning meaning effect

`Delta_L >= 0.75`

### G2 Evaluation-threat meaning effect

`Delta_E >= 0.75`

### G3 Family generalization

8 family中6以上で、同一family内において

- `Delta_L_f > 0`
- `Delta_E_f > 0`

を同時に満たす。

### G4 Leave-one-family-out robustness

全てのleave-one-family-out集合で、

- `Delta_L > 0`
- `Delta_E > 0`

を維持する。

### G5 Experience boundary quality

生成Experienceの`response_leakage`が事前閾値以下である。

## 12. Secondary analysis

以下は事前定義するが、confirmatory gateの代替に用いない。

- VB-L / VB-EでExperienceのvalenceやarousalが変わるか
- 両意味軸が一つのExperience内で共存する割合
- familyごとの効果量のばらつき
- ExperienceがValues & Beliefsの語彙をどの程度直接反復するか

Secondary resultは主要仮説のPASS/FAILと分離して報告する。

## 13. Interpretation boundary

PASSした場合、本実験が直接支持するのは、

> 固定されたSituation・Perception・neutral Relationshipのもとで、Values & Beliefsの違いがExperienceの意味を再現可能かつ方向整合的に変え得る。

という限定された主張である。

同じPerceptionから異なるExperienceが得られるため、PerceptionとExperienceを機能的に分けるv1.2の境界への支持にもなる。

ただし、次は本実験だけでは支持しない。

- `Relationship → Experience`
- `Experience → Response`
- Values & Beliefsの自然な形成・更新機構
- Values & Beliefsが自然なPerceptionへ影響しないこと
- 他のValues & Beliefs次元への一般化
- 実世界の人間への一般化

FAILした場合も、直ちに `VB → Experience` またはPerception / Experience分離を否定しない。操作強度、Perception境界、生成prompt、評価尺度、scenario依存性を切り分ける。

## 14. Audit

- stimulus / prompt / schema / threshold hashをmain generation前に記録する
- pretest FAIL時はmain generationへ進まない
- raw generation textは非公開とする
- blind keyはevaluation完了まで分析から隔離する
- Gate判定後の新規指標はexploratoryと明示する
- FAIL後に同pilotのGateを緩和しない
- 実行済みPF-EXP-0001〜0004の監査記録を変更しない

## 15. Plan / implementation boundary

この計画PRではResearch Question、Hypothesis、操作、pretest、confirmatory gates、audit policyのみを固定する。

stimuli、prompts、schemas、runner、evaluator、analyzer、manifest、tests等の実装は別PRとする。

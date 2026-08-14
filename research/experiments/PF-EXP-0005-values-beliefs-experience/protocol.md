# PF-EXP-0005 protocol

## 1. Purpose

PF-EXP-0005は、APRL Personality Formation Model v1.2の

`E_t = h(P_t, VB_t, Rel_t)`

のうち、`Values & Beliefs → Experience` の寄与を他要因からできるだけ分離して検証する。

本実験はPerceptionとExperienceを分離したv1.2の境界を直接扱う。

## 2. Unit of comparison

比較単位はscenario family内のVB-L / VB-E pairとする。

同一familyでは以下を完全に共通化する。

- current Situation
- supplied Perception packet
- Relationship state
- generation prompt template

Values & Beliefsのみを操作する。Temperament T0はExperience生成時に与えない。

## 3. Values & Beliefs construction rule

### VB-L — Learning / Improvement orientation

能力や知識を固定的ではなく変化し得るものと捉え、不十分さや誤りに関する情報を学習・発達に関わるものとして重視する一般化されたValues & Beliefsとする。

### VB-E — Evaluation / Competence-protection orientation

能力が十分と評価されている状態、評価や立場、能力の確かさを重視する一般化されたValues & Beliefsとする。

VB packetに現在Situation固有の事実、現在行動への指示、Action、意思決定、行動計画、能力差、Relationship差、現在Experienceの結論を含めない。

## 4. Situation fixation

各familyに1つのSituationを用意し、VB-L / VB-Eで完全同一とする。

SituationはCharacter外部の現在の事実・出来事・条件だけを記述する。

## 5. Perception fixation and boundary

各familyに1つのPerception packetを用意し、VB-L / VB-Eへ完全同一で入力する。

Perceptionは、Situationの何がsalientになり、どのようなmotivational-emotional significanceとして感じ取られているかまでを記述する。一方、学習・改善上の意味、自己評価・能力評価上の意味、人生上の位置づけ、Action・意思決定・行動計画は含めない。

この固定は、VBやRelationshipが自然なPerceptionへ影響しないと主張するものではない。`P` を実験上固定し、条件付きの `VB → E` を検証する介入である。

## 6. Relationship control

Relationshipは `none / neutral` に固定する。信頼、親密さ、敵対、義務、愛着等の継続的関係履歴を付与しない。

## 7. Generation

Experience generatorには以下のみを与える。

1. current Situation
2. fixed Perception packet
3. Values & Beliefs packet
4. fixed Relationship state
5. Experience output schema

Temperament T0は与えない。

生成対象はExperienceのみとし、Action、意思決定、行動計画、ResponseのIntensity / Latency、固定trait label、外部事実の追加、VB packetの逐語反復を禁止する。

## 8. Blind evaluation

Evaluatorにはcurrent Situation、fixed Perception、generated Experienceのみを与える。VB packetとcondition labelは与えない。

0〜4で評価する。

- `learning_improvement_meaning`
- `evaluation_threat_meaning`
- `response_leakage`

前二者をconfirmatory score、`response_leakage`をExperience / Response境界の品質Gateとする。

## 9. Pretest

### 9.1 pilot-001

pilot-001ではSituation、Perception、VB、Relationshipを1つのpacketとして16件評価した。

16 / 16 succeededだったが、P2とP4がFAILしたためmainへ進まなかった。

### 9.2 pilot-002 split pretest

pilot-002では評価対象を分離する。

#### VB_QUALITY — 16 evaluations

入力：

- Situation
- Values & Beliefs

PerceptionとRelationshipは提示しない。

評価：

- P1 VB separation
- P2 No current-response directiveness
- P3 No current-situation leakage

#### PERCEPTION_BOUNDARY — 8 evaluations

入力：

- Situation
- fixed Perception
- Relationship

Values & Beliefsは提示しない。

評価：

- P4 Perception boundary
- P5 Relationship neutrality

この分離により、P4を評価する際にVBとの組み合わせからExperienceを推測する経路を遮断する。

閾値は [`thresholds.yaml`](thresholds.yaml) から変更しない。

Pretest FAIL時はmain generationを実行しない。

## 10. Confirmatory analysis

Learning effect：

`Delta_L = mean(L_VB-L) - mean(L_VB-E)`

Evaluation-threat effect：

`Delta_E = mean(E_VB-E) - mean(E_VB-L)`

family別：

`Delta_L_f = mean(L_VB-L,f) - mean(L_VB-E,f)`

`Delta_E_f = mean(E_VB-E,f) - mean(E_VB-L,f)`

Leave-one-family-outでは各familyを1つずつ除外して再計算する。

## 11. Main confirmatory gates

- G1: `Delta_L >= 0.75`
- G2: `Delta_E >= 0.75`
- G3: 8 family中6以上で `Delta_L_f > 0` かつ `Delta_E_f > 0`
- G4: 全LOOで `Delta_L > 0` かつ `Delta_E > 0`
- G5: `response_leakage` が凍結閾値以下

Overall PASSはG1〜G5の全PASSとする。

## 12. Secondary analysis

以下は事前定義するがconfirmatory gateの代替にしない。

- Experience valence / arousal
- dual meaning coactivation
- family別効果量
- VB lexical repetition

## 13. Interpretation boundary

PASSした場合に直接支持するのは、

> 固定されたSituation・Perception・neutral Relationshipのもとで、Values & Beliefsの違いがExperienceの意味を再現可能かつ方向整合的に変え得る。

という限定された主張である。

Relationship、Experience→Response、VB形成更新、他VB次元、人間一般への拡張は主張しない。

## 14. Audit

- stimulus / prompt / schema / threshold hashをmain generation前に記録
- pretest FAIL時はmain generationへ進まない
- raw generation textは非公開
- blind keyはevaluation完了まで隔離
- Gate後の新規指標はexploratory
- FAIL後に同pilotのGateを緩和しない
- pilot-001とpilot-002のphase、path、seedを分離する
- pilot-001の結果をpilot-002で事後再判定しない

## 15. Pilot history

### pilot-001

- pretest: 16 / 16 succeeded
- P1 PASS
- P2 FAIL
- P3 PASS
- P4 FAIL
- P5 PASS
- main not run
- H-VB01 untested

### pilot-002

- P1〜P3 / P4〜P5のpretestを分離
- VB packetのcurrent-response directivenessを弱める
- F03 / F06 Perceptionを境界上より中立な表現へ修正
- thresholds unchanged
- pretest not run

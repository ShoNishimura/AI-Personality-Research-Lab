# PF-EXP-0004 protocol

## 1. Purpose

PF-EXP-0004は、APRL Personality Formation Model v1.1の

`R_t = g(P_t, H_t, Rel_t)`

のうち、`History → Response` の寄与を他要因からできるだけ分離して検証する。

## 2. Unit of comparison

比較単位はscenario family内のH+ / H- pairとする。

同一familyでは、次を完全に共通化する。

- current Experience
- supplied Perception packet
- Relationship state
- body / physiological state
- environmental / physical constraints
- generation prompt template

Historyのみを操作する。

## 3. History construction rule

各Historyは、現在のscenarioと構造的に類似するが同一ではない過去episodeを複数含む。

H+とH-では、過去episodeにおけるCharacterのResponseを可能な限り同一にする。主な差分はResponse後のoutcomeとする。

禁止事項：

- 「慎重な性格になった」「自信を持った」等のtrait / state結論
- 「今回は避けるべき」等の現在行動への助言
- H+だけに勇気・能力・知識を追加する等の能力差
- H-だけに身体損傷・資源喪失等の現在状態差を残す記述
- Relationship差を生む固有人物との継続関係

過去outcomeの結果として現在も残っている物理的・身体的状態を条件間で変えない。Historyの効果とcurrent Experienceの差を混同しないためである。

## 4. Perception fixation

本実験ではPerceptionをgeneration stepで再生成しない。

各familyに1つのPerception packetを用意し、H+ / H-へ同一文字列または同一構造データとして入力する。

Perception packetは、現在の状況に含まれる主要な機会・コスト・リスクのsalienceを記述するが、具体的なActionを指示しない。

この操作は「HistoryがPerceptionへ影響しない」ことを検証するものではない。`P` を実験上固定し、条件付きの `H → R` を検証するための介入である。

## 5. Relationship control

Relationshipは `none / neutral` に固定する。

現在scenarioとHistoryの双方で、信頼、親密さ、敵対、義務、愛着等がResponseを左右しやすい継続的人間関係を避ける。

## 6. Generation

Response generatorには、以下のみを与える。

1. current Experience
2. fixed Perception packet
3. History
4. fixed Relationship state
5. Response output schema

Temperament T0は与えない。

生成物は次を含む。

- `action`
- `intensity` 0–4
- `latency` 0–4

`latency` は実API処理時間ではなく、CharacterがAction開始までに置く意図上の遅延である。

## 7. Blind evaluation

評価セット作成時に、以下をblind化する。

- H+ / H- label
- family内pair identity
- generation order

Evaluatorにはcurrent scenario、fixed Perception、Responseを与える。History本文とcondition labelは与えない。

Evaluatorは少なくとも次を0–4で評価する。

- approach_commitment
- caution_information_seeking
- response_intensity
- response_latency

主要confirmatory scoreは `approach_commitment` とする。

## 8. Pretest

main generation前にHistory stimulusだけをblind評価し、次を確認する。

- outcome valenceがH+ > H-となる
- current Responseへの直接指示が弱い
- trait / personality labelingが弱い
- family間で操作方向が一貫する

閾値は `thresholds.yaml` から変更しない。

Pretest FAIL時はmain generationを実行せず、stimulus修正後に新しいpretest versionとして履歴を残す。

## 9. Confirmatory analysis

各responseについてblind `approach_commitment` scoreを得る。

全体効果：

`Delta_A = mean(A_H+) - mean(A_H-)`

family別効果：

`Delta_A_f = mean(A_H+,f) - mean(A_H-,f)`

Leave-one-family-out：

各familyを1つずつ除外し、残り7 familyの `Delta_A` を再計算する。

Overall PASS条件はREADME / thresholds.yamlに定義したG1–G3の全PASSとする。

## 10. Secondary analysis

以下は事前定義するが、confirmatory gateの代替に用いない。

- H-でcautionが高まるか
- H-でlatencyが長くなるか
- intensityがHistory valenceで変化するか
- action categoryの分布が変わるか

Secondary resultは主要仮説のPASS/FAILと分離して報告する。

## 11. Audit

- stimulus / prompt / schema / threshold hashをmain generation前に記録する
- raw generation textは非公開とする
- blind keyはevaluation完了まで分析から隔離する
- Gate判定後の新規指標はexploratoryと明示する
- FAIL後に同pilotのGateを緩和しない

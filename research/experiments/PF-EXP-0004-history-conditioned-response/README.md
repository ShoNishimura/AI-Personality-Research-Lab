# PF-EXP-0004 — History-Conditioned Response

> Status: **planned / protocol and gates frozen before responses**  
> Canonical Model: [APRL Personality Formation Model v1.1](../../../docs/models/Personality_Formation_Model.md)  
> Target relation: `R_t = g(P_t, H_t, Rel_t)`

## Research Question

> **同一のPerceptionとRelationshipのもとで、類似状況に対する過去のResponse結果の履歴は、現在のResponseを再現可能かつ方向整合的に変えるか。**

PF-EXP-0001〜0003は主に `P_t=f(E_t,T_0)` を検証した。PF-EXP-0004は初めてResponse側へ進み、現行v1.1で明示された `History → Response` の寄与を単独で検証する。

## Confirmatory Hypothesis

### H-HR01 — Outcome-history effect on Response

現在のPerceptionを固定したとき、**類似状況で接近・試行した過去のResponseが好ましい結果につながったHistory（H+）** は、**同じ過去Responseが好ましくない結果につながったHistory（H-）** より、現在のResponseを接近・実行方向へ偏らせる。

主要評価量を、blind evaluatorによる `approach_commitment`（0–4）とする。

$$
\Delta A = \overline{A}_{H+} - \overline{A}_{H-}
$$

H-HR01は `\Delta A > 0` を予測する。

## Why History first

現行モデルは、

$$
R_t=g(P_t,H_t,Rel_t)
$$

とする。

最初のResponse実験でHistoryとRelationshipを同時に操作すると、Response差の原因を切り分けにくい。そこでPF-EXP-0004では、

- Perception：固定
- History：操作
- Relationship：固定 / 非顕在化
- Temperament：Response生成時には与えない

とし、まずHistoryの寄与だけを検証する。

Relationshipの独立効果は後続実験候補とする。

## Experimental Design

### Current state

各scenario familyについて、現在のExperienceとPerception packetを1つ固定する。

Perceptionは生成し直さず、Response生成器へ既知の状態として直接与える。これにより本実験は、自然な全過程の再現ではなく、**固定されたPerceptionに条件づけたResponse生成の検証**として扱う。

現在のPerceptionは、接近可能性と無視できないコスト・リスクの双方を含み、HistoryによってResponse差が現れ得るが、一方のActionを直接要求しない内容とする。

### History manipulation

各familyに2条件を置く。

- **H+ favorable outcome history**：過去に類似状況で接近・試行するResponseを選び、その結果が複数回好ましかった
- **H- adverse outcome history**：過去に類似状況で**同じ接近・試行Response**を選び、その結果が複数回好ましくなかった

重要なのは、H+ / H-で過去のResponse自体を変えず、**結果だけを主に操作する**ことである。

Historyには、「そのため慎重になった」「自信を持った」「次も挑戦すべき」等の人格ラベル、心理的結論、現在行動への指示を含めない。

### Fixed factors

- Relationshipは全条件で `none / neutral` とし、関係性が判断を左右しやすいscenarioを避ける
- Body / physiological stateはfamily内で固定する
- Environmental / physical constraintsはfamily内で固定する
- T0はResponse生成promptへ入れない
- H+ / H-でcurrent ExperienceとPerception packetは完全同一とする

## Scenario families and sample size

- **8 independent scenario families**
- 2 History conditions: H+ / H-
- 3 replicates per cell

Main generation:

`8 families × 2 histories × 3 replicates = 48 responses`

Blind evaluation:

`48 responses`

History pretest:

`8 families × 2 histories = 16 history stimuli`

予定される最小API評価単位は、pretest 16 + generation 48 + blind evaluation 48 = **112**。

## Response representation

Responseは現行正本に合わせ、次を出力する。

```text
Response = (Action, Intensity, Latency)
```

- **Action**：現在何をするか。短い自由記述
- **Intensity**：反応の強さ 0–4
- **Latency**：開始までの意図された遅延 0–4。API応答時間そのものではない

Response生成時にPerceptionを再評価・再生成させない。

## Blind evaluation

blind evaluatorにはHistory condition（H+ / H-）を見せない。

current scenario、固定Perception、Responseのみを提示し、少なくとも次を評価する。

- `approach_commitment` 0–4：回避・保留から、明確な接近・実行まで
- `caution_information_seeking` 0–4：確認・情報収集・条件付き実行の強さ
- `response_intensity` 0–4
- `response_latency` 0–4

主要confirmatory metricは `approach_commitment` とする。他の尺度はResponseの構造を診断する副次指標とする。

## Frozen gates

Gateの数値は [`thresholds.yaml`](thresholds.yaml) を正とする。

### Pretest

- **P1 Outcome separation**：H+とH-のoutcome valence差が十分大きい
- **P2 No directiveness**：Historyが現在Responseを直接指示しない
- **P3 No trait labeling**：Historyに人格特性・心理変化の明示を入れない
- **P4 Family coverage**：大半のfamilyでH+ / H-操作が意図方向に成立する

PretestがFAILした場合、main response generationへ進まない。

### Main confirmatory gates

- **G1 Primary history effect**：`mean(A_H+) - mean(A_H-) >= 0.75`
- **G2 Family generalization**：8 family中6以上で `A_H+ > A_H-`
- **G3 Leave-one-family-out robustness**：全LOOでhistory effectが正方向を維持する

**Overall PASSはG1–G3をすべて満たすこと**とする。

Intensity、Latency、cautionのHistory差は事前定義したsecondary / diagnostic analysisとし、G1–G3の代替には用いない。

## Interpretation boundary

PASSした場合に支持するのは、

> **固定されたPerceptionのもとでも、過去の結果履歴が現在のResponseを系統的に変え得る。**

という限定された主張である。

以下は本実験だけでは主張しない。

- Historyが自然なPerception形成へ影響しないこと
- Relationshipの効果
- C / Regulationの必要性または不要性
- Motivationという独立変数の存在または不存在
- 実世界の人間に同じ効果量が成立すること

FAILした場合も直ちに `History → Response` を否定しない。History操作、Perception固定法、Response尺度、scenario依存性を切り分け、追加機構を正本へ導入する前に再検証する。

## Audit policy

- Gate、threshold、stimulus、prompt、schemaはmain generation前に固定する
- Raw responsesは公開しない現行方針を維持する
- Blind keyは評価完了までanalysisから分離する
- Gate判定後の探索分析はconfirmatory resultと分離して記録する
- Gate未達後に閾値を変更しない

## Next step after this PR

このPRは**実験計画のみ**を追加する。

マージ後、別PRでstimuli、prompt、schema、runner、analyzerを実装し、history pretestを通過した場合だけpilot-001へ進む。
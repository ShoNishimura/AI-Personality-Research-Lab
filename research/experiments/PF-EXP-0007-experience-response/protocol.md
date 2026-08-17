# PF-EXP-0007 protocol

## 1. Purpose

PF-EXP-0007は、APRL Personality Formation Model v1.2の

`R_t = g(E_t, Sit_t)`

のうち、`Experience → Response` の条件付き寄与をSituationからできるだけ分離して検証する。

PF-EXP-0005 pilot-002では `Values & Beliefs → Experience`、PF-EXP-0006 pilot-001ではRelationship内のTrust状態による `Relationship → Experience` が今回の実験条件で支持された。

次の未検証中核関係として、同一Situationに対してExperienceの主観的意味だけを変えたとき、ResponseのAction意味が対応して変化するかを検証する。

本実験は上流からResponseまでの媒介経路を一括検証するものではない。Experienceを既知の状態として直接与え、`E_t → R_t` の条件付き効果だけを対象とする。

## 2. Unit of comparison

比較単位はscenario family内のE-B / E-A pairとする。

同一familyでは次を完全に共通化する。

- current Situation
- counterpart identity（該当する場合）
- external constraints
- generation prompt template
- Response output schema

操作するのはExperience packetのみとする。

Response生成時には次を入力しない。

- Temperament T0
- Perception
- Values & Beliefs
- Relationship
- Episodic Memory / History

これらをResponse generatorへ与えると、`Experience → Response` ではなく上流状態からResponseへの追加経路を同時に操作することになるためである。

## 3. Experience contrast

pilot-001ではExperience全体を多次元分類しない。一つの最小contrastだけを扱う。

### E-B — Benign / Low-risk Experience

現在のSituationについて、Characterが主観的に、

- 悪意・脅威・不利益の可能性を低く感じている
- 現在の出来事を比較的benign / low-riskな意味として経験している

状態とする。

### E-A — Adverse / High-risk Experience

同じSituationについて、Characterが主観的に、

- 悪意・脅威・不利益の可能性を高く感じている
- 現在の出来事を比較的adverse / high-riskな意味として経験している

状態とする。

このcontrastは客観的Situationの安全性・危険性を変更しない。あくまで**同一SituationがCharacterにとって持つ主観的意味**を操作する。

また、Benign / AdverseはExperienceの普遍的な二分類として採用するものではない。pilot-001で `E_t → R_t` を検出可能な最小操作として用いる。

## 4. Experience construction rule

E-B / E-A packetは、可能な限り同じ構文密度・情報量で記述し、target meaning以外の不要な差を増やさない。

Experience packetに含めてよいもの：

- Characterにとって現在の出来事がどのような意味を持つ経験となっているか
- 主観的なbenign / adverse significance
- 主観的な安心・警戒・不利益可能性等の意味

Experience packetに含めないもの：

- 「質問する」「距離を取る」「断る」等のAction
- 意思決定
- 行動計画
- 「〜すべき」等のResponse指示
- Response Intensity / Latency
- 現在Situationに存在しない外部事実
- 具体的な過去Episode
- 「この人を信頼しているから」等のRelationship状態の明示的原因
- 「協力を重視しているから」等のValues & Beliefsの明示的原因
- 「新奇性を求める性格だから」等のTemperamentの明示的原因

Experienceは上流状態を再説明するpacketではなく、**現在時点で形成済みの主観的意味**として与える。

## 5. Situation bank policy

PF-EXP-0006の8つのrelationship-generic Situationをpilot-001の候補bankとして優先的に再利用する。

理由は、これらが既に次の性質を持つためである。

- social Situationとして外部事実が固定されている
- 意図やRelationship-level結論をSituation自体が決め切っていない
- 同一Situationに複数の主観的意味を与える余地がある

ただし、PF-EXP-0006で有効だったことはPF-EXP-0007での適合性を保証しない。

Responseを検証する本実験では、Situation自体がConstructive Engagement / Protective Distancingのどちらかを強制すると、Experience操作の余地が小さくなる。

そのため、各familyは次を満たすことを要求する。

1. E-B / E-Aでcurrent Situationを完全に同一にできる
2. Situationだけではtarget Response方向が一意に決まらない
3. 外部規則・時間制約・資源制約等が一方のtarget Responseを事実上強制しない
4. E-B / E-Aのどちらからも複数の具体的Actionが成立し得る
5. 特定Actionを促す文言をSituationに追加しない

再利用可能性より因果分離を優先する。

実装PRでstimuliをfreezeする前に静的レビューを行い、不適合familyは置換してよい。pilot-001のAPI pretest開始後は同pilot内でstimuliを変更しない。

## 6. Response definition

正本v1.2に従い、ResponseはCharacterが**選択し、開始する反応**とする。

`Response_t = (Action_t, Intensity_t, Latency_t)`

### Action

何をするかを表す。対話、質問、協力、保留、拒否、距離確保、情報制限、回避等を含み得る。

### Intensity

選択したActionをどの程度の強さで開始するかを表す。

### Latency

ExperienceからResponseを開始するまでの相対的な遅さを表す。

pilot-001のconfirmatory targetはActionの**意味方向**だけとする。

ExperienceのBenign / Adverse差からIntensity / Latencyの一意な方向を理論的に仮定しないため、両者はsecondary outcomeとして記録する。

## 7. Main generation

Response generatorには以下だけを与える。

1. current Situation
2. fixed Experience packet
3. Response output schema

生成対象はResponseだけとする。

実装時には、Action、Intensity、Latencyをmachine-readableに取得できるschemaを固定する。

禁止事項：

- Situationの再解釈だけを返しActionを生成しない
- Experienceを言い換えるだけでActionを生成しない
- 現在Situationに存在しない外部事実を追加する
- 上流状態を新たに設定する
- condition labelをResponse本文へ反復する

## 8. Main evaluation construct

主要評価軸はActionの意味方向を測る。

### Constructive Engagement

`constructive_engagement` 0–4

現在の相手・課題・出来事に対して、対話、確認、協力、質問、接近、関与継続等を通じて関係・課題へ働きかける程度。

### Protective Distancing

`protective_distancing` 0–4

現在の相手・課題・出来事に対して、保留、拒否、距離確保、情報制限、回避、防御等によって自己・資源・境界を守る方向へ動く程度。

二軸は一つの連続尺度の両極と仮定しない。

例えば「必要情報だけ確認し、それ以上の共有は保留する」はConstructive EngagementとProtective Distancingの両方を含み得る。

品質評価として次を別尺度で記録する。

- `non_action_leakage` 0–4
- `external_fact_invention` 0–4

補助評価としてIntensity / Latency、二軸のcoactivation等を記録してよいが、confirmatory gateの代替には用いない。

## 9. Blind evaluation

評価セット作成時に次をblind化する。

- E-B / E-A condition label
- Experience packet
- family内pair identity
- generation order

Blind evaluatorには次だけを与える。

1. current Situation
2. generated Response

EvaluatorはResponseのAction意味を `constructive_engagement` / `protective_distancing` で評価する。

Experienceを見せないことで、「このExperienceならこのResponseであるべき」という評価側のcondition leakageを避ける。

## 10. Sample size

pilot-001では次を計画する。

- 8 scenario families
- 2 Experience conditions
- 3 replicates per cell

Main generation:

`8 × 2 × 3 = 48 Responses`

Blind evaluation:

`48 Responses`

Pretestは評価対象を混ぜないため分離する。

- Experience quality: `8 × 2 = 16`
- Situation affordance boundary: `8`
- total: `24`

予定最小API評価単位は `24 + 48 + 48 = 120`。

## 11. Pretest

main generation前に二種類のpretestを別評価として実施する。

### 11.1 Experience quality pretest

`8 families × 2 Experience conditions = 16 packets`

EvaluatorにはSituationとExperience packetを提示する。

Response生成は行わない。

#### P1 Experience separation

E-BがE-AよりBenign / Low-risk meaningを強く表し、E-AがE-BよりAdverse / High-risk meaningを強く表すこと。

planned thresholds:

- Benign meaning separation `>= 2.0`
- Adverse meaning separation `>= 2.0`
- correct family direction `>= 7 / 8`

評価尺度は実装時に0–4で固定する。

#### P2 No Response directiveness

Experience packetが現在のAction、意思決定、行動計画、Intensity / Latencyを直接指示しないこと。

- mean `<= 0.50`
- max `<= 1`

#### P3 No external-fact leakage

Experience packetがcurrent Situationに存在しない外部事実をResponse選択の根拠として追加していないこと。

- mean `<= 0.50`
- max `<= 1`

主観的意味と外部事実を区別する。「危険に感じる」はExperienceとして許容するが、「相手が実際に嘘をついていた」等の未提示事実は許容しない。

#### P4 Upstream-state isolation

Experience packetが、target Experienceの原因として上流状態を同時に設定していないことを別尺度で確認する。

- Values & Beliefs preload: mean `<= 0.50`, max `<= 1`
- Relationship preload: mean `<= 0.50`, max `<= 1`
- Temperament preload: mean `<= 0.50`, max `<= 1`

P4は、E-B / E-Aの差が「Experience packetに埋め込まれた別のCharacter state」になっていないことを確認するGateとする。

### 11.2 Situation affordance boundary pretest

`8 families = 8 Situations`

EvaluatorにはSituationだけを提示し、Experience packetを与えない。

#### P5 Situation affordance boundary

Situationの外部事実・制約だけでConstructive EngagementまたはProtective Distancingのどちらかが事実上強制されていないこと。

`response_direction_constraint` 0–4で評価する。

planned thresholds:

- mean `<= 0.50`
- max `<= 1`

P5は「SituationがResponseへ影響しない」ことを要求しない。正本v1.2ではSituationはResponseの直接入力である。

要求するのは、**同一Situation内でExperience差によるResponse変化を観測できる選択余地が残っていること**である。

P1〜P5のいずれかがFAILした場合、main generationへ進まない。

## 12. Confirmatory hypothesis

### H-ER01 — Experience meaning effect on Response

Situationを固定したとき、Experienceの主観的意味の差はResponseのAction意味を対応方向へ変化させる。

予測：

- E-BはE-AよりConstructive Engagementを高める
- E-AはE-BよりProtective Distancingを高める

主要効果量：

`Delta_C = mean(C_E-B) - mean(C_E-A)`

`Delta_P = mean(P_E-A) - mean(P_E-B)`

family別効果：

`Delta_C_f = mean(C_E-B,f) - mean(C_E-A,f)`

`Delta_P_f = mean(P_E-A,f) - mean(P_E-B,f)`

Leave-one-family-outでは各familyを一つずつ除外し、残り7 familyで `Delta_C` / `Delta_P` を再計算する。

## 13. Main confirmatory gates

### G1 Constructive Engagement effect

`Delta_C >= 0.75`

### G2 Protective Distancing effect

`Delta_P >= 0.75`

### G3 Family generalization

8 family中6以上で同一family内において、

- `Delta_C_f > 0`
- `Delta_P_f > 0`

を同時に満たす。

### G4 Leave-one-family-out robustness

全leave-one-family-out集合で、

- `Delta_C > 0`
- `Delta_P > 0`

を維持する。

### G5 Response boundary quality

生成ResponseがResponseとして成立し、Situation外の事実を新たな判断根拠として発明していないことを確認する。

- non-action leakage mean `<= 0.50`, max `<= 1`
- external-fact invention mean `<= 0.50`, max `<= 1`

Overall PASSはG1〜G5の全PASSとする。

## 14. Secondary analysis

confirmatory判定後にのみ探索的に確認してよい項目：

- Response Intensityのcondition mean差
- Response Latencyのcondition mean差
- Constructive Engagement / Protective Distancingのcoactivation率
- family別のActionカテゴリ分布
- Experience packetとResponseの単純な語彙反復

これらはpilot-001のPASS / FAILを変更しない。

探索結果から新しい仮説を立てる場合は、後続pilotまたは別実験で事前登録する。

## 15. Freeze and failure rule

実装PRで次をmachine-readableまたはhash可能な形に固定する。

- experiment configuration
- stimuli / Experience packets
- thresholds
- generation prompt
- pretest prompt
- blind evaluation prompt
- output schemas
- randomization seeds
- model identifiers

pilot-001 pretest開始後にdesignを変更しない。

pretest FAILの場合：

- mainを実行しない
- thresholdを緩和しない
- stimulus / Experience packetを同pilot内で修正して再実行しない
- 修正版はpilot-002等の新しい監査単位として扱う

main FAILの場合も、実行後にGateや評価軸を変更してPASSへ再分類しない。

## 16. Relation to PF-EXP-0005 / 0006

PF-EXP-0005は、同一Situation / Perception / neutral RelationshipでValues & Beliefsを操作し、Experience差を確認した。

PF-EXP-0006は、同一Situation / Perception / target-neutral Values & BeliefsでRelationship内のTrust状態を操作し、Experience差を確認した。

PF-EXP-0007は、これらのgenerated Experienceをそのまま再利用して媒介分析する実験ではない。

独立した実験として、fixed Situationに対して事前に定義したE-B / E-A Experience packetを直接与え、Response差を測る。

したがってPF-EXP-0007がPASSしても、

`VB / Rel → Experience → Response`

という媒介経路全体が一つの連続実験で検証済みになったとは扱わない。

一方、PF-EXP-0005 / 0006 / 0007がそれぞれPASSした場合、v1.2の中核変数間に**個別操作による連続した機能的証拠**が蓄積した、と限定して解釈できる。

## 17. Interpretation boundary

PASSした場合に直接支持するのは、

> **固定されたSituationのもとで、Benign / Low-riskとAdverse / High-riskというExperienceの主観的意味の違いが、ResponseのAction意味を再現可能かつ方向整合的に変え得る。**

という主張である。

本pilotだけでは次を主張しない。

- ExperienceがResponseの唯一の原因である
- SituationのResponseへの直接寄与が不要である
- Experienceの全次元が同様にResponseへ作用する
- Intensity / Latencyの方向効果が確立した
- PF-EXP-0005 / 0006からResponseまでの自然な媒介過程が検証済みである
- Values & Beliefs / Relationshipの自然形成・更新からResponseまで再現できる
- 人間へ一般化できる
- 別モデルまたは人手Evaluatorでも再現する

## 18. Model implication

PASSした場合、Personality Formation Model v1.2の

`R_t = g(E_t, Sit_t)`

における `E_t → R_t` の条件付き寄与に経験的支持を追加できる。

ただしSituationも同式の入力であるため、本実験は `Sit_t → R_t` を検証・否定しない。

FAILした場合も、`Experience → Response` の一般的不存在を直ちに意味しない。Experience contrast、scenario bank、Response評価軸、LLM実験系の感度等を分けて監査し、必要なら新しいpilotとして再設計する。

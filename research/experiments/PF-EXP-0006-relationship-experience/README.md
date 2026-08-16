# PF-EXP-0006 — Relationship → Experience

> Status: **pilot-001 completed / overall PASS**  
> Canonical Model: [APRL Personality Formation Model v1.2](../../../docs/models/Personality_Formation_Model.md)  
> Target relation: `E_t = h(P_t, VB_t, Rel_t)`  
> Isolated contribution: `Rel_t → E_t`  
> Result report: [pilot-001 summary](reports/pilot-001-summary.md)

## Research Question

> **同一のSituationとPerception、同一のValues & Beliefsのもとで、Relationshipの違いは、その出来事がCharacterにとって持つExperienceの意味を再現可能かつ方向整合的に変えるか。**

PF-EXP-0005 pilot-002で `VB_t → E_t` の条件付き寄与が支持されたため、本実験ではもう一つのExperience入力であるRelationshipを単独操作した。

## Result

pilot-001はpretest P1〜P5とmain confirmatory gate G1〜G5をすべてPASSし、**Overall PASS**となった。

主要結果：

- Trust separation: `3.125`
- Distrust separation: `3.0`
- pretest family direction: `8 / 8`
- generalized VB / Closeness-Affection / Power-Dependency leakage: mean / maxすべて `0.0`
- Perception meaning preload: mean / max `0.0`
- `Delta_B = 2.5833`
- `Delta_S = 2.0417`
- main family generalization: `8 / 8`
- min LOO `Delta_B = 2.4762`
- min LOO `Delta_S = 1.9048`
- Response leakage: mean `0.125`, max `1.0`

この結果は、今回の実験条件において、**固定されたSituation・Perception・target-neutral Values & Beliefsのもとで、特定相手とのTrust状態の違いがExperienceの意味を対応する方向へ変化させ得る**ことを支持する。

詳細なGate、family effects、LOO、design hash、解釈境界は [pilot-001 summary](reports/pilot-001-summary.md) を正とする。

## pilot-001 scope

Relationship全体を最初から多次元ベクトルとして固定せず、pilot-001では **Trust一軸だけ**を検証した。

- **REL-T — Trusting Relationship**: 特定相手の発言・説明・約束の信頼性を高く見積もる
- **REL-D — Distrustful Relationship**: 同じ相手の発言・説明・約束の信頼性を低く見積もる

Trust以外のRelationship候補を同時に動かさないよう、Trust packetには親密さ・好意・上下関係・依存等を条件差として含めなかった。

## Input set policy

8 scenario familiesはTrust専用にせず、可能な範囲で **relationship-generic** に設計した。

各familyでは次を固定した。

- Situation
- Perception
- Values & Beliefs: `none / neutral`
- counterpart identity / external constraints
- generation prompt template

操作したのはRelationshipのTrust状態だけである。TemperamentはExperience生成時には与えていない。

将来別Relationship次元を検証するときは、Situation / Perception / Values & Beliefsを固定したまま、その次元だけをRelationshipとして操作できる場合に同じscenario bankを再利用できる。

Power / Roleの操作が外的な権限・制度上の役割・資源制約そのものを変える場合、それはSituation側の操作になり得るため、同じstimulusの再利用を強制しない。**比較可能性より因果分離を優先する。**

## Scenario families

pilot-001では次の8つの社会的曖昧性を用いた。具体文は [`stimuli.yaml`](stimuli.yaml) を正とする。

1. 案への見直し要求
2. 予定変更
3. 作業中資料へのアクセス要求
4. 返答の遅れと説明
5. 異なる進め方の提案
6. 作業代行の申し出
7. 判断への再確認
8. 話題の持ち越し

Situation / Perceptionには、善意・悪意、裏切り、操作、親密さ、権威等のRelationship-level結論を先取りしない。

## Confirmatory Hypothesis

### H-REL01 — Trust state effect on Experience

Situation、Perception、Values & Beliefsを固定したとき、**特定相手とのTrust状態の違いは、生成されるExperienceの意味を対応する方向へ変化させる。**

主要評価軸：

- `benign_good_faith_meaning` 0–4
- `suspicious_adverse_intent_meaning` 0–4

主要効果量：

`Delta_B = mean(B_REL-T) - mean(B_REL-D)`

`Delta_S = mean(S_REL-D) - mean(S_REL-T)`

## Sample size

- 8 scenario families
- 2 Trust conditions
- 3 replicates per cell
- main evaluation: `48 Experiences`
- pretest: Relationship quality `16` + Perception boundary `8` = `24`

## Frozen pretest gates

数値は [`thresholds.yaml`](thresholds.yaml) を正とし、実行後に変更しない。

- **P1 Trust separation**
  - Trust separation `>= 2.0`
  - Distrust separation `>= 2.0`
  - correct family direction `>= 7 / 8`
- **P2 No current-response directiveness**
  - mean `<= 0.50`, max `<= 1`
- **P3 No current-situation leakage**
  - mean `<= 0.50`, max `<= 1`
- **P4 Trust isolation**
  - generalized-VB leakage mean `<= 0.50`, max `<= 1`
  - closeness / affection leakage mean `<= 0.50`, max `<= 1`
  - power / dependency leakage mean `<= 0.50`, max `<= 1`
- **P5 Perception boundary**
  - Trust-dependent Experience meaning preload mean `<= 0.50`, max `<= 1`

## Frozen confirmatory gates

- **G1 Benign / good-faith meaning effect**: `Delta_B >= 0.75`
- **G2 Suspicious / adverse-intent meaning effect**: `Delta_S >= 0.75`
- **G3 Family generalization**: 8 family中6以上で両effect `> 0`
- **G4 Leave-one-family-out robustness**: 全LOOで両effect `> 0`
- **G5 Experience boundary quality**: response leakage mean `<= 0.50`, max `<= 1`

**Overall PASSはG1〜G5の全PASSとする。pilot-001は全GateをPASSした。**

## Interpretation boundary

本pilotが直接支持するのは、

> **固定されたSituation・Perception・target-neutral Values & Beliefsのもとで、特定相手とのTrust状態の違いがExperienceの意味を再現可能かつ方向整合的に変え得る。**

という限定された主張である。

本実験だけでは次を主張しない。

- Relationship全体がTrust一軸で十分である
- Trust以外のRelationship次元へ一般化できる
- Relationshipの自然な形成・更新機構
- Relationshipが自然なPerception形成へ影響しない
- `Experience → Response`
- 人間への一般化
- 独立Evaluatorまたは人手評価での再現

Generation、pretest、blind evaluationはいずれも`gpt-5.6`を用いているため、独立Evaluator / 人手blind評価による堅牢性確認は未実施である。

## Audit policy

- Gate / threshold / stimulus / prompt / schemaを実行後に変更しない
- Raw responsesは公開しない
- Gate判定後の探索分析はconfirmatory resultと分離する
- PF-EXP-0001〜0005の実行済み結果を変更しない
- 将来のRelationship次元検証を理由にpilot-001のstimulus、Gate、閾値、結果を書き換えない

詳細な計画上の根拠と設計ルールは [`protocol.md`](protocol.md) を参照する。

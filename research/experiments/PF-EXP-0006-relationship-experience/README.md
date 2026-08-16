# PF-EXP-0006 — Relationship → Experience

> Status: **pilot-001 implementation ready / pretest not run**  
> Canonical Model: [APRL Personality Formation Model v1.2](../../../docs/models/Personality_Formation_Model.md)  
> Target relation: `E_t = h(P_t, VB_t, Rel_t)`  
> Isolated contribution: `Rel_t → E_t`

## Research Question

> **同一のSituationとPerception、同一のValues & Beliefsのもとで、Relationshipの違いは、その出来事がCharacterにとって持つExperienceの意味を再現可能かつ方向整合的に変えるか。**

PF-EXP-0005 pilot-002で `VB_t → E_t` の条件付き寄与が支持されたため、本実験ではもう一つの未検証入力であるRelationshipを単独操作する。

## pilot-001 scope

Relationship全体を最初から多次元ベクトルとして固定しない。pilot-001では **Trust一軸だけ**を検証する。

- **REL-T — Trusting Relationship**: 特定相手の発言・説明・約束の信頼性を高く見積もる
- **REL-D — Distrustful Relationship**: 同じ相手の発言・説明・約束の信頼性を低く見積もる

Trustだけでは説明できない差が確認された場合に、Closeness、Power / Role等を個別に検証する。これらは現時点では正本変数として採用しない。

## Input set policy

8 scenario familiesはTrust専用にせず、可能な範囲で **relationship-generic** に設計する。

各familyでは次を固定する。

- Situation
- Perception
- Values & Beliefs: `none / neutral`
- counterpart identity / external constraints
- generation prompt template

操作するのはRelationshipのTrust状態だけである。TemperamentはExperience生成時には与えない。

Trust packetには、現在Situation固有の事実、現在Response、具体的な過去Episodeを含めない。また、親密さ・好意・上下関係・依存等を条件差として同時に操作しない。

将来別Relationship次元を検証するときは、Situation / Perception / Values & Beliefsを固定したまま、その次元だけをRelationshipとして操作できる場合に同じscenario bankを再利用する。

Power / Roleの操作が外的な権限・制度上の役割・資源制約そのものを変える場合、それはSituation側の操作になり得るため、同じstimulusの再利用を強制しない。**比較可能性より因果分離を優先する。**

## Scenario families

pilot-001では次の8つの社会的曖昧性を用いる。具体文は [`stimuli.yaml`](stimuli.yaml) を正とする。

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

主要評価軸はblind evaluatorによる次の2軸とする。

- `benign_good_faith_meaning` 0–4
- `suspicious_adverse_intent_meaning` 0–4

主要効果量：

`Delta_B = mean(B_REL-T) - mean(B_REL-D)`

`Delta_S = mean(S_REL-D) - mean(S_REL-T)`

## Sample size

- 8 scenario families
- 2 Trust conditions
- 3 replicates per cell

Main generation:

`8 × 2 × 3 = 48 Experiences`

Blind evaluation:

`48 Experiences`

Pretestは測定対象を混ぜないため分離する。

- Relationship quality: `8 × 2 = 16`
- Perception boundary: `8`
- total: `24`

予定最小API評価単位は **24 + 48 + 48 = 120**。

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

Relationship quality pretestではSituation + Relationshipだけを評価する。Perception boundary pretestではSituation + Perceptionだけを評価し、Relationshipを提示しない。

**P1〜P5のどれかがFAILした場合、main generationへ進まない。**

## Frozen confirmatory gates

- **G1 Benign / good-faith meaning effect**: `Delta_B >= 0.75`
- **G2 Suspicious / adverse-intent meaning effect**: `Delta_S >= 0.75`
- **G3 Family generalization**: 8 family中6以上で両effect `> 0`
- **G4 Leave-one-family-out robustness**: 全LOOで両effect `> 0`
- **G5 Experience boundary quality**: response leakage mean `<= 0.50`, max `<= 1`

**Overall PASSはG1〜G5の全PASSとする。**

## Execution flow

実験ディレクトリから次の順に実行する。

```powershell
python -m src.validate
pytest
python -m src.pretest --dry-run
python -m src.pretest
python -m src.pretest_analyze
```

`all_gates_pass = true` の場合のみmainへ進む。

```powershell
python -m src.pilot --dry-run
python -m src.pilot
python -m src.blind
python -m src.evaluate --dry-run
python -m src.evaluate
python -m src.analyze
```

`src.pilot` はpretest時のdesign hashと現在のdesign hashが一致しない場合にも停止する。

## Interpretation boundary

PASSした場合に支持するのは、

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

## Audit policy

- Gate / threshold / stimulus / prompt / schemaを実行前に固定する
- Raw responsesは公開しない
- Blind keyはevaluation完了までanalysisから分離する
- Gate判定後の探索分析はconfirmatory resultと分離する
- FAIL後に同pilotのGateを緩和しない
- PF-EXP-0001〜0005の実行済み結果を変更しない
- 将来の再利用可能性を理由にpilot-001のstimulusを事後変更しない

詳細な計画上の根拠と設計ルールは [`protocol.md`](protocol.md) を参照する。

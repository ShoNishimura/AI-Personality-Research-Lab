# PF-DISC-0002 — Trust shapes Experience

> Status: **supported in PF-EXP-0006 pilot-001**  
> Source experiment: [PF-EXP-0006](../experiments/PF-EXP-0006-relationship-experience/)  
> Result report: [pilot-001 summary](../experiments/PF-EXP-0006-relationship-experience/reports/pilot-001-summary.md)

## Discovery

固定されたSituation・Perception・target-neutral Values & Beliefsのもとでも、特定相手とのTrust状態の違いは、生成されるExperienceの意味を再現可能かつ方向整合的に変え得る。

PF-EXP-0006 pilot-001では、Trusting Relationship（REL-T）とDistrustful Relationship（REL-D）を操作し、次を観測した。

- `Delta benign / good-faith = 2.5833`
- `Delta suspicious / adverse-intent = 2.0417`
- 8 / 8 scenario familiesで両方向のeffectが正
- 全leave-one-family-outで両effectが正
- Response leakageは事前Gate内
- pretest P1〜P5、main G1〜G5をすべてPASS

## Model implication

この結果は、Personality Formation Model v1.2の

`E_t = h(P_t, VB_t, Rel_t)`

のうち、**Relationship内のTrust状態による `Rel_t → E_t` の条件付き寄与**を支持する。

PF-EXP-0005の `VB_t → E_t` と合わせると、同一Perceptionを固定したまま、Values & BeliefsとRelationshipのTrust状態を別々に操作してExperience差が生じ得ることが確認された。現時点では、`VB_t` と `Rel_t` をExperienceの独立入力として保持するv1.2の構造と整合する。

## Boundary

このDiscoveryは次を意味しない。

- Relationship全体がTrust一軸で十分である
- Trust以外のRelationship次元へ一般化できる
- Relationshipの自然な形成・更新機構が検証済みである
- Relationshipが自然なPerception形成へ作用しない
- `Experience → Response` が検証済みである
- 人間でも同じ効果量が成立する
- 独立したモデルや人手Evaluatorでも同じ結果が再現される

Generation、pretest、blind evaluationにはいずれも`gpt-5.6`を用いた。独立Evaluatorまたは人手blind評価による再評価は未実施である。

## Secondary observation

REL-TのExperience valenceはREL-Dより高かった一方、arousal差は小さかった。`dual_meaning_coactivation_rate = 0.0208`、Relationship lexical repetition meanは`0.0433`だった。これらはconfirmatory resultではなく探索的観察として扱う。

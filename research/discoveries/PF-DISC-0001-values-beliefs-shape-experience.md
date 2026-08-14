# PF-DISC-0001 — Values & Beliefs shape Experience

> Status: **supported in PF-EXP-0005 pilot-002**  
> Source experiment: [PF-EXP-0005](../experiments/PF-EXP-0005-values-beliefs-experience/)  
> Result report: [pilot-002 summary](../experiments/PF-EXP-0005-values-beliefs-experience/reports/pilot-002-summary.md)

## Discovery

固定されたSituation・Perception・neutral Relationshipのもとでも、Values & Beliefsの違いは、生成されるExperienceの意味を再現可能かつ方向整合的に変え得る。

PF-EXP-0005 pilot-002では、Learning / Improvement orientation（VB-L）とEvaluation / Competence-protection orientation（VB-E）を操作し、次を観測した。

- `Δ Learning meaning = 3.5417`
- `Δ Evaluation threat = 2.5833`
- 8 / 8 scenario familiesで両方向のeffectが正
- 全leave-one-family-outで両effectが正
- ExperienceからResponseへのleakageは事前Gate内
- pretest P1〜P5、main G1〜G5をすべてPASS

## Model implication

この結果は、Personality Formation Model v1.2の

`E_t = h(P_t, VB_t, Rel_t)`

のうち、**`VB_t → E_t` の条件付き寄与**を支持する。

また、同じPerceptionを固定したままValues & Beliefsのみを変えてExperience差が生じたため、PerceptionとExperienceを機能的に分離する現行モデルにも限定的な経験的支持を与える。

## Boundary

このDiscoveryは次を意味しない。

- PerceptionとExperienceが人間心理において完全に離散した二段階である
- `Relationship → Experience` が検証済みである
- Learning / Evaluation以外のValues & Beliefsへ一般化できる
- 人間でも同じ効果量が成立する
- 独立したモデルや人手Evaluatorでも同じ結果が再現される

Generationとblind evaluationにはともに`gpt-5.6`を用いた。独立Evaluatorまたは人手blind評価による再評価は未実施である。

## Secondary observation

`dual_meaning_coactivation_rate = 0.25` を観測した。Learning meaningとEvaluation-threat meaningが同一Experience内で共存し得る可能性を示唆するが、confirmatory resultではなく探索的観察として扱う。

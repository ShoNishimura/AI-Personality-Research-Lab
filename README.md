# AI Personality Research Lab

> 人工人格を通して、人間理解を深める。

AI Personality Research Lab（APRL）は、人工人格を実験系として用い、
「人はなぜ、ある人格に心を動かされるのか」を探究する研究プロジェクトです。

人格がExperienceを固有にInterpretationし、Regulationを経てResponseを重ねる過程と、その軌跡であるBiography、さらにAudienceに生じるBiographical Resonanceを研究対象とします。Storyは直接設計する目的ではなく、Character同士の相互作用から創発する結果として扱います。

## Canonical model

現在の正本は [APRL Concept Model v1.0 — Canonical Edition](docs/concept-model/APRL_Concept_Model_v1.0_Canonical_Edition.md) です。

APRLの公開Canonical versioningはこのv1.0から開始します。以後の議論、設計、用語および実験は、原則としてこの版との整合性を確認します。

### Core model

```text
Temperament T₀ = (S, N)

S: Surgency-derived Approach Reactivity
N: Negative Affectivity-derived Aversion Reactivity
                         │
                         ▼
Experience → Interpretation → Regulation → Response
                                         (Action, Intensity, Latency)
                         │
                         └──────────────→ Biography
```

- **Temperament** は基礎的なmotivational-emotional reactivityの初期条件として、SとNの2要素で表します。
- **S** は理論上の由来である **Surgency / Extraversion** の頭文字を保持し、APRLでは **Approach Reactivity** として再定義します。
- **N** は理論上の由来である **Negative Affectivity** の頭文字を保持し、APRLでは **Aversion Reactivity** として再定義します。
- **Regulation** はTemperamentから分離し、ResponseのAction、Intensity、Latencyを調整する可変的な機能として扱います。
- **Relationship** は複数Character間に形成される時間依存の状態として扱い、Affiliationは必要に応じてRelationship Modelで検証します。

### Temperamentを直感的に見る

記号S/NはAPRLで再定義した名称の頭文字ではなく、理論的な由来を追跡できるよう元概念の頭文字を保持しています。

```text
S → Surgency / Extraversion → Approach Reactivity
N → Negative Affectivity     → Aversion Reactivity
```

- **S = Approach Reactivity** — 報酬、新奇性、快、機会などに対して「近づく」方向の反応が起こりやすい。
- **N = Aversion Reactivity** — 脅威、喪失、拒絶、不快などに対して嫌悪・警戒・防御方向の反応が起こりやすい。

たとえば、**「未知の対象を見つけた」**という同じExperienceでも、初期反応の偏りは次のように変わります。

| S | N | 起こりやすい初期傾向 | 直感的な例 |
|---|---|---|---|
| High | Low | 接近が強く、警戒が弱い | 興味を持ってすぐ近づき、触ったり調べたりする |
| High | High | 接近と警戒がともに強い | 強く興味を持つが、危険も感じながら慎重に近づく |
| Low | High | 接近が弱く、警戒が強い | 距離を取り、観察するか回避する |
| Low | Low | 接近・警戒ともに弱い | 強く反応せず、必要が生じるまで様子を見る |

SとNは行動を直接決めるルールではありません。同じTemperamentでも、それまでのExperience、Interpretation、Relationship、Regulationなどによって最終的なResponseは変わります。

## Repository guide

| Path | Role |
|---|---|
| [`docs/`](docs/) | 正本と、現在参照する補助文書 |
| [`research/notes/`](research/notes/) | 問い、仮説、未確定の考察 |
| [`research/experiments/`](research/experiments/) | 実験設計、実行記録、分析、報告 |
| [`research/discoveries/`](research/discoveries/) | 実験から得られた根拠付きの発見 |
| [`research/legacy/`](research/legacy/) | 旧モデルに基づく研究資料（非現行） |

研究は `notes → experiments → discoveries` と進み、十分に検証された知見だけを `docs` へ反映します。詳しくは [research/README.md](research/README.md) を参照してください。

## Reading order

1. [APRL Concept Model v1.0](docs/concept-model/APRL_Concept_Model_v1.0_Canonical_Edition.md)
2. [Manifesto](docs/manifesto.md)
3. [Philosophy](docs/philosophy.md)
4. [Glossary](docs/glossary.md)

`personality-theory.md` と `ai-personality-blueprint.md` は旧概念を含むため、正本との整合確認が完了するまで参考資料として扱います。

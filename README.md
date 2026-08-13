# AI Personality Research Lab

> **人工人格を通して、人間理解を深める。**

AI Personality Research Lab（APRL）は、人工人格を実験系として用い、

**「人はなぜ、その人に心を動かされるのか。」**

を探究する研究プロジェクトです。

## Two-level research structure

APRLは、研究全体の地図と、個別の検証モデルを分けて管理します。

| Layer | Role | Current canonical |
|---|---|---|
| **APRL Research Framework** | GRQと、Creator / Character / Relationship / Biography / Communicator / Audience / Resonanceの位置関係を定義 | [v1.0.1](docs/APRL_Research_Framework.md) |
| **Research Model** | Frameworkの一部分を検証可能な形へ具体化 | [Personality Formation Model v1.1](docs/models/Personality_Formation_Model.md) |

上位Frameworkはできるだけ安定させ、下位Research Modelは実験に応じて独立して改訂します。

## Current Research Focus

現在のPrimary Research Trackは **Personality Formation** です。

中心的な問いは、

**「人格はどのように形成されるのか。」**

です。

現行の最小モデルは、次の二つの関係を核にします。

$$
P_t=f(E_t,T_0)
$$

$$
R_t=g(P_t,H_t,Rel_t)
$$

```text
                Temperament T0 = (S, N)
                         │
                         ▼
Experience_t ───────► Perception_t ───────► Response_t
                                             ▲       ▲
                                             │       │
                                         History_t  Relationship_t

Response_t ──► next Experience / History / Relationship
                         │
                         ▼
                      Biography
```

- **S = Seeking Reactivity** — 報酬、新奇性、快、機会などを求め、探索しようとする反応性。Surgency / Extraversionを主要な理論的起点とします。
- **N = Negative Affectivity** — 脅威、喪失、拒絶、不快などに対してネガティブ情動が活性化しやすい反応性です。
- **Perception** — Experienceのうち何がsalientになり、どのようなmotivational-emotional significanceとして感じ取られるか。
- **History / Relationship** — 同じPerceptionに対して、CharacterがどのResponseを選ぶかを変え得る時間依存の文脈です。

### S / N を直感的に見る

同じ「未知の対象を見つけた」というExperienceでも、Perceptionの偏りは次のように変わり得ます。

| S | N | 起こりやすいPerception | 直感的なイメージ |
|---|---|---|---|
| High | Low | 機会・新奇性が強くsalient、危険は比較的弱い | 「面白そう。価値がありそう」 |
| High | High | 機会と危険の双方が強くsalient | 「すごく気になる。でも危険でもある」 |
| Low | High | 機会への反応は弱く、脅威・損失が強くsalient | 「危険かもしれない」 |
| Low | Low | いずれも強くsalientになりにくい | 「今すぐ反応するほどではない」 |

SとNは行動を直接決めるルールではありません。TemperamentはPerceptionを偏らせ、最終的なResponseはPerception、History、Relationshipによって変わります。

C / Regulationは現行Minimum Modelの独立変数には置きません。Perception、History、RelationshipだけではResponse差を説明できない必要性が実証された場合に再検討します。

## APRL Research Framework

APRL全体では、概念的に次の領域を扱います。

```text
Creator
   │
World / Initial Conditions
   │
   ▼
Character(s) ↔ Relationship
   │
   ▼
Biography
   │
   ▼
Communicator
   │
   ▼
Audience
   │
   ▼
Resonance
```

現在はこのうち、**Character / Biographyがどのように形成されるか**に研究対象を絞っています。

## Experiment continuity

PF-EXP-0001〜0003は、実行時には生成対象を `Interpretation` と呼んでいました。

Personality Formation Model v1.1では、それらの実験で観測していたOpportunity / Danger Salience、Seeking / Negative Activationを **Perceptionの観測**として再位置づけます。

実行済みのprompt、schema、config、raw artifactのfield名、Gate、閾値、hash、集計結果は監査記録のため変更しません。

## Repository guide

| Path | Role |
|---|---|
| [`docs/`](docs/) | 現行正本。Research Framework / Research Models / Glossary |
| [`research/notes/`](research/notes/) | 現行モデルに整合する問い・仮説 |
| [`research/experiments/`](research/experiments/) | 現行モデルを検証する実験 |
| [`research/discoveries/`](research/discoveries/) | 現行系列の根拠付きの発見 |
| [`research/legacy/`](research/legacy/) | 旧版・旧モデル・旧実験の隔離Archive |

研究は `notes → experiments → discoveries → docs/models` と進め、十分に検証された知見だけを正本へ反映します。

## Canonical documents

1. [APRL Research Framework v1.0.1](docs/APRL_Research_Framework.md)
2. [Personality Formation Model v1.1](docs/models/Personality_Formation_Model.md)
3. [Glossary](docs/glossary.md)

単一の旧 `APRL Concept Model v1.0` は二段構造へ置き換え、[Legacy Archive](research/legacy/concept-model-v1/) に保存しています。

旧 `T0=(S,N,C)` 系列のEXP-0001も、最新の監査記録を含めて [canonical-v1 archive](research/legacy/canonical-v1/) に隔離しています。
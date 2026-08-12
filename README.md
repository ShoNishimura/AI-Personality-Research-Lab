# AI Personality Research Lab

> **人工人格を通して、人間理解を深める。**

AI Personality Research Lab（APRL）は、人工人格を実験系として用い、

**「人はなぜ、その人に心を動かされるのか。」**

を探究する研究プロジェクトです。

## Two-level research structure

APRLは、研究全体の地図と、個別の検証モデルを分けて管理します。

| Layer | Role | Current canonical |
|---|---|---|
| **APRL Research Framework** | GRQと、Creator / Character / Relationship / Biography / Communicator / Audience / Resonanceの位置関係を定義 | [v1.0](docs/APRL_Research_Framework.md) |
| **Research Model** | Frameworkの一部分を検証可能な形へ具体化 | [Personality Formation Model v1.0](docs/models/Personality_Formation_Model.md) |

上位Frameworkはできるだけ安定させ、下位Research Modelは実験に応じて独立して改訂します。

## Current Research Focus

現在のPrimary Research Trackは **Personality Formation** です。

中心的な問いは、

**「人格はどのように形成されるのか。」**

です。

現行の最小モデルは次の循環を扱います。

```text
Temperament T0 = (S, N)
          │
          ▼
Experience → Interpretation → Regulation → Response
    ▲                                      │
    └──────────── next Experience ◄────────┘
                         │
                         ▼
                      Biography
```

- **S = Seeking Reactivity** — 報酬、新奇性、快、機会などを求め、探索しようとする反応性。Surgency / Extraversionを主要な理論的起点とします。
- **N = Negative Affectivity** — 脅威、喪失、拒絶、不快などに対してネガティブ情動が活性化しやすい反応性です。
- **Regulation** — ResponseのAction、Intensity、Latencyを抑制・保留・選択・調整する可変的な機能です。

### S / N を直感的に見る

同じ「未知の対象を見つけた」というExperienceでも、初期反応の偏りは次のように変わります。

| S | N | 起こりやすい初期傾向 | 直感的な例 |
|---|---|---|---|
| High | Low | 探索・希求が強く、警戒が弱い | 興味を持ってすぐ近づき、触ったり調べたりする |
| High | High | 探索・希求とネガティブ情動がともに強い | 強く知りたい一方で危険も感じ、慎重に近づく |
| Low | High | 探索・希求が弱く、ネガティブ情動が強い | 距離を取り、観察するか回避する |
| Low | Low | 両方の反応性が比較的弱い | 強く反応せず、必要が生じるまで様子を見る |

SとNは行動を直接決めるルールではありません。同じTemperamentでも、Experience、Interpretation、履歴、Relationship、Regulationによって最終的なResponseは変わります。

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

1. [APRL Research Framework v1.0](docs/APRL_Research_Framework.md)
2. [Personality Formation Model v1.0](docs/models/Personality_Formation_Model.md)
3. [Glossary](docs/glossary.md)

単一の旧 `APRL Concept Model v1.0` は二段構造へ置き換え、内容を変更せず [Legacy Archive](research/legacy/concept-model-v1/) に保存しています。

旧 `T0=(S,N,C)` 系列のEXP-0001も、最新の監査記録を含めて [canonical-v1 archive](research/legacy/canonical-v1/) に隔離しています。
# AI Personality Research Lab

> **人工人格を通して、人間理解を深める。**

AI Personality Research Lab（APRL）は、人工人格を実験系として用い、

**「人はなぜ、その人に心を動かされるのか。」**

を探究する研究プロジェクトです。

## Two-level research structure

APRLは、研究全体の地図と、個別の検証モデルを分けて管理します。

| Layer | Role | Current canonical |
|---|---|---|
| **APRL Research Framework** | GRQと、Creator / Character / Relationship / Biography / Communicator / Audience / Resonanceの位置関係を定義 | [v1.0.2](docs/APRL_Research_Framework.md) |
| **Research Model** | Frameworkの一部分を検証可能な形へ具体化 | [Personality Formation Model v1.2](docs/models/Personality_Formation_Model.md) |

上位Frameworkはできるだけ安定させ、下位Research Modelは実験に応じて独立して改訂します。

## Current Research Focus

現在のPrimary Research Trackは **Personality Formation** です。

中心的な問いは、

**「人格はどのように形成されるのか。」**

です。

現行の最小モデルは、次の三つの関係を核にします。

$$
P_t=f(Sit_t,T_0)
$$

$$
E_t=h(P_t,VB_t,Rel_t)
$$

$$
R_t=g(E_t,Sit_t)
$$

```text
                         Temperament T0 = (S, N)
                                  │
                                  ▼
World ──► Situation_t ──► Perception_t ──► Experience_t ──► Response_t
            │                                      ▲             │
            │                                      │             │
            │                            Values & Beliefs_t       │
            │                              Relationship_t         │
            └──────── external context / constraints ────────────┘
                                                                 │
                                                                 ▼
                                                             Outcome
                                                                 │
                                  ┌──────────────────────────────┤
                                  ▼                              ▼
                           next Situation                  learning / update
```

- **Situation (`Sit_t`)** — Character外部に存在する事実・出来事・条件。法律、規則、制度、社会規範、資源、時間・物理的制約等も含み得ます。
- **Perception (`P_t`)** — Situationの何がsalientになり、どのようなmotivational-emotional significanceとして感じ取られるか。
- **Values & Beliefs (`VB_t`)** — 経験を通じて学習・一般化された、「何を大切とするか」と「自分・他者・世界をどう捉えるか」に関する内的状態。
- **Relationship (`Rel_t`)** — 他者との相互作用から形成される時間依存の関係状態。
- **Experience (`E_t`)** — PerceptionされたSituationが、Values & BeliefsとRelationshipを通じて、そのCharacterにとってどのような意味を持つ経験となったか。
- **Response (`R_t`)** — Experienceと外部Situationの条件・制約のもとでCharacterが選択・開始する反応。

### Perception と Experience

```text
Situation
「相手が眉をひそめた」
        ↓
Perception
「拒絶の兆候が強くsalientになった」
        ↓
Experience
「自分はこの人から受け入れられていない、と感じる経験になった」
        ↓
Response
「話すのをやめる」
```

**Situationは外で何が起きたか、Perceptionは何をどう感じ取ったか、Experienceはそれがその人にとってどんな経験になったか**を区別します。

### S / N を直感的に見る

同じ「未知の対象が現れた」というSituationでも、Perceptionの偏りは次のように変わり得ます。

| S | N | 起こりやすいPerception | 直感的なイメージ |
|---|---|---|---|
| High | Low | 機会・新奇性が強くsalient、危険は比較的弱い | 「面白そう。価値がありそう」 |
| High | High | 機会と危険の双方が強くsalient | 「すごく気になる。でも危険でもある」 |
| Low | High | 機会への反応は弱く、脅威・損失が強くsalient | 「危険かもしれない」 |
| Low | Low | いずれも強くsalientになりにくい | 「今すぐ反応するほどではない」 |

- **S = Seeking Reactivity** — 報酬、新奇性、快、機会などを求め、探索しようとする反応性。Surgency / Extraversionを主要な理論的起点とします。
- **N = Negative Affectivity** — 脅威、喪失、拒絶、不快などに対してネガティブ情動が活性化しやすい反応性です。

SとNは行動を直接決めるルールではありません。TemperamentはPerceptionを偏らせます。

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

実行済み実験の用語・データ・Gate・閾値・hash・結論は、後続のモデル改訂によって書き換えません。

PF-EXP-0001〜0003の入力として用いた `Experience` は、v1.2では外部 `Situation` として概念的に対応づけられます。一方、実行時の生成対象 `Interpretation` は、v1.2でPerceptionとExperienceを分離する以前の概念であり、**両者の境界そのものを直接検証したものではありません**。Opportunity / Danger Salience、Seeking / Negative Activation等の評価は、SituationとTemperamentによるPerception側の偏りを観測する指標として引き続き参照できます。実行済み記録はそのまま保持します。

PF-EXP-0004 pilot-001は旧 `History → Response` を検証する計画でしたが、history pretestでP2 No directivenessをFAILしたためmain generationへ進まず、confirmatory hypothesis自体は未検証です。この結果もv1.2への移行によって変更しません。

PF-EXP-0005 pilot-002では、Situation・Perception・Relationshipを固定してValues & Beliefsだけを操作したところ、pretest P1〜P5とmain G1〜G5をすべてPASSしました。Learning meaning effect `ΔL=3.5417`、Evaluation-threat meaning effect `ΔE=2.5833`、8/8 familyで両方向の効果を確認し、今回の実験条件では **`Values & Beliefs → Experience` を支持**しました。この結果はPerception / Experienceの機能的分離にも限定的な支持を与えます。詳細は [PF-DISC-0001](research/discoveries/PF-DISC-0001-values-beliefs-shape-experience.md) に記録しています。

## Repository guide

| Path | Role |
|---|---|
| [`docs/`](docs/) | 現行正本。Research Framework / Research Models / Glossary |
| [`research/notes/`](research/notes/) | 現行モデルに整合する問い・仮説 |
| [`research/experiments/`](research/experiments/) | 人格形成を検証する実験と監査記録 |
| [`research/discoveries/`](research/discoveries/) | 現行系列の根拠付きの発見 |
| [`research/legacy/`](research/legacy/) | 旧版・旧モデル・旧実験の隔離Archive |

研究は `notes → experiments → discoveries → docs/models` と進め、十分に検証された知見だけを正本へ反映します。

## Canonical documents

1. [APRL Research Framework v1.0.2](docs/APRL_Research_Framework.md)
2. [Personality Formation Model v1.2](docs/models/Personality_Formation_Model.md)
3. [Glossary](docs/glossary.md)

単一の旧 `APRL Concept Model v1.0` は二段構造へ置き換え、[Legacy Archive](research/legacy/concept-model-v1/) に保存しています。

旧 `T0=(S,N,C)` 系列のEXP-0001も、最新の監査記録を含めて [canonical-v1 archive](research/legacy/canonical-v1/) に隔離しています。

# APRL Concept Model v1.0.3

> Canonical Edition  
> AI Personality Research Lab

---

# はじめに

APRL（AI Personality Research Lab）は、人工人格を実験系として用い、

**「人はなぜ、ある人格に心を動かされるのか。」**

を探究する研究プロジェクトである。

APRLの目的はAI小説を生成することではない。

人工人格を通して人格形成を理解し、人が人生に共鳴する仕組みを理解することである。

本書はAPRLにおける概念モデルの正本（Canonical Edition）として位置付けられ、今後の研究・設計・実験の基準となる。

---

# Vision

## 人工人格を通して、人間理解を深める。

人間は人格に心を動かされる。

しかし実際には、人格そのものではなく、その人格が歩んできた人生、すなわち人格形成史（Biography）に心を動かされている可能性がある。

APRLは人工人格を実験系として用いることで、人格形成と人生への共鳴を理解することを目指す。

---

# Mission

## 人格形成と人生への共鳴を再現・理解する。

APRLでは、人格形成を再現するだけでは十分ではない。

人格形成史をAudienceへ届け、Audienceがどのように人生へ共鳴するのかまでを研究対象とする。

---

# Grand Research Question

## 人はなぜ、ある人格に心を動かされるのか。

この問いはAPRLにおける最上位研究課題である。

すべての概念モデル・研究課題・実験は、この問いを理解するために存在する。

---

# Core Philosophy

APRLは以下の哲学に基づいて設計される。

## Character First

物語ではなく人格を中心に設計する。

## Biography First

人格の静的な設定ではなく、人格形成史を理解する。

## Process over Result

結果よりも過程を重視する。人格形成の過程そのものが研究対象である。

## Story Emerges

Storyは設計するものではない。人格同士の相互作用から自然に創発する。

## Observe Before Intervening

Creatorは人格を直接操作しない。まず観察し、必要最小限のみ介入する。

---

# Core Principles

- 人格は経験によって形成される。
- Characterは、Experienceを人格固有にInterpretationし、Responseへ変換する。
- Responseは新たなExperienceを生み、この反復によってCharacterは更新される。
- Biographyは、この反復過程の時間的軌跡である。
- 気質は行動を直接決定せず、Characterの変換過程に初期的な確率的偏りを与える。
- 人格尺度は、生成条件と観測指標を区別して用いる。
- Audienceは人格の属性だけでなく、Biographyに共鳴する。
- CreatorはCharacterの人格や意思決定を直接操作しない。
- StoryはCharacter同士の相互作用から創発する。
- Characterは媒体を超えて存在する。

---

# Concept Model

```text
Creator Layer
  Creator Persona
  ├─ World
  ├─ Character
  ├─ Temperament T0
  └─ Narrative Pressure
          │
          ▼
Character Layer
  Experience_t
      │
      ▼
  Character: Interpretation | T0, H_t
      │
      ▼
  Response_t = (Action, Intensity, Latency)
      │
      └──────────────► Experience_t+1

  反復された軌跡 ──► Biography
          │
          ▼
Communicator Layer
  BiographyをAudienceへ伝達する
  （媒体・視点・構成・演出を包含）
          │
          ▼
Audience Layer
  Audience
      │
      ▼
  Biographical Resonance
```

人格形成の最小単位は、次の循環である。

$$
Experience_t
\rightarrow
\boxed{Character: Interpretation \mid T_0,H_t}
\rightarrow
Response_t
\rightarrow
Experience_{t+1}
$$

ここで、

- $T_0$：Characterの初期気質
- $H_t$：時点 $t$ までの経験・解釈・反応の履歴
- $Response_t$：反応の内容・強度・開始時点

を表す。

---

# Creator Layer

Creator Layerは、人格形成が起こる初期条件と環境を設計するレイヤーである。

Creator Personaは、主に次を設計する。

- World
- Character
- 初期気質 $T_0$
- 世界の制約
- Narrative Pressure

Creatorは、Characterの人格や個々のResponseを直接決定しない。

Characterは、自らの気質と履歴を持ってExperienceをInterpretationし、Responseを生成する。

Creatorの人格傾向は、設計選択との関連を分析する観測変数になり得るが、個々の選択を単純に決定する因果変数とはみなさない。

---

# Character Layer

Character LayerはAPRLの中心となる研究対象である。

Characterは固定された属性ではない。

Experience、Interpretation、Responseの反復を通して形成され続ける動的な存在である。

## 最小Characterモデル

$$
I_t=f(E_t,T_0,H_t)
$$

$$
R_t=g(I_t,T_0,H_t)
$$

- $E_t$：現在のExperience
- $I_t$：Character固有のInterpretation
- $R_t$：生成・調整されたResponse
- $T_0$：初期気質
- $H_t$：それまでの履歴

Interpretationは、知覚、注意、評価、感情、記憶、意味づけ、信念、動機などを必要に応じて包含する中核機能である。

ただし、これらを固定された直列工程として正本には置かない。

この抽象化により、詳細な心理過程を事前に一つへ固定せず、実験ごとに必要な内部モデルを検証できる。

## Response

Responseは行動の種類だけではない。

$$
Response_t=(Action_t,Intensity_t,Latency_t)
$$

- $Action_t$：どのような行動を選ぶか
- $Intensity_t$：どの程度の強度で反応するか
- $Latency_t$：いつ反応を開始するか

複数のCharacterが同じイベントに直面したとき、最初に行動するCharacterは次のように表現できる。

$$
FirstActor_t=\arg\min_i Latency_{i,t}
$$

Latencyは単一の気質次元だけでなく、Interpretation、気質の組み合わせ、履歴、関係性、状況から確率的に生じる。

---

# Temperament as Initial Condition

APRLでは、Rothbartの気質概念を参考に、Characterの初期条件を次の3次元で表す。

$$
T_0=(S,N,C)
$$

| 記号 | 次元 | APRLでの機能 |
|---|---|---|
| $S$ | Surgency / Extraversion | 新奇性、報酬、接近、活動開始への初期的な反応傾向 |
| $N$ | Negative Affectivity | 脅威、喪失、拒絶、失敗への初期的な感受性 |
| $C$ | Effortful Control | 注意の維持・切替、優勢反応の抑制、反応の選択・調整 |

$S$ と $N$ は主に反応を駆動し、$C$ は優勢になった反応を実行、保留、切替、調整する。

したがって、誰が最初に行動するかは $C$ 単独では決まらない。

| 気質構成 | 生じやすい初期傾向 |
|---|---|
| 高 $S$・低 $C$ | 接近、発言、探索を早く開始する |
| 高 $N$・低 $C$ | 警戒、防御、回避を早く開始する |
| 高 $S$・高 $C$ | 接近意欲を保ちながら状況確認後に動く |
| 低 $S$・高 $C$ | 観察と必要性の判断を優先する |
| 低 $S$・低 $N$ | 反応開始の駆動が弱く、他者を待ちやすい |

気質は、Responseを直接決定する固定ルールではない。

**気質 $T_0$ は、Interpretationを中核とするCharacterの変換全体に、初期的な確率的偏りを与える条件である。**

また、Rothbartの人間向け質問紙をLLMへそのまま適用することを意味しない。APRLでは理論概念をAI人格の操作可能な生成パラメータとして再定義し、独自に妥当性を検証する。

---

# Formation and Observation Layers

APRLでは心理モデルの役割を、生成・形成・観測の三層に分ける。

| 層 | 対象 | モデル・変数 | 役割 |
|---|---|---|---|
| 生成層 | Characterの開始時 | Rothbart型気質 $T_0=(S,N,C)$ | 初期的な反応性と自己調整の偏りを与える |
| 形成層 | Characterの時間発展 | Experience → Interpretation → Response | 経験の反復によってCharacterを形成する |
| 観測層 | Creator・Character・Audience | Big Five | 形成・表出された比較的安定した傾向を測る |

## CharacterのBig Five

形成途中または形成後のCharacterについて、Big Fiveは表出的傾向を観測する指標として用いる。

$$
B_{Ch,t}=Measure(\{Response_\tau\}_{\tau\leq t})
$$

Big Fiveは原則として、Character内部でResponseを生成する初期条件ではない。

## CreatorのBig Five

CreatorのBig Fiveは、World、Character、Narrative Pressureなどの設計選択と人格傾向の関連を分析するために用いる。

単純な決定論的因果説明には用いない。

## AudienceのBig Five

AudienceのBig Fiveは、同じBiographyに対して共鳴の仕方が異なることを分析する調整変数として用いる。

$$
Resonance_{a,ch}=Q(Biography_{ch},B_{A,a},Context_a,Communication)
$$

## CommunicatorのBig Five

必要に応じて、視点、構成、演出、表現の選択傾向を分析する観測指標として用いる。

---

# Biography

Biography（人格形成史）は、Experience、Interpretation、Responseの反復によって形成された時間的軌跡である。

$$
\{Experience \rightarrow Interpretation \rightarrow Response\}_{t=1}^{n}
\rightarrow Biography
$$

Biographyは単なる出来事の年表ではない。

- Characterが何を経験したか
- そのExperienceをどうInterpretationしたか
- どのようなResponseを選んだか
- Responseが次のExperienceをどう変えたか
- 反復によって傾向、信念、動機、関係性がどう形成されたか

を記述する。

BiographyはCharacterを理解するための中心概念である。

---

# Communicator Layer

Communicator Layerは、BiographyをAudienceへ伝達するレイヤーである。

Communicatorは特定の媒体を意味しない。

- 視点
- 構成
- 演出
- 表現
- 媒体

など、伝達に関わる方法を包含する。

小説、映画、ゲーム、漫画、アニメ、TRPGなどは、Communicator Layerの実装例である。

---

# Audience Layer

Audience Layerは、Biographyに触れ、Biographical Resonanceを形成するレイヤーである。

同じBiographyでも、Audienceの人格傾向、経験、文脈、およびCommunicationによって共鳴は異なる。

AudienceはCharacterと同じ人格だから共鳴するとは限らない。

共鳴は、Biographyとの実際の類似性だけでなく、Audienceが知覚した類似性、差異、願望、葛藤によっても生じ得る。

---

# Biographical Resonance

Biographical Resonance（人生への共鳴）とは、AudienceがCharacterのBiographyに触れ、理解、共感、愛着、感動、考察などの心理的変化を生じる現象である。

APRLは、Characterの生成だけでなく、BiographyがCommunicatorを介してAudienceへ届き、どのような共鳴を生むかまでを研究対象とする。

---

# Story Emergence

APRLでは、Storyは目的ではない。

Storyは、複数のCharacterがExperienceをInterpretationし、異なるResponseを返し、そのResponseが互いの次のExperienceとなることで創発する結果である。

CreatorはStoryを直接決定しない。

Characterが人生を歩むことで、Storyが生まれる。

APRLはStory Generationではなく、Character EvolutionとBiographical Resonanceを研究対象とする。

---

# Theoretical Positioning

APRLの簡易Characterモデルは、既存理論を置き換えるものではない。

- 基本構造：S–O–R
- 人格固有の処理：CAPS
- Interpretationの根拠：認知的評価理論
- Responseから次のExperienceへの循環：社会的認知理論
- Biography：Narrative Identity
- 人工人格の実装候補：Generative Agents
- APRL独自の射程：Biography → Communication → Biographical Resonance

研究上の独自性は、Experience、Interpretation、Responseの三要素自体ではなく、反復による人格形成、Biography化、Audienceとの共鳴までを一つの研究系として接続する点にある。

---

# Discoveries

## D-0001 Biography Hypothesis

Blueprintではなく、Biographyを人格理解の中心概念とする。

人格形成史を記述することで、人格理解はより深まると考える。

## D-0002 Creator Collaboration Hypothesis

Creator Personaは単一である必要はない。

複数のCreator Personaが、異なる哲学、価値観、動機を持ちながら協調・競合することで、より創発的な世界設計が可能になる可能性がある。

現時点ではConcept Modelへは組み込まず、Discoveryとして継続研究する。

---

# Glossary

| 用語 | 定義 |
|---|---|
| Creator Persona | World、Character、初期条件、Narrative Pressureを設計する存在 |
| Character | Experienceを人格固有にInterpretationし、Responseを生成しながら形成される人工人格 |
| Experience | Characterが世界および他者との相互作用を通して経験する出来事 |
| Interpretation | 知覚、注意、評価、感情、記憶、意味づけ、信念、動機などを包含し得るCharacter固有の中核機能 |
| Response | Characterが生成・調整する反応。内容、強度、開始時点を含む |
| Temperament $T_0$ | Characterの変換過程に初期的な確率的偏りを与える条件 |
| History $H_t$ | 時点 $t$ までに蓄積したExperience、Interpretation、Responseの履歴 |
| Biography | 人格形成の反復過程を記述した時間的軌跡 |
| Communicator | BiographyをAudienceへ伝達する役割 |
| Audience | Biographyに触れ、人生へ共鳴する存在 |
| Biographical Resonance | Biographyへの共鳴 |
| Narrative Pressure | 人格形成を促すためにCreatorが世界へ与える出来事、制約、試練 |
| Big Five | 形成・表出された比較的安定した人格傾向を観測する指標 |

---

# Version History

## v1.0.3

### Added

- Rothbart型初期気質 $T_0=(S,N,C)$
- Responseの観測次元：Action、Intensity、Latency
- 複数CharacterにおけるFirst Actorの定義
- 生成層・形成層・観測層の区別
- Creator、形成後Character、Audience、CommunicatorへのBig Fiveの使い分け
- 既存心理モデルとの理論的位置づけ

### Updated

- Character Layerを簡易モデル `Experience → Character: Interpretation → Response` へ更新
- Responseから次のExperienceへの循環を明示
- Biographyを反復過程の時間的軌跡として再定義
- 気質をInterpretation単独ではなく、Characterの変換全体の初期条件として定義
- 旧版の誤記ディレクトリ `docs/condept-model/` から、正しい `docs/concept-model/` へ正本パスを移行

## v1.0.2

### Added

- Communicator Layer
- Biographical Resonance
- Creator Persona
- Story Emergence
- Creator Collaboration Hypothesis（Discovery）

### Updated

- Biographyを中心概念として再定義
- Concept Modelを4層構造へ整理

---

# Manifesto

## We Believe

物語は設計するものではない。

人格が人生を歩むことで、物語は自然に創発する。

私たちは、物語を書くために人格を作るのではない。

人格を理解するために、世界を設計する。

Creatorは世界を創る。

Characterは人生を生きる。

Communicatorは人生を伝える。

Audienceは人生に共鳴する。

---

# Canonical Statement

APRL（AI Personality Research Lab）は、人工人格を実験系として用い、

**「人はなぜ、ある人格に心を動かされるのか。」**

を探究する研究である。

人格形成と人生への共鳴を再現・理解することを目的とし、Creatorが初期条件と世界を設計し、CharacterがExperienceを人格固有にInterpretationしてResponseを重ね、その軌跡がBiographyとなり、CommunicatorがBiographyをAudienceへ届け、Audienceが人生へ共鳴することで、Storyは自然に創発すると考える。

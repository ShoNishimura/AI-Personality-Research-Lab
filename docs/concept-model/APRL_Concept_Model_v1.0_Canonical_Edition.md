# APRL Concept Model v1.0

> Canonical Edition  
> AI Personality Research Lab  
> 2026-08-12

---

# 1. Purpose

APRL（AI Personality Research Lab）は、人工人格を実験系として用い、

**「人はなぜ、ある人格に心を動かされるのか。」**

を探究する研究プロジェクトである。

APRLの目的はAI小説そのものを生成することではない。

人工人格を通して人格形成を理解し、その人格形成史がAudienceにどのような共鳴を生むかを理解することを目的とする。

本書をAPRLの概念モデルの正本（Canonical Edition）とする。

---

# 2. Vision / Mission / Grand Research Question

## Vision

**人工人格を通して、人間理解を深める。**

## Mission

**人格形成と人生への共鳴を再現・理解する。**

## Grand Research Question

**人はなぜ、ある人格に心を動かされるのか。**

すべての研究課題・設計・実験は、この問いを理解するために存在する。

---

# 3. Core Philosophy

- **Character First** — 物語ではなく人格を中心に設計する。
- **Biography First** — 静的な人格設定ではなく、人格が形成された軌跡を重視する。
- **Process over Result** — 結果だけでなく、形成過程そのものを研究対象とする。
- **Story Emerges** — Storyは直接設計するのではなく、Character同士の相互作用から創発する結果として扱う。
- **Observe Before Intervening** — CreatorはCharacterの個々のResponseを直接決定せず、環境と初期条件を設計して観察する。
- **Minimum Model First** — 正本には必要最小限の概念だけを置き、詳細モデルは実験によって必要性が確認されたときに追加する。

---

# 4. Core Model

APRLにおける人格形成の最小単位は、次の循環である。

```text
                Temperament T0 = (S, N)
                         │
                         ▼
Experience_t ──► Interpretation_t ──► Regulation_t ──► Response_t
     ▲                                                   │
     └──────────────── Experience_t+1 ◄─────────────────┘

Response_t = (Action_t, Intensity_t, Latency_t)

反復された時間的軌跡 ──► Biography
```

より形式的には、

$$
I_t=f(E_t,T_0,H_t)
$$

$$
R_t=g(I_t,T_0,Reg_t,H_t)
$$

と表す。

- $E_t$：現在のExperience
- $I_t$：Character固有のInterpretation
- $T_0$：初期的なTemperament
- $Reg_t$：時点 $t$ におけるRegulation
- $R_t$：Response
- $H_t$：それまでのExperience、Interpretation、Regulation、Response等の履歴

この式は詳細な心理過程を固定するものではない。APRLでは、実験で必要になるまでは中間過程を増やさない。

---

# 5. Temperament

## 5.1 APRLにおける定義

APRLではTemperamentを、**刺激に対する基礎的な motivational-emotional reactivity の初期条件**として操作的に定義する。

最小モデルでは、次の2次元を採用する。

$$
T_0=(S,N)
$$

| 記号 | APRLでの名称 | 理論上の由来 | APRLでの意味 |
|---|---|---|---|
| $S$ | **Seeking Reactivity** | Surgency / Extraversion | 報酬、新奇性、快、機会などに価値を感じ、それを求め、探索しようとする反応性 |
| $N$ | **Negative Affectivity** | Negative Affectivity | 脅威、喪失、拒絶、不快などに対して、恐怖、不快、悲しみ、苛立ちなどのネガティブ情動が活性化しやすい反応性 |

SはRothbart系のSurgency / Extraversionを主要な理論的起点とするが、APRLではその全内容をそのまま採用するのではなく、報酬、新奇性、快、機会などを求める基礎的な反応性に焦点を当ててSeeking Reactivityとして操作的に定義する。

NはRothbart系のNegative Affectivityという名称をそのまま用いる。

SとNはResponseを直接決定する固定ルールではない。CharacterがExperienceをInterpretationし、Responseを形成する過程へ初期的な確率的偏りを与える。

SとNが統計的に完全に独立していることは仮定しない。また、両者は同時に活性化し得る。たとえば、魅力的だが危険でもある対象では、「知りたい・試したい」というSeekingと、「怖い・不快だ」というNegative Affectivityが同時に生じ得る。

## 5.2 Rothbart理論との関係

Rothbart系の気質理論は、気質をreactivityとself-regulationの個人差として広く扱う。

APRLはその理論をそのまま複製するのではなく、モデルを簡潔に保つため、**Temperamentという語を基礎的なmotivational-emotional reactivityに限定して使用する**。

Effortful Controlに対応する機能はTemperamentの第三軸には置かず、後述するRegulationとして分離する。

この2次元は、人間の気質を完全に記述する普遍的な基底であると主張するものではない。APRLにおける最小の初期条件モデルであり、必要性が実証された場合にのみ拡張する。

---

# 6. Interpretation

Interpretationは、ExperienceがそのCharacterにとって**どのような意味を持つ状態として処理されるか**を表す。

Interpretationは意識的な思考に限定しない。

生物一般へ適用できるよう、知覚、注意、評価、感情、記憶、意味づけ、信念、動機などを必要に応じて包含する抽象概念とする。

人間のCharacterでは、過去の経験、信念、価値観、関係性、社会規範、将来予測などがInterpretationを複雑にし得る。

これらを固定された直列工程として正本には置かない。

---

# 7. Regulation

Regulationは、Interpretationから生じるResponseを**抑制、保留、選択、切替、調整する機能**である。

APRLではRegulationをTemperamentの一要素とはせず、Characterが持つ可変的な調整機能として扱う。

Regulationは、発達、成熟、学習、経験などによって変化し得る。

最小モデルではInterpretationとResponseの間に置く。

```text
Interpretation
      │
      ▼
  Regulation
      │
      ▼
   Response
```

RegulationはResponseの以下のすべてに作用し得る。

- **Action** — どの行動を選択するかを変更する。
- **Intensity** — 反応の強さを増減する。
- **Latency** — 反応を開始するまでの時間を変化させる。

したがって、RegulationはLatencyそのものではない。

詳細な心理モデルではRegulationが注意やInterpretationにも影響し得るが、APRLの正本ではモデルの簡潔さを優先し、まずResponse形成を調整する機能として置く。

---

# 8. Response

Responseは次の3要素で記述する。

$$
Response_t=(Action_t,Intensity_t,Latency_t)
$$

## Action

**何をするか。**

接近、逃走、攻撃、停止、探索、対話、質問、援助、無視など、Characterが選択した反応の内容を表す。

## Intensity

**どの程度の強さで反応するか。**

同じActionでも、弱く反応する場合と強く反応する場合を区別する。

## Latency

**ExperienceからResponseを開始するまでにどの程度の時間を要するか。**

同じActionでも、即時に行う場合と、観察・保留の後に行う場合を区別する。

人間ではAction spaceが広く、対話、規範に基づく行動、将来を考慮した選択なども可能になる。またRegulationによってAction、Intensity、Latencyを柔軟に調整できる。

---

# 9. Biological Applicability

このCore Modelは人間に限定しない。

生物種や人工エージェントによって異なるのは、基本構造の有無ではなく、主として次の程度であると考える。

- Experienceとして処理できる情報の範囲
- Interpretationの複雑さ
- Action spaceの広さ
- Regulationの能力と柔軟性
- 履歴を保持し学習へ利用する能力

単純な反応系ではInterpretationやRegulationは非常に小さく実装され得る。一方、人間では対話、規範、自己概念、将来予測などによってInterpretationとAction spaceが大きく拡張され、Regulationも複雑になる。

APRLは生物を「高次／低次」と階層化せず、同じ基本モデルの実装上の差として扱う。

---

# 10. Relationship

複数のCharacterが存在すると、一方のResponseは他方の次のExperienceになる。

```text
Character A                         Character B
Experience → ... → Response ─────► Experience
    ▲                                  │
    └──────── Response ◄──── ... ◄────┘
```

この相互作用の履歴からRelationshipが形成される。

Relationshipは単一Characterの属性ではなく、**Character間に形成される時間依存の状態**として扱う。必要に応じて非対称性を許容する。

## Affiliation

Affiliationは、他者との暖かさ、親密さ、結びつきを求めるCharacter側の関係的動機として扱う。

AffiliationはSと同一ではない。

- S / Seeking Reactivityは、人や対象に価値や新奇性を感じ、それを求めたり探索したりする反応を起こしやすくすることがある。
- Affiliationは、特定の他者との親密な関係を求める傾向を表す。

したがって、多くの人や対象へ積極的に探索・接近するが深い関係を求めないCharacterも、Seekingは低いが少数の相手との強い結びつきを求めるCharacterも表現できる。

AffiliationはCore Temperamentには含めず、Relationship Modelで必要になった時点で導入・検証する。

---

# 11. Character and Biography

Characterは固定された属性一覧ではない。

Experience、Interpretation、Regulation、Responseの反復と、他者とのRelationshipを通して継続的に形成される動的な存在である。

Biography（人格形成史）は、その形成過程の時間的軌跡である。

Biographyは単なる出来事の年表ではなく、

- 何をExperienceしたか
- それをどうInterpretationしたか
- どのようにRegulationしたか
- どのResponseを、どのIntensityとLatencyで選んだか
- そのResponseが次のExperienceをどう変えたか
- 他者とのRelationshipがどう形成されたか
- その反復によって信念、動機、価値観、行動傾向がどう形成されたか

を含む。

---

# 12. Creator / Communicator / Audience

## Creator Layer

Creatorは、人格形成が起こる初期条件と環境を設計する。

主な対象は、World、Characterの初期条件、Temperament、環境制約、Narrative Pressureである。

CreatorはCharacterの個々のResponseを直接決定しない。

## Communicator Layer

CommunicatorはBiographyをAudienceへ伝達する。

視点、構成、演出、表現、媒体など、伝達方法を包含する。

## Audience Layer

AudienceはBiographyに触れ、Biographical Resonanceを形成する。

同じBiographyでも、Audience自身の経験、人格傾向、文脈、Communicationによって共鳴の仕方は異なり得る。

---

# 13. Story Emergence

StoryはAPRLの直接設計対象ではない。

複数のCharacterがExperienceをInterpretationし、Regulationを経てResponseを返し、そのResponseが互いの次のExperienceとなることで、出来事の連鎖が生じる。

その結果としてStoryが創発する。

**Creatorは世界を設計する。  
Characterは人生を生きる。  
Communicatorは人生を伝える。  
Audienceは人生に共鳴する。**

---

# 14. Formation and Observation

APRLでは、人格を形成する変数と、形成された人格を観測する尺度を区別する。

- Temperament、Experience、Interpretation、Regulation、Response、Relationshipは形成モデルの候補である。
- Big Fiveなどの人格尺度は、形成・表出された傾向を観測するために利用できる。

観測尺度を、そのままCharacter内部の生成ルールとはみなさない。

---

# 15. Theoretical Basis

APRLのCore Modelは既存理論の再現ではなく、研究のための最小抽象モデルである。

特にTemperamentとRegulationの整理では、Rothbart系のtemperament researchを主要な理論的参照点とする。

- Rothbart & Derryberry (1981): temperamentをreactivityとself-regulationの個人差として整理。
- Putnam, Gartstein, & Rothbart (2006): 幼児の気質にSurgency/Extraversion、Negative Affectivity、Effortful Controlの上位構造を報告。 DOI: 10.1016/j.infbeh.2006.01.004
- Evans & Rothbart (2007): 成人のtemperament modelでExtraversion/Surgency、Negative Affect、Effortful Control、Affiliativeness等を区別。 DOI: 10.1016/j.jrp.2006.11.002

APRLはこれらを踏まえつつ、正本ではモデルの簡潔さを優先して、

- motivational-emotional reactivityを **Temperament = (S,N)**
- Sを **Seeking Reactivity**（Surgency / Extraversionを理論的起点とする）
- Nを **Negative Affectivity**
- responseの調整機能を **Regulation**
- 親密な他者との結びつきへの動機を **Affiliation / Relationship Model**

へ分離する。

---

# 16. Canonical Statement

APRLは、Characterを静的な人格設定ではなく、Experienceを固有にInterpretationし、Regulationを経てResponseを重ねながら形成される動的な存在として扱う。

Characterの最小初期条件として、報酬、新奇性、快、機会などを求めるSeeking Reactivity（S）と、脅威、喪失、拒絶、不快などに対するNegative Affectivity（N）からなるTemperamentを置く。

ResponseはAction、Intensity、Latencyによって記述され、Regulationはこれらを調整する。

複数Characterの相互作用はRelationshipを形成し、その時間的軌跡がBiographyとなる。

BiographyがCommunicatorを通してAudienceへ伝わり、Biographical Resonanceを生む過程までをAPRLの研究対象とする。

---

# Version

**v1.0 — Initial Canonical Edition**

APRLの公開Canonical versioningは本版から開始する。
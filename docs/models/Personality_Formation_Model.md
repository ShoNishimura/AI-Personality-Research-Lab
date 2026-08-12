# APRL Personality Formation Model v1.0

> Canonical Research Model  
> AI Personality Research Lab  
> Current Research Focus  
> 2026-08-12

---

# 1. Position in APRL

本書は、[APRL Research Framework](../APRL_Research_Framework.md) の下位に位置する研究モデルである。

APRL全体のGrand Research Questionは、

**「人はなぜ、その人に心を動かされるのか。」**

である。

本モデルはその全体を説明するものではなく、直近の研究対象である**人格形成（Personality Formation）**を扱う。

本モデルの中心的なResearch Questionは、

**「人格はどのように形成されるのか。」**

である。

---

# 2. Minimum Formation Model

APRLにおける人格形成の最小単位を、次の循環として扱う。

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

この式は詳細な心理過程を固定するものではない。実験上の必要性が確認されるまでは中間過程を増やさない。

---

# 3. Temperament

APRLではTemperamentを、**刺激に対する基礎的な motivational-emotional reactivity の初期条件**として操作的に定義する。

最小モデルでは、次の2次元を採用する。

$$
T_0=(S,N)
$$

| 記号 | APRLでの名称 | 理論上の由来 | APRLでの意味 |
|---|---|---|---|
| $S$ | **Seeking Reactivity** | Surgency / Extraversion | 報酬、新奇性、快、機会などに価値を感じ、それを求め、探索しようとする反応性 |
| $N$ | **Negative Affectivity** | Negative Affectivity | 脅威、喪失、拒絶、不快などに対して、恐怖、不快、悲しみ、苛立ちなどのネガティブ情動が活性化しやすい反応性 |

SはRothbart系のSurgency / Extraversionを主要な理論的起点とするが、その全内容をそのまま採用するのではなく、報酬、新奇性、快、機会などを求める基礎的な反応性に焦点を当ててSeeking Reactivityとして操作的に定義する。

NはRothbart系のNegative Affectivityという名称をそのまま用いる。

SとNはResponseを直接決定する固定ルールではない。ExperienceをInterpretationし、Responseを形成する過程へ初期的な確率的偏りを与える。

SとNが統計的に完全に独立していることは仮定しない。また、両者は同時に活性化し得る。

## 3.1 Intuitive examples

同じ「未知の対象を見つけた」というExperienceでも、初期反応の偏りは次のように変わり得る。

| S | N | 起こりやすい初期傾向 |
|---|---|---|
| High | Low | 強く探索・接近しやすく、警戒は比較的弱い |
| High | High | 強く知りたい一方で危険も強く感じ、慎重に接近しやすい |
| Low | High | 探索欲求が弱く、距離を取る・回避する方向へ偏りやすい |
| Low | Low | 強く反応せず、必要が生じるまで様子を見やすい |

これらは行動規則ではない。最終的なResponseはInterpretation、履歴、Relationship、Regulation等によって変化する。

## 3.2 Rothbart theoryとの関係

Rothbart系の気質理論は、気質をreactivityとself-regulationの個人差として広く扱う。

APRLはモデルを簡潔に保つため、**Temperamentという語を基礎的なmotivational-emotional reactivityに限定して使用する**。

Effortful Controlに対応する機能はTemperamentの第三軸には置かず、Regulationとして分離する。

この2次元は、人間の気質を完全に記述する普遍的基底であると主張するものではない。APRLにおける最小の初期条件モデルであり、必要性が実証された場合にのみ拡張する。

---

# 4. Interpretation

Interpretationは、ExperienceがそのCharacterにとって**どのような意味を持つ状態として処理されるか**を表す。

Interpretationは意識的な思考に限定しない。

知覚、注意、評価、感情、記憶、意味づけ、信念、動機などを必要に応じて包含する抽象概念とする。

人間のCharacterでは、過去の経験、信念、価値観、関係性、社会規範、将来予測などがInterpretationを複雑にし得る。

これらを固定された直列工程として本モデルには置かない。

---

# 5. Regulation

Regulationは、Interpretationから生じるResponseを**抑制、保留、選択、切替、調整する機能**である。

RegulationはTemperamentの一要素とはせず、Characterが持つ可変的な調整機能として扱う。

発達、成熟、学習、経験などによって変化し得る。

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

- **Action** — どの行動を選択するか
- **Intensity** — 反応の強さ
- **Latency** — 反応を開始するまでの時間

したがって、RegulationはLatencyそのものではない。

詳細な心理モデルではRegulationが注意やInterpretationにも影響し得るが、本モデルでは簡潔さを優先し、まずResponse形成を調整する機能として置く。

---

# 6. Response

Responseは次の3要素で記述する。

$$
Response_t=(Action_t,Intensity_t,Latency_t)
$$

- **Action** — 何をするか。接近、逃走、攻撃、停止、探索、対話、質問、援助、無視など。
- **Intensity** — どの程度の強さで反応するか。
- **Latency** — ExperienceからResponseを開始するまでにどの程度の時間を要するか。

人間ではAction spaceが広く、対話、規範に基づく行動、将来を考慮した選択なども可能になる。またRegulationによってAction、Intensity、Latencyを柔軟に調整できる。

---

# 7. History and Biography Interface

人格形成は一回のResponseではなく、反復によって生じる。

$H_t$ は、それまでのExperience、Interpretation、Regulation、Response等の履歴を表す。

この履歴の時間的軌跡が、上位のAPRL Research Frameworkで定義するBiographyへ接続する。

Biographyは本モデルの内部変数として閉じず、**人格形成モデルから上位Frameworkへ渡される主要な出力**として扱う。

---

# 8. Relationship Boundary

複数のCharacterが存在すると、一方のResponseは他方のExperienceになり得る。

Relationshipは人格形成へ強く影響し得るが、Relationshipそのものの形成機構は本モデルでは固定しない。

本モデルでは、Relationshipを以下の形で扱う。

- Experienceの重要な発生源
- Interpretationへ影響し得る履歴・文脈
- Biographyを構成する相互作用の軌跡

Relationshipの詳細は、必要性が確認された時点で独立したRelationship Modelとして検証する。

AffiliationもCore Temperamentには含めず、そのモデルで必要になった時点で導入する。

---

# 9. Biological Applicability

このFormation Modelは人間に限定しない。

生物種や人工エージェントによって異なるのは、基本構造の有無ではなく、主として次の程度であると考える。

- Experienceとして処理できる情報の範囲
- Interpretationの複雑さ
- Action spaceの広さ
- Regulationの能力と柔軟性
- 履歴を保持し学習へ利用する能力

APRLは生物を「高次／低次」と階層化せず、同じ基本モデルの実装上の差として扱う。

---

# 10. Formation and Observation

人格を形成する変数と、形成された人格を観測する尺度を区別する。

- Temperament、Experience、Interpretation、Regulation、Responseは形成モデルの中核候補である。
- Relationshipは形成へ影響する外部・相互作用的状態として扱う。
- Big Fiveなどの人格尺度は、形成・表出された傾向を観測するために利用できる。

観測尺度を、そのままCharacter内部の生成ルールとはみなさない。

---

# 11. Theoretical Basis

本モデルは既存理論の再現ではなく、研究のための最小抽象モデルである。

特にTemperamentとRegulationの整理では、Rothbart系のtemperament researchを主要な理論的参照点とする。

- Rothbart & Derryberry (1981): temperamentをreactivityとself-regulationの個人差として整理。
- Putnam, Gartstein, & Rothbart (2006): 幼児の気質にSurgency/Extraversion、Negative Affectivity、Effortful Controlの上位構造を報告。 DOI: 10.1016/j.infbeh.2006.01.004
- Evans & Rothbart (2007): 成人のtemperament modelでExtraversion/Surgency、Negative Affect、Effortful Control、Affiliativeness等を区別。 DOI: 10.1016/j.jrp.2006.11.002

APRLでは、

- motivational-emotional reactivityを **Temperament = (S,N)**
- Sを **Seeking Reactivity**
- Nを **Negative Affectivity**
- Responseの調整機能を **Regulation**

へ分離する。

---

# 12. Scope

## In scope

- Temperamentの初期条件
- Experience
- Interpretation
- Regulation
- Response
- 履歴を通した人格形成
- Biographyへの接続

## Out of scope for this model

- Relationship形成の詳細機構
- Creatorによる介入モデル
- Communicatorによる伝達モデル
- Audienceの心理過程
- Resonanceの分類・測定
- Storyの評価

これらは上位Frameworkに位置づけ、必要になった時点で別のResearch Modelとして導入する。

---

# 13. Canonical Statement

APRL Personality Formation Modelは、Characterを静的な人格設定ではなく、Experienceを固有にInterpretationし、Regulationを経てResponseを重ねながら形成される動的な存在として扱う。

最小初期条件として、Seeking Reactivity（S）とNegative Affectivity（N）からなるTemperamentを置く。

ResponseはAction、Intensity、Latencyによって記述し、Regulationはこれらを調整する。

この反復の履歴が人格を形成し、その時間的軌跡がAPRL Research FrameworkにおけるBiographyへ接続する。

---

# Version

**v1.0 — Initial Canonical Personality Formation Model**

APRL Research Frameworkとは独立してversioningする。
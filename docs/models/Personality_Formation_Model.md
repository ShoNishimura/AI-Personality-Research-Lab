# APRL Personality Formation Model v1.1

> Canonical Research Model  
> AI Personality Research Lab  
> Current Research Focus  
> 2026-08-14

---

# 1. Position in APRL

本書は、[APRL Research Framework](../APRL_Research_Framework.md) の下位に位置する研究モデルである。

APRL全体のGrand Research Questionは、

**「人はなぜ、その人に心を動かされるのか。」**

である。

本モデルはその全体を説明するものではなく、直近の研究対象である **人格形成（Personality Formation）** を扱う。

中心的なResearch Questionは、

**「人格はどのように形成されるのか。」**

である。

---

# 2. Minimum Formation Model

APRLにおける人格形成の最小単位を、次の循環として扱う。

```text
External environment / physical conditions ─┐
Body / physiological state ─────────────────┤
                                             ▼
                                        Experience_t
                                             │
                          Temperament T0      │
                               │              │
                               └──────► Perception_t ───────► Response_t
                                                              ▲       ▲
                                                              │       │
                                                          History_t  Relationship_t

Response_t ──► World / interaction outcome ──► next Experience / History / Relationship

Response_t = (Action_t, Intensity_t, Latency_t)

反復された時間的軌跡 ──► Biography
```

最小モデルの核は二つの関係で表す。

$$
P_t=f(E_t,T_0)
$$

$$
R_t=g(P_t,H_t,Rel_t)
$$

- $E_t$：Characterがその時点で置かれているExperience。外部の出来事・刺激・環境条件に加え、身体・生理状態等の内部状態を含み得る
- $P_t$：Character固有のPerception
- $T_0$：初期的なTemperament
- $H_t$：それまでのExperience、Perception、Response等の履歴
- $Rel_t$：時点 $t$ におけるRelationship
- $R_t$：Characterが選択・開始するResponse

この式は詳細な心理過程を固定するものではない。実験上の必要性が確認されるまでは中間変数や直接経路を増やさない。

特に最小モデルでは、TemperamentからResponseへの直接経路、History / RelationshipからPerceptionへの直接経路、独立したMotivation変数、独立したRegulation変数を置かない。

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

SとNはResponseを直接決定する行動規則ではない。**Experienceの何がどの程度salientになり、どのように感じ取られるかというPerceptionへ初期的な確率的偏りを与える。**

SとNが統計的に完全に独立していることは仮定しない。また、両者は同時に活性化し得る。

## 3.1 Intuitive examples

同じ「未知の対象を見つけた」というExperienceでも、Perceptionの偏りは次のように変わり得る。

| S | N | 起こりやすいPerception |
|---|---|---|
| High | Low | 新奇性や機会が強くsalientになり、危険は比較的弱く感じ取りやすい |
| High | High | 機会・探索価値と危険の双方が強くsalientになり得る |
| Low | High | 機会への反応は弱く、脅威・損失が強くsalientになりやすい |
| Low | Low | いずれも強くsalientにならず、反応性が比較的低い |

これらは行動規則ではない。同じPerceptionでも、HistoryやRelationshipが異なれば最終的なResponseは変わり得る。

---

# 4. Experience

Experienceは、Characterがその時点で置かれている**現在の入力・状態**を表す。

外部だけに限定せず、必要に応じて次を含む。

- **外部の出来事・刺激** — 他者の発言、対象物、出来事等
- **環境・物理的条件** — 場所、距離、利用可能な手段、障害物、温度、時間的制約等
- **身体・生理状態** — 空腹、疲労、痛み、覚醒状態等

これらをそれぞれ独立した人格変数として最小モデルへ追加しない。現在時点でCharacterが受け取る条件として $E_t$ に含め、TemperamentとともにPerceptionへ入力する。

身体・生理状態や環境条件がResponseの実行可能性そのものを制約する場合は、Responseの選択と、そのResponseがWorld内で実現した結果を区別する。

---

# 5. Perception

Perceptionは、**Experienceのうち何がCharacterにとってsalientになり、どのような motivational-emotional significance として感じ取られるか**を表す。

ここでいうPerceptionは、単なる感覚器入力や物体認識に限定しない。

注意、salience、機会・脅威の感じ取り、情動的な活性化など、ExperienceをResponseへつなぐための初期的な受け取り方を包含する。

最小モデルでは、Perceptionの直接入力をExperienceとTemperamentに限定する。

$$
P_t=f(E_t,T_0)
$$

HistoryやRelationshipが知覚そのものへ影響する可能性を一般理論として否定するものではない。ただしAPRLの最小モデルでは、その直接経路は実験上の必要性が確認されるまで追加しない。

---

# 6. History

Historyは、それまでのCharacterの形成過程をResponse選択へ持ち込む時間依存の文脈である。

$H_t$ は、それまでのExperience、Perception、Response等の履歴を表す。

同じPerceptionでも、過去に何を経験し、どのようなResponseと結果を重ねてきたかによって、現在のResponseは変わり得る。

Historyの詳細な内部表現は本版では固定しない。まず、Historyの違いがResponseへ再現可能な差を生むかを検証する。

---

# 7. Relationship

Relationshipは、**複数Character間の相互作用履歴から形成される時間依存の状態**である。

同じPerceptionでも、相手との信頼、親密さ、敵対、役割等のRelationshipが異なればResponseは変わり得る。

本モデルではRelationshipをResponseの入力として扱う。

$$
R_t=g(P_t,H_t,Rel_t)
$$

一方のResponseは他方のExperienceとなり得るため、Relationship自体も相互作用を通じて更新される。

Relationshipの詳細な形成機構、関係資源、Affiliation等は、必要性が確認された時点で独立したRelationship Modelとして検証する。

---

# 8. Response

Responseは、Characterが**選択し、開始する反応**である。

$$
Response_t=(Action_t,Intensity_t,Latency_t)
$$

- **Action** — 何をするか。接近、回避、探索、対話、質問、援助、停止、無視など。
- **Intensity** — どの程度の強さで反応するか。
- **Latency** — ExperienceからResponseを開始するまでにどの程度の時間を要するか。

最小モデルではResponseを、Perception、History、Relationshipから形成されるものとして扱う。

TemperamentはPerceptionを介してのみResponseへ寄与する。TemperamentからResponseへの直接経路は置かない。

Responseは、World内で必ずそのまま実現する結果を意味しない。例えば「逃げようとする」というResponseを選んでも、出口が塞がれていれば逃走は成功しない。環境・物理的制約や身体能力との相互作用によって生じた結果は、次のExperience、History、Relationshipへ接続する。

## 8.1 Motivation boundary

MotivationはResponse形成に重要であり得るが、v1.1では独立した中核変数として固定しない。

APRLの最小モデルでは、Motivationと呼び得る傾向を、その起源に応じて既存入力からResponseに現れるものとして扱う。

- 現在の報酬・脅威・身体要求等に由来する動機的意味はPerceptionに現れ得る
- 過去の成功・失敗、学習、長期的な目標等に由来する傾向はHistoryに保持され得る
- 特定の相手を助けたい、避けたい、信頼したい等の関係的な傾向はRelationshipに反映され得る

したがって、現行の

$$
R_t=g(P_t,H_t,Rel_t)
$$

の中でどこまで説明できるかを先に検証する。

同一のPerception、History、Relationshipを与えても、Motivationを独立状態として置かなければ説明できない安定したResponse差が確認された場合にのみ、Motivation変数の追加を再検討する。

---

# 9. Biography Interface

人格形成は一回のResponseではなく、反復によって生じる。

ResponseはWorldや他者と相互作用し、その結果が次のExperienceを変え、Historyを蓄積し、他者との相互作用ではRelationshipを変化させ得る。

その時間的軌跡が、上位のAPRL Research Frameworkで定義するBiographyへ接続する。

Biographyは本モデルの内部変数として閉じず、**人格形成モデルから上位Frameworkへ渡される主要な出力**として扱う。

---

# 10. Regulation / C Boundary

APRLの旧検討では、Effortful ControlやRegulationに相当する調整機能を独立変数として置く案を扱った。

v1.1のMinimum Modelでは、**C / Regulationを独立した中核変数として置かない。**

まず、

$$
R_t=g(P_t,H_t,Rel_t)
$$

でResponse差をどこまで説明できるかを検証する。

同一のPerception、History、Relationshipを与えても安定したResponse差が残るなど、追加の調整能力を仮定する必要性が実証された場合にのみ、C / Regulation等の変数を再検討する。

これはRegulationの存在を否定する主張ではなく、**Minimum Model First** に基づくモデル境界である。

---

# 11. Formation and Observation

人格を形成する変数と、形成・表出された傾向を観測する尺度を区別する。

- Temperament、Experience、Perception、History、Relationship、Responseは現行Formation Modelの中核である。
- 身体・生理状態、環境・物理的条件はExperienceを構成し得る現在条件として扱う。
- Motivationは現行Minimum Modelでは独立変数にせず、Perception、History、RelationshipからResponseへ現れる派生的な説明概念として扱う。
- Big Fiveなどの人格尺度は、形成・表出された傾向を観測するために利用できる。
- Opportunity Salience、Danger Salience、Seeking Activation、Negative Activation等はPerceptionを観測するための実験尺度として利用できる。

観測尺度や説明上のラベルを、そのままCharacter内部の独立生成変数とはみなさない。

---

# 12. Theoretical Basis

本モデルは既存理論の再現ではなく、研究のための最小抽象モデルである。

Temperamentの整理では、Rothbart系のtemperament researchを主要な理論的参照点とする。

- Rothbart & Derryberry (1981): temperamentをreactivityとself-regulationの個人差として整理。
- Putnam, Gartstein, & Rothbart (2006): 幼児の気質にSurgency/Extraversion、Negative Affectivity、Effortful Controlの上位構造を報告。 DOI: 10.1016/j.infbeh.2006.01.004
- Evans & Rothbart (2007): 成人のtemperament modelでExtraversion/Surgency、Negative Affect、Effortful Control、Affiliativeness等を区別。 DOI: 10.1016/j.jrp.2006.11.002

APRL v1.1では、

- motivational-emotional reactivityを **Temperament = (S,N)**
- Sを **Seeking Reactivity**
- Nを **Negative Affectivity**
- Temperamentの主たる作用点を **Perception**

として最小化する。

Effortful Control / Regulationは理論上の重要性を否定しないが、現行Minimum Modelには独立変数として含めない。

---

# 13. Scope

## In scope

- Temperamentの初期条件
- 外部条件と身体・生理状態を含み得るExperience
- Perception
- History
- Relationshipを条件としたResponse
- ResponseとWorld / 他者との相互作用による次状態
- 反復による人格形成
- Biographyへの接続

## Out of scope for the current minimum model

- Motivationの独立機構
- C / Regulationの独立機構
- Relationship形成の詳細機構
- Creatorによる介入モデル
- Communicatorによる伝達モデル
- Audienceの心理過程
- Resonanceの分類・測定
- Storyの評価

これらは必要性が確認された時点で別のResearch Modelまたはモデル拡張として導入する。

---

# 14. Canonical Statement

APRL Personality Formation Modelは、Characterを静的な人格設定ではなく、身体・生理状態や環境条件を含むExperienceをTemperamentに応じて固有にPerceptionし、そのPerceptionにHistoryとRelationshipが加わってResponseを形成し、そのResponseがWorldや他者と相互作用する反復によって変化する動的な存在として扱う。

最小初期条件として、Seeking Reactivity（S）とNegative Affectivity（N）からなるTemperamentを置く。

TemperamentはPerceptionを偏らせるが、Responseを直接決定しない。

ResponseはAction、Intensity、Latencyによって記述し、Perception、History、Relationshipの関数として扱う。身体・生理状態や環境・物理的条件はExperienceおよびResponse実現後の相互作用条件として扱い、MotivationとC / Regulationは必要性が実証されるまで独立変数として置かない。

この反復の履歴が人格を形成し、その時間的軌跡がAPRL Research FrameworkにおけるBiographyへ接続する。

---

# 15. v1.0 → v1.1 migration

v1.1では、モデルを単純化し、実験系列との対応を明確化した。

- `Interpretation` を **Perception** へ再定義した。
- Perceptionの直接入力を `Experience + Temperament` に限定した。
- TemperamentからResponseへの直接経路を削除した。
- HistoryとRelationshipをResponseの入力として明示した。
- 身体・生理状態、環境・物理的条件は独立変数を増やさずExperienceとWorld interactionの境界として整理した。
- Motivationを独立変数にせず、Perception、History、RelationshipからResponseへ現れる派生的な説明概念として整理した。
- C / RegulationをMinimum Modelから外し、必要性が実証された場合の拡張候補とした。
- PF-EXP-0001〜0003で `Interpretation` と呼んでいた生成対象は、v1.1ではPerceptionの観測として再位置づける。実行済みデータ、Gate、閾値、hash、結論は変更しない。

---

# Version

**v1.1 — Perception-centered Minimum Formation Model**

APRL Research Frameworkとは独立してversioningする。
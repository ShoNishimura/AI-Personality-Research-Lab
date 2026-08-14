# APRL Personality Formation Model v1.2

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
                         Temperament T0
                              │
                              ▼
World ──► Situation_t ──► Perception_t ──► Experience_t ──► Response_t
            │                                      ▲             │
            │                                      │             │
            │                            Values & Beliefs_t       │
            │                              Relationship_t         │
            │                                                    │
            └──────── external context / constraints ────────────┘
                                                                 │
                                                                 ▼
                                                   World / interaction outcome
                                                                 │
                       ┌─────────────────────────────────────────┤
                       ▼                                         ▼
                next Situation                         learning / update
                                                         │            │
                                                         ▼            ▼
                                                Values & Beliefs  Relationship

反復された時間的軌跡 ──► Biography
```

最小モデルの核は次の関係で表す。

$$
P_t=f(Sit_t,T_0)
$$

$$
E_t=h(P_t,VB_t,Rel_t)
$$

$$
R_t=g(E_t,Sit_t)
$$

- $Sit_t$：時点 $t$ にCharacterの外部に存在するSituation
- $P_t$：Situationの何がCharacterにとってsalientになり、どのように感じ取られるかというPerception
- $T_0$：初期的なTemperament
- $VB_t$：時点 $t$ のValues & Beliefs
- $Rel_t$：時点 $t$ のRelationship
- $E_t$：PerceptionがそのCharacterにとってどのような意味を持つ経験となったかを表すExperience
- $R_t$：Characterが選択・開始するResponse

`S` はSeeking Reactivityの記号として使用するため、Situationは記号衝突を避けて `Sit` と表記する。

`R_t=g(E_t,Sit_t)` におけるSituationの入力は、Experienceで表現された主観的意味を重複して与えるためではない。Responseが常に外部の状況・制約のもとで選択されることを表す。

この式は詳細な心理過程を固定するものではない。実験上の必要性が確認されるまでは中間変数や直接経路を増やさない。

---

# 3. Situation

Situationは、**Characterの外部に存在する現在の事実・出来事・条件**を表す。

最小モデルの一次入力はSituationであり、Character内部の状態をSituationへ混在させない。

Situationには必要に応じて次を含み得る。

- **Event / Stimulus** — 他者の発言、対象物、出来事等
- **External Context / Constraints** — 法律、規則、制度、社会規範、利用可能な資源、時間的制約、環境・物理的条件等

Situationは二つの経路で形成過程へ作用し得る。

1. TemperamentとともにPerceptionを形成する
2. Responseの選択可能性・制約、およびResponse後の実現結果を外部から構造化する

外部に存在する条件と、それをCharacterがどう感じ取るかは区別する。

---

# 4. Temperament

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

SとNはResponseを直接決定する行動規則ではない。**Situationの何がどの程度salientになり、どのように感じ取られるかというPerceptionへ初期的な確率的偏りを与える。**

SとNが統計的に完全に独立していることは仮定しない。また、両者は同時に活性化し得る。

## 4.1 Intuitive examples

同じ「未知の対象が現れた」というSituationでも、Perceptionの偏りは次のように変わり得る。

| S | N | 起こりやすいPerception |
|---|---|---|
| High | Low | 新奇性や機会が強くsalientになり、危険は比較的弱く感じ取りやすい |
| High | High | 機会・探索価値と危険の双方が強くsalientになり得る |
| Low | High | 機会への反応は弱く、脅威・損失が強くsalientになりやすい |
| Low | Low | いずれも強くsalientにならず、反応性が比較的低い |

これらは行動規則ではない。同じPerceptionでも、Values & BeliefsやRelationshipが異なればExperienceは変わり得る。

---

# 5. Perception

Perceptionは、**Situationの何がCharacterにとってsalientになり、どのような motivational-emotional significance として感じ取られるか**を表す。

ここでいうPerceptionは、単なる感覚器入力や物体認識に限定しない。

注意、salience、機会・脅威の感じ取り、情動的な活性化など、外部SituationをCharacter固有のExperienceへつなぐ初期的な受け取り方を包含する。

最小モデルでは、Perceptionの直接入力をSituationとTemperamentに限定する。

$$
P_t=f(Sit_t,T_0)
$$

Values & BeliefsやRelationshipは、最小モデルではPerceptionではなく、そのPerceptionがCharacterにとってどのようなExperienceとなるかに作用する。

---

# 6. Values & Beliefs

Values & Beliefsは、Characterが経験を重ねる中で形成・更新される**学習された内的状態**である。

- **Values** — 何を大切・望ましい・優先すべきと捉えるか
- **Beliefs** — 自分、他者、世界がどのようなものだと捉え、何を期待するか

$VB_t$ は、過去の出来事そのものの記録ではなく、それまでのExperience、Response、その結果等を通じて学習・一般化され、時点 $t$ まで保持されている状態を表す。

Values & Beliefsは明示的に言語化された信念だけに限定しない。行動選択へ影響する暗黙的な学習・期待も含み得る。

最小モデルでは、Values & BeliefsはPerceptionとRelationshipとともにExperienceの形成へ作用する。

$$
E_t=h(P_t,VB_t,Rel_t)
$$

個別の過去Episodeをそのまま保持・想起するEpisodic Memoryは、必要性が確認されるまで独立した中核変数として置かない。

---

# 7. Relationship

Relationshipは、**複数Character間の相互作用履歴から形成される時間依存の状態**である。

同じPerceptionでも、相手との信頼、親密さ、敵対、役割等のRelationshipが異なれば、その出来事がCharacterにとって持つ意味、すなわちExperienceは変わり得る。

最小モデルではRelationshipをExperienceの入力として扱う。

$$
E_t=h(P_t,VB_t,Rel_t)
$$

Relationshipが関与しないSituationでは `none / neutral` として扱える。

一方のResponseは他方のSituationとなり得るため、Relationship自体も相互作用を通じて更新される。

Relationshipの詳細な形成機構、関係資源、Affiliation等は、必要性が確認された時点で独立したRelationship Modelとして検証する。

---

# 8. Experience

Experienceは、**PerceptionされたSituationが、そのCharacterにとってどのような意味を持つ経験となったか**を表す。

したがって、SituationとExperienceを区別する。

- **Situation** — 外部で何が起きているか
- **Perception** — そのうち何がsalientになり、どう感じ取られたか
- **Experience** — それが、そのCharacterにとってどのような意味を持つ経験になったか

最小モデルでは、

$$
E_t=h(P_t,VB_t,Rel_t)
$$

とする。

## 8.1 Intuitive example

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

同じSituation・Perceptionでも、Values & BeliefsやRelationshipが異なればExperienceは異なり得る。

---

# 9. Response and Outcome

Responseは、Characterが**選択し、開始する反応**である。

$$
Response_t=(Action_t,Intensity_t,Latency_t)
$$

- **Action** — 何をするか。接近、回避、探索、対話、質問、援助、停止、無視など
- **Intensity** — どの程度の強さで反応するか
- **Latency** — ExperienceからResponseを開始するまでにどの程度の時間を要するか

最小モデルでは、ResponseをExperienceとSituationの関数として扱う。

$$
R_t=g(E_t,Sit_t)
$$

ExperienceはCharacter内部で形成された主観的意味を表す。Situationは、Responseが外部の現実・規則・資源・物理条件等のもとで選択されることを表す。

Responseは、World内で必ずそのまま実現する結果を意味しない。選択されたResponseと実際のSituationとの相互作用によってOutcomeが生じる。

例えば、Characterがある行動を選択しても、外部条件によって実行できない、あるいは意図した結果にならない場合がある。

Outcomeは次のSituationを変え、学習を通じてValues & Beliefsを更新し、他者との相互作用ではRelationshipを変化させ得る。

---

# 10. Formation and Biography Interface

人格形成は一回のResponseではなく、反復によって生じる。

```text
Situation → Perception → Experience → Response → Outcome
                           ▲                       │
                           │                       │
                  Values & Beliefs ── learning ───┘
                  Relationship ────── interaction ─┘
```

Values & Beliefsの更新過程は概念的には、

$$
VB_{t+1}=u(VB_t,E_t,R_t,Outcome_t)
$$

と表せる。

この式は具体的な学習アルゴリズムを固定するものではない。何をどの程度学習・一般化し、ValuesやBeliefsがどのように変わるかは今後の検証対象である。

Biographyは、この形成過程の**時間的軌跡**である。

Biographyは過去EpisodeをResponseへ直接入力するための内部変数ではない。Situation、Perception、Experience、Response、Outcome、Values & Beliefs、Relationshipが時間の中でどのように変化したかを上位のAPRL Research Frameworkへ接続する。

---

# 11. Embodiment / Body State Extension

Minimum Modelでは、Body / Physiological Stateを独立変数として置かない。

身体・生理状態が対象とする現象に重要な場合は、`Body State (B_t)` を拡張変数として導入できる。

ただし、Body Stateの作用経路をCoreでは一律に固定しない。

例えば、**食事に関わる状況では空腹がPerceptionにもExperienceにも作用し得る一方、怪我はResponseの実行可能性に主として作用し得る。**

どの経路へ作用させるかは、対象とする現象と検証目的に応じて定義する。

---

# 12. Model Boundaries

## 12.1 History / Episodic Memory

v1.1の`History`は、過去のExperience、Perception、Response等の履歴をResponse入力としてまとめていた。

v1.2では、過去から形成された現在の内的状態を **Values & Beliefs** として明示し、`History`をMinimum Modelの中核変数から外す。

過去の出来事そのものの時間的軌跡はBiographyとの接続で扱う。特定Episodeの想起が現在の形成過程へ独立して必要であることが確認された場合は、Episodic Memory等として別途検証する。

PF-EXP-0004 pilot-001は旧History操作のpretestで停止しており、`History → Response`仮説自体は未検証である。実行済みのstimuli、Gate、閾値、hash、結果記録はv1.2への移行によって書き換えない。

## 12.2 Motivation

Motivationは人格形成・Response形成に重要であり得るが、v1.2では独立した中核変数として固定しない。

- 現在の報酬・脅威等の動機的意味はPerception / Experienceに現れ得る
- 長期的な価値判断や期待はValues & Beliefsに保持され得る
- 特定の相手へ向けた傾向はRelationshipに反映され得る

これらだけでは説明できない安定した差が確認された場合に、独立したMotivation変数を再検討する。

## 12.3 Regulation / C

Effortful ControlやRegulationに相当する調整機能の理論的重要性は否定しない。

ただしv1.2 Minimum Modelでは独立した中核変数として置かない。同一のExperienceとSituationを与えても安定したResponse差が残るなど、追加の調整機能を仮定する必要性が実証された場合に再検討する。

---

# 13. Formation and Observation

人格を形成する変数と、形成・表出された傾向を観測する尺度を区別する。

- Situation、Temperament、Perception、Values & Beliefs、Relationship、Experience、Responseは現行Formation Modelの中核である
- Body State、Episodic Memory、Motivation、Regulationは現行Minimum Modelでは拡張候補である
- Big Fiveなどの人格尺度は、形成・表出された傾向を観測するために利用できる
- Opportunity Salience、Danger Salience、Seeking Activation、Negative Activation等はPerceptionを観測するための実験尺度として利用できる

観測尺度や説明上のラベルを、そのままCharacter内部の独立生成変数とはみなさない。

---

# 14. Theoretical Basis

本モデルは既存理論の再現ではなく、研究のための最小抽象モデルである。

APRL Personality Formation Modelは、Stimulus–Organism–Response（S-O-R）という一般的な枠組みと概念的に整合する。

v1.2ではこの境界を明確化し、S-O-RにおけるStimulus側を **Situation** としてCharacter外部の事実・出来事・条件に限定する。Character側では、TemperamentによるPerception、Values & BeliefsとRelationshipを通じたExperience形成を区別し、その結果としてResponseが生じる過程を具体化する。

APRLはS-O-Rの再現を目的としない。S-O-Rの一方向モデルに加えて、OutcomeからValues & BeliefsやRelationshipが更新され、反復された形成過程がBiographyへ接続する時間的ループを研究対象とする。

Temperamentの整理では、Rothbart系のtemperament researchを主要な理論的参照点とする。

- Rothbart & Derryberry (1981): temperamentをreactivityとself-regulationの個人差として整理
- Putnam, Gartstein, & Rothbart (2006): 幼児の気質にSurgency/Extraversion、Negative Affectivity、Effortful Controlの上位構造を報告。 DOI: 10.1016/j.infbeh.2006.01.004
- Evans & Rothbart (2007): 成人のtemperament modelでExtraversion/Surgency、Negative Affect、Effortful Control、Affiliativeness等を区別。 DOI: 10.1016/j.jrp.2006.11.002

APRL v1.2では、

- motivational-emotional reactivityを **Temperament = (S,N)**
- Sを **Seeking Reactivity**
- Nを **Negative Affectivity**
- Temperamentの主たる作用点を **Perception**

として最小化する。

Effortful Control / Regulationは理論上の重要性を否定しないが、現行Minimum Modelには独立変数として含めない。

---

# 15. Scope

## In scope

- Character外部のSituation
- Temperamentの初期条件
- Perception
- Values & Beliefs
- Relationship
- Experience
- Situationの制約下でのResponse
- ResponseとWorld / 他者との相互作用によるOutcome
- 学習・一般化によるValues & Beliefsの更新
- 反復による人格形成
- Biographyへの接続

## Out of scope for the current minimum model

- Body / Physiological Stateの固定的な作用経路
- Episodic Memoryの独立機構
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

# 16. Canonical Statement

APRL Personality Formation Modelは、Characterを静的な人格設定ではなく、外部SituationをTemperamentに応じて固有にPerceptionし、そのPerceptionがValues & BeliefsとRelationshipを通じてCharacter固有のExperienceとなり、そのExperienceと外部SituationのもとでResponseを選択する動的な存在として扱う。

ResponseはWorldや他者と相互作用してOutcomeを生み、その結果からValues & BeliefsやRelationshipが更新される。この反復が人格形成を生み、その時間的軌跡がBiographyへ接続する。

最小初期条件として、Seeking Reactivity（S）とNegative Affectivity（N）からなるTemperamentを置く。TemperamentはPerceptionを偏らせるが、Responseを直接決定しない。

Body State、Episodic Memory、Motivation、C / Regulationは必要性が確認されるまでMinimum Modelの独立変数として置かない。

---

# 17. v1.1 → v1.2 migration

v1.2では、内外の境界と、Perception / Experience / 学習された内的状態の役割を再整理した。

- 一次入力を、Character外部の **Situation (`Sit_t`)** へ変更した
- SituationとCharacter内部状態を分離した
- Perceptionを、Situationの何がsalientになりどう感じ取られるかに限定した
- Experienceを、PerceptionがValues & BeliefsとRelationshipを通じてCharacterにとって持つ主観的意味として再定義した
- `History`をMinimum Modelから外し、過去から学習・一般化された現在状態を **Values & Beliefs (`VB_t`)** として明示した
- ResponseがExperienceだけでなく、常に外部Situationの条件・制約下で選択されることを明示した
- OutcomeからValues & Beliefsが更新されるformation loopを明示した
- Body / Physiological StateはMinimum Modelから外し、必要時のEmbodiment extensionとした。作用経路はCoreでは固定しない
- Biographyを内部入力ではなく、形成過程の時間的軌跡として明確化した
- PF-EXP-0001〜0004の実行済み用語、データ、Gate、閾値、hash、結果は監査記録として変更しない

PF-EXP-0001〜0003の入力として用いた `Experience` は、v1.2では外部 `Situation` として概念的に対応づけられる。一方、実行時の生成対象 `Interpretation` は、v1.2でPerceptionとExperienceを分離する以前の概念であり、**両者の境界そのものを直接検証したものではない**。Opportunity / Danger Salience、Seeking / Negative Activation等の評価は、SituationとTemperamentによるPerception側の偏りを観測する指標として引き続き参照できる。

---

# Version

**v1.2 — Situation–Perception–Experience Formation Model**

APRL Research Frameworkとは独立してversioningする。

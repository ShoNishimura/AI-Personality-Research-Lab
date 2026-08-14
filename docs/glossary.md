# APRL Glossary

この用語集は、現行の [APRL Research Framework v1.0.2](APRL_Research_Framework.md) と [Personality Formation Model v1.2](models/Personality_Formation_Model.md) における共通言語を定義する。

一般理論上の定義ではなく、APRLでの操作的な意味を優先する。

---

## APRL Research Framework

APRL全体のGrand Research Question、主要な研究領域、その位置関係を定義する上位正本。

---

## Research Model

Research Frameworkの一部分を、仮説検証可能な形へ具体化する下位モデル。

現在のPrimary Research ModelはPersonality Formation Modelである。

---

## Character

外部SituationをPerceptionし、それが自分にとってどのようなExperienceとなるかを形成し、Responseを重ね、RelationshipやValues & Beliefsを変化させながら時間の中で形成される動的な存在。

---

## Biography

Characterがどのように形成されてきたかを表す時間的軌跡。

Situation、Perception、Experience、Response、Outcome、Values & Beliefs、Relationship等の時間的な変化を含み得る。単なる出来事の年表ではない。

---

## Relationship

複数Character間の相互作用履歴から形成される時間依存の状態。

現行Personality Formation Modelでは、同じPerceptionがCharacterにとってどのようなExperienceとなるかを変え得る入力として扱う。

---

## Creator

World、Characterの初期条件、環境制約、出来事、Narrative Pressure等を設計する役割。

Characterの個々のResponseは直接決定しない。

---

## Communicator

BiographyをAudienceへ伝達する役割。

---

## Audience

Communicatorを通してCharacter / Biographyに触れ、心理的反応を形成する存在。

---

## Resonance

Audienceが「その人」に触れることで生じる心理的反応を研究するための上位概念。

---

## Biographical Resonance

AudienceがCharacterのBiographyに触れることで生じる理解、共感、愛着、感動、考察等の心理的な共鳴。

---

## Personality Formation Model

現在のPrimary Research Trackである人格形成を扱うResearch Model。

現行v1.2では次を最小核とする。

`Perception = f(Situation, Temperament)`

`Experience = h(Perception, Values & Beliefs, Relationship)`

`Response = g(Experience, Situation)`

---

## Situation (`Sit_t`)

Characterの外部に存在する現在の事実・出来事・条件。

Event / Stimulusに加え、法律、規則、制度、社会規範、利用可能な資源、時間的制約、環境・物理的条件等を含み得る。

Character内部の状態はSituationへ含めない。

S-O-RにおけるStimulus側と概念的に対応するが、Seeking Reactivityの記号 `S` との衝突を避けるため、APRLではSituationを `Sit` と表記する。

---

## Temperament

刺激に対する基礎的な motivational-emotional reactivity の初期条件。

最小モデルでは `T0=(S,N)` とする。TemperamentはResponseを直接決定せず、Perceptionへ初期的な偏りを与える。

---

## Seeking Reactivity (S)

報酬、新奇性、快、機会などに価値を感じ、それを求め、探索しようとする反応性。

Rothbart系のSurgency / Extraversionを主要な理論的起点とする。

---

## Negative Affectivity (N)

脅威、喪失、拒絶、不快などに対して、ネガティブ情動が活性化しやすい反応性。

---

## Perception

Situationの何がCharacterにとってsalientになり、どのような motivational-emotional significance として感じ取られるかを表す。

単なる感覚器入力や物体認識に限定しない。

現行Minimum Modelでは `Perception = f(Situation, Temperament)` とする。

PF-EXP-0001〜0003の実行時の生成対象 `Interpretation` は、v1.2でPerceptionとExperienceを分離する以前の概念であり、**両者の境界そのものを直接検証したものではない**。一方、Opportunity / Danger Salience、Seeking / Negative Activation等の評価は、SituationとTemperamentによるPerception側の偏りを観測する指標として引き続き参照できる。実行済み記録では監査性のため旧名称を保持する。

---

## Values & Beliefs (`VB_t`)

経験を重ねる中で形成・更新される学習された内的状態。

- **Values**：何を大切・望ましい・優先すべきと捉えるか
- **Beliefs**：自分、他者、世界がどのようなものだと捉え、何を期待するか

過去の出来事そのものの記録ではなく、Experience、Response、その結果等を通じて学習・一般化され、現在まで保持されている状態を表す。

---

## Experience

PerceptionされたSituationが、Values & BeliefsとRelationshipを通じて、**そのCharacterにとってどのような意味を持つ経験となったか**を表す。

Situationは「外で何が起きたか」、Perceptionは「何をどう感じ取ったか」、Experienceは「それがその人にとってどんな経験になったか」を区別する。

現行Minimum Modelでは `Experience = h(Perception, Values & Beliefs, Relationship)` とする。

---

## Response

Characterが選択し、開始する反応。

- **Action**：何をするか
- **Intensity**：どの程度の強さで反応するか
- **Latency**：ExperienceからResponseを開始するまでの時間

現行Minimum Modelでは `Response = g(Experience, Situation)` とする。

SituationをResponse入力として残すのは、Responseが外部の現実・規則・資源・物理条件等の制約下で選択されることを表すためである。

---

## Outcome

選択されたResponseと実際のSituation / Worldとの相互作用によって生じる結果。

Responseそのものとは区別する。Outcomeは次のSituationを変え、学習を通じてValues & Beliefsを更新し、他者との相互作用ではRelationshipを変化させ得る。

---

## History — legacy core term

Personality Formation Model v1.1まで、過去のExperience、Perception、Response等をResponseへ持ち込む時間依存の文脈として使用していた中核概念。

v1.2では中核変数から外し、過去から学習・一般化された現在状態はValues & Beliefsとして扱う。

特定Episodeの保持・想起が独立して必要になった場合は、Episodic Memory等の拡張候補として検証する。

実行済みPF-EXP-0004等では監査性のため `History` 表記を保持する。

---

## Embodiment / Body State — extension candidate

身体・生理状態を扱う必要がある場合に導入できる拡張概念。

現行Minimum Modelでは独立変数として置かず、作用経路もCoreでは固定しない。

例えば、食事に関わる状況では空腹がPerceptionにもExperienceにも作用し得る一方、怪我はResponseの実行可能性に主として作用し得る。

---

## Motivation — derived explanatory concept

Response形成に重要であり得る動機的な傾向を表す説明概念。

現行v1.2では独立した中核変数にせず、現在の動機的意味はPerception / Experience、長期的な価値判断や期待はValues & Beliefs、特定の相手に向けた傾向はRelationshipに現れ得るものとして扱う。

これらだけではResponse差を説明できない必要性が実証された場合に、独立変数としての導入を再検討する。

---

## World / external constraints

Characterの外部にある環境条件、制度、規則、物理法則、利用可能な手段、障害等。

現在条件としてSituationを構成し得る。Response実行後は、選択されたResponseとWorldとの相互作用によってOutcomeを決める。

---

## Interpretation — execution-time term

PF-EXP-0001〜0003で、v1.2のPerception / Experience分離以前に生成対象へ使用していた名称。

実行済みprompt、schema、artifactのfield名等では監査性のため `interpretation` を保持する。Opportunity / Danger Salience、Seeking / Negative Activation等はPerception側の観測として参照できるが、`Interpretation` 全体をv1.2のPerceptionと同一視しない。

---

## Regulation / C — extension candidate

旧検討で扱ったResponse調整機能の候補概念。

現行v1.2 Minimum Modelには独立変数として含めず、ExperienceとSituationだけではResponse差を十分説明できない場合に再検討する。

---

## Affiliation

他者との暖かさ、親密さ、結びつきを求める関係的動機候補。

Core Temperamentには含めず、Relationship Modelで必要になった時点で検証する。

---

## Narrative Pressure

人格形成を促し得るようCreatorがWorldへ与える出来事、制約、試練等を表す作業概念。

---

## Story

複数Characterの相互作用によって生じる出来事の連鎖。

APRLでは直接設計する中心対象ではなく、Characterの人生から創発する結果として扱う。

---

## Big Five

形成・表出された比較的安定した人格傾向を観測するために利用できる尺度。

APRLでは原則としてCharacterの初期生成条件そのものとはしない。

---

Aligned with: **Research Framework v1.0.2 / Personality Formation Model v1.2**

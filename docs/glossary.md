# APRL Glossary

この用語集は、現行の [APRL Research Framework v1.0.1](APRL_Research_Framework.md) と [Personality Formation Model v1.1](models/Personality_Formation_Model.md) における共通言語を定義する。

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

時間の中でExperienceとResponseを重ね、Relationshipを形成しながら変化する動的な存在。

---

## Biography

Characterがどのように形成されてきたかを表す時間的軌跡。

Experience、Perception、Response、History、Relationship等の反復を含み得る。

---

## Relationship

複数Character間の相互作用履歴から形成される時間依存の状態。

現行Personality Formation Modelでは、同じPerceptionに対するResponseを変え得る入力として扱う。

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

現行v1.1では次を最小核とする。

`Perception = f(Experience, Temperament)`

`Response = g(Perception, History, Relationship)`

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

## Experience

Characterがその時点で置かれている現在の入力・状態。

外部の出来事・刺激だけでなく、環境・物理的条件や、空腹、疲労、痛み、覚醒状態等の身体・生理状態を必要に応じて含む。

現行Minimum Modelでは、これらを独立変数として増やさず `Experience` に含める。

---

## Perception

Experienceのうち何がCharacterにとってsalientになり、どのような motivational-emotional significance として感じ取られるかを表す。

単なる感覚器入力や物体認識に限定しない。

現行Minimum Modelでは `Perception = f(Experience, Temperament)` とする。

PF-EXP-0001〜0003の実行時には、この生成対象を `Interpretation` と呼んでいた。v1.1ではそれらをPerceptionの観測として再位置づける。

---

## History

Characterがそれまでに重ねたExperience、Perception、Response等の時間的履歴。

現行Minimum Modelでは、同じPerceptionに対するResponseを変え得る入力として扱う。

---

## Response

Characterが選択し、開始する反応。

- **Action**：何をするか
- **Intensity**：どの程度の強さで反応するか
- **Latency**：ExperienceからResponseを開始するまでの時間

現行Minimum Modelでは `Response = g(Perception, History, Relationship)` とする。

ResponseがWorld内で実際に実現した結果とは区別する。環境・物理的制約や身体能力との相互作用による結果は、次のExperience、History、Relationshipへ接続する。

---

## Motivation — derived explanatory concept

Response形成に重要であり得る動機的な傾向を表す説明概念。

現行v1.1では独立した中核変数にせず、現在の動機的意味はPerception、過去や長期目標に由来する傾向はHistory、特定の相手に向けた傾向はRelationshipからResponseへ現れ得るものとして扱う。

これらだけではResponse差を説明できない必要性が実証された場合に、独立変数としての導入を再検討する。

---

## World / physical constraints

Characterの外部にある環境条件、物理法則、利用可能な手段、障害等。

現在条件としてはExperienceに含まれ得る。Response実行後は、選択されたResponseとWorldとの相互作用によって実現結果を決め、その結果が次のExperienceへ接続する。

---

## Interpretation — execution-time term

PF-EXP-0001〜0003の実行時に、現在のPerceptionに相当する生成対象へ使用していた名称。

実行済みprompt、schema、artifactのfield名等では監査性のため `interpretation` を保持するが、現行モデルの中核概念としてはPerceptionを用いる。

---

## Regulation / C — extension candidate

旧検討で扱ったResponse調整機能の候補概念。

現行v1.1 Minimum Modelには独立変数として含めず、Perception、History、RelationshipだけではResponse差を十分説明できない場合に再検討する。

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

Aligned with: **Research Framework v1.0.1 / Personality Formation Model v1.1**
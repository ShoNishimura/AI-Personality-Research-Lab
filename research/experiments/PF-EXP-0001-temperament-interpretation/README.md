# PF-EXP-0001 — Temperament → Interpretation

> Status: **Planned / pre-pilot**  
> Research Track: **Personality Formation**  
> Canonical Framework: [APRL Research Framework v1.0](../../../docs/APRL_Research_Framework.md)  
> Canonical Model: [APRL Personality Formation Model v1.0](../../../docs/models/Personality_Formation_Model.md)

---

## 1. Purpose

Personality Formation Model v1.0では、Temperamentを刺激に対する基礎的な motivational-emotional reactivity の初期条件として定義し、最小モデルを次の2次元で表す。

- **S = Seeking Reactivity**
- **N = Negative Affectivity**

TemperamentはResponseを直接決める行動規則ではなく、ExperienceのInterpretationからResponse形成へ確率的な偏りを与える初期条件として扱う。

本実験では、その最初の接続だけを切り出して検証する。

```text
Temperament T0 = (S, N)
          │
          ▼
Experience ──► Interpretation
```

### Research Question

**同一のExperienceに対し、Seeking Reactivity（S）とNegative Affectivity（N）は、想定した方向へ独立かつ再現可能なInterpretationの偏りを生むか。**

本実験は「人格形成」全体を一度に検証しない。まずTemperamentの操作的定義が測定可能な差として現れるかを確認する。

---

## 2. Scope

### In scope

- `T0=(S,N)` のHigh / Low操作
- 同一Experienceに対するInterpretation
- Seeking Activationの盲検評価
- Negative Activationの盲検評価
- S / Nの同時活性化
- neutral stimulusにおける不要な条件効果

### Out of scope

- History / Biography形成
- Relationship
- Regulationの個人差
- ResponseのAction / Intensity / Latencyの主要検証
- Creator / Communicator / Audience / Resonance

`H0 = ∅` とし、過去経験、信念、価値観、Relationship、Personality label等を与えない。

Regulationは条件間で操作しない。

ResponseはPF-EXP-0002以降で扱う。本実験ではInterpretationを主要生成物として切り出し、TemperamentからInterpretationへの接続を汚染しない。

---

## 3. Experimental Design

### 3.1 Factorial conditions

S / NをHigh / Lowにした2×2 factorial designとする。

| Condition | S | N | 操作上の意味 |
|---|---|---|---|
| T00 | Low | Low | SeekingもNegative Affectも比較的活性化しにくい |
| T01 | Low | High | Seekingは比較的弱く、Negative Affectが活性化しやすい |
| T10 | High | Low | Seekingが活性化しやすく、Negative Affectは比較的弱い |
| T11 | High | High | SeekingとNegative Affectがともに活性化しやすい |

High / Lowの記述にはActionを含めない。

禁止例：

- High S = 「未知のものへすぐ近づく」
- High N = 「危険なら逃げる」

これらはResponseを直接指定するため、本実験のTemperament操作には使用しない。

Low条件も「臆病ではない」「楽観的」等の人格ラベルで定義せず、対象のreactivityが比較的活性化しにくい状態として対称に記述する。

### 3.2 Experience classes

Pilotでは12 Experienceを使用する。

| Class | Count | 主に検証するもの |
|---|---:|---|
| Seeking-target | 3 | Sの主効果 |
| Negative-target | 3 | Nの主効果 |
| Conflict | 3 | S / Nの同時活性化 |
| Neutral | 3 | 不要なcondition effectの検出 |

#### Seeking-target

報酬、新奇性、快、機会、探索価値などを含み、明確な脅威・喪失・拒絶を極力含まないExperience。

例：未知だが安全そうな対象、任意参加の小さな報酬機会、興味深い情報へのアクセス機会。

#### Negative-target

脅威、喪失、拒絶、不快などを含み、探索報酬や新奇性そのものの価値を極力混ぜないExperience。

#### Conflict

SeekingとNegative Affectの両方が同時に活性化し得るExperience。

例：価値ある未知情報が得られる可能性がある一方、安全性が不明な対象。

T11で「知りたい」と「怖い／不快」が相殺されて中立になるのではなく、**両方が同時に立ち上がるか**を検証する。

#### Neutral

SにもNにも強く訴えないExperience。

Temperament条件を与えただけで、あらゆるExperienceに対して条件らしい人格演技が生じていないかを検出する。

### 3.3 Stimulus construction rules

各Experienceは以下を満たすよう作成し、pilot実行前に固定する。

1. 条件によって事実情報を変えない。
2. 特定のActionを要求・誘導しない。
3. 「危険」「魅力的」等、評価を先に決める語を必要以上に使わない。
4. 人物属性、社会的背景等、不要な交絡要因を入れない。
5. Seeking / Negative / Conflict / Neutralの分類目的以外の情報量をできるだけ揃える。

Pilot刺激とconfirmatory holdout刺激は分離する。

---

## 4. Generation Protocol

各runは独立した新規contextで実行する。

入力は最小限とし、次だけを与える。

1. 共通system instruction
2. Temperament condition
3. Experience
4. Interpretationのみを返すoutput instruction

Character自身にはSeeking / Negativeの数値評価をさせない。

理由は、High / Low条件を知る生成主体に自己採点させると、条件ラベルをそのまま尺度へ写像する自己申告テストになるためである。

生成時には少なくとも以下をmanifestへ固定する。

- experiment_id
- run_id
- condition_id
- stimulus_id
- replicate_id
- model_requested
- generation parameters
- prompt hash
- temperament prompt hash
- stimulus hash
- randomization seed
- execution timestamp

Raw responseは公開repositoryへ含めず、従来のAPRL方針どおり非公開で保持する。GitHubには再現性と監査に必要なmetadata、集計、checksumのみを残す。

---

## 5. Blind Evaluation

生成されたInterpretationから、condition_id、仮説、刺激classを隠したblind evaluation setを作成する。

Blind Evaluatorは最低限、次の2軸を0〜4で評価する。

### Seeking Activation

| Score | Definition |
|---:|---|
| 0 | 見られない |
| 1 | 弱い |
| 2 | 中程度 |
| 3 | 強い |
| 4 | 非常に強い |

評価対象：知りたい、得たい、試したい、探索したい、機会として価値を感じる等の反応。

### Negative Activation

| Score | Definition |
|---:|---|
| 0 | 見られない |
| 1 | 弱い |
| 2 | 中程度 |
| 3 | 強い |
| 4 | 非常に強い |

評価対象：恐怖、不快、悲しみ、苛立ち、拒絶・喪失・脅威へのネガティブ情動反応。

EvaluatorにはTemperament conditionを知らせない。

可能であれば評価順も無作為化し、生成順と切り離す。

---

## 6. Hypotheses

### H1 — Seeking validity

Seeking-target Experienceにおいて、S High条件はS Low条件よりSeeking Activationが高い。

```text
S High > S Low  on Seeking Activation
```

NのHigh / Lowにかかわらず同方向の効果が見られることを期待する。

### H2 — Negative validity

Negative-target Experienceにおいて、N High条件はN Low条件よりNegative Activationが高い。

```text
N High > N Low  on Negative Activation
```

SのHigh / Lowにかかわらず同方向の効果が見られることを期待する。

### H3 — Discriminant validity

主要な期待は次である。

```text
S → Seeking Activation      strong
S → Negative Activation     comparatively weak

N → Negative Activation     strong
N → Seeking Activation      comparatively weak
```

SとNが統計的に完全独立であることは要求しない。ただし、一方の操作が他方の尺度へ同程度以上の効果を示す場合、現在の操作的定義の弁別性を再検討する。

### H4 — Coactivation

Conflict ExperienceにおいてT11は、Seeking ActivationとNegative Activationを同時に示す。

High SとHigh Nが互いを単純に相殺し、「平均的な反応」へ戻ることを期待しない。

### H5 — Neutrality

Neutral Experienceでは、4条件間に大きなsystematic differenceが生じない。

差が大きい場合、Temperament promptがExperience固有のreactivityではなく、全般的な人格演技を誘導している可能性を疑う。

---

## 7. Pilot

最初のpilotは次の最小構成とする。

```text
4 Temperament conditions
× 12 Experiences
× 2 independent replicates
= 96 runs
```

各conditionは24 runs、各stimulusは8 runsとなる。

Pilotは測定設計と操作妥当性の確認を目的とし、confirmatory evidenceとして使用しない。

### Pilot gates

以下をすべて確認できた場合にconfirmatoryへ進む。

| Gate | Criterion |
|---|---|
| G1 | Seeking-targetでSの期待方向の主効果が再現される |
| G2 | Negative-targetでNの期待方向の主効果が再現される |
| G3 | cross-effectが対応する主効果を支配せず、S / Nを区別して測定できる |
| G4 | ConflictでT11にSeeking / Negativeのcoactivationが観測される |
| G5 | Neutralで大きな不要condition effectが生じない |

数値的な合格閾値は、**pilot responseを見る前に**評価手順・尺度とともに固定する。閾値を固定した後は、pilot結果を見て都合よく変更しない。

Gateを通らない場合、モデルをすぐ複雑化せず、まず以下を順に疑う。

1. Temperament操作文
2. Experience stimulus
3. generation instruction
4. evaluation rubric

---

## 8. Confirmatory Boundary

Pilotを通過した場合のみ、別に作成したholdout stimuliでconfirmatory studyを行う。

Pilotで使用した刺激はconfirmatory datasetへ再利用しない。

Confirmatory実行前に以下を凍結する。

- hypotheses
- condition definitions
- generation prompt
- evaluation rubric
- holdout stimuli
- exclusion rules
- retry rules
- model / generation parameters
- sample size
- analysis plan
- practical-effect / equivalence thresholds

解析では少なくともS、N、S×N、およびstimulus差を分離して扱う。

刺激固有の偶然ではなく、同種Experienceへの一般化可能性を検証するため、stimulusを跨いだ階層的解析を候補とする。

Confirmatory sample sizeは、pilotから得た分散・効果量と、事前に定義するminimum effect of interestを用いて決定する。

---

## 9. Interpretation of Outcomes

### Expected pattern

- S操作がSeeking Activationを選択的に変える。
- N操作がNegative Activationを選択的に変える。
- T11がConflictで両方を同時に示す。
- Neutralでは条件差が小さい。

このパターンが得られれば、`T0=(S,N)` をPersonality Formation Modelの最小初期条件として次段階へ進める根拠になる。

### Failure is informative

例えば、

- Sを上げるとNegativeも同程度に上がる
- Nを上げるとSeekingが一貫して下がる
- T11がcoactivationではなく単純な中和を示す
- Neutralでも強い条件差が出る

場合、Seeking Reactivity / Negative Affectivityの定義またはprompt operationalizationを見直す。

結果をモデルに合わせるのではなく、失敗をPersonality Formation Modelの改訂材料として保存する。

---

## 10. Next Experiment

PF-EXP-0001を通過した後に、次の接続を検証する。

```text
PF-EXP-0001
Temperament → Interpretation
        │
        ▼
PF-EXP-0002
Interpretation → Regulation → Response
        │
        ▼
PF-EXP-0003+
Repeated Experience → History → Personality Formation → Biography
```

PF-EXP-0001が成立する前に長期Biography simulationへ進まない。

---

## 11. Pre-pilot TODO

Pilot実行前に次を別PRで固定する。

- [ ] High / Low temperament promptの対称性レビュー
- [ ] 12 pilot stimuliの作成
- [ ] stimuliの中立性・交絡レビュー
- [ ] structured output schema
- [ ] blind evaluation rubricの最終化
- [ ] numeric pilot gate thresholds
- [ ] manifest / randomization design
- [ ] raw / blind artifactの非公開保存規則
- [ ] dry-runとvalidation

このチェックリストを完了するまでは有料API runを開始しない。

# PF-EXP-0005 pilot-002 summary

> Result: **OVERALL PASS**  
> Experiment: PF-EXP-0005  
> Phase: pilot-002  
> Target hypothesis: H-VB01 `Values & Beliefs → Experience`  
> Canonical model at execution: APRL Personality Formation Model v1.2

## Conclusion

PF-EXP-0005 pilot-002は、事前に固定したpretest P1〜P5とmain confirmatory gate G1〜G5をすべてPASSした。

この結果は、今回の実験条件において、

> **同一のSituation・Perception・neutral Relationshipのもとでも、Values & Beliefsの違いによってExperienceの意味が再現可能かつ方向整合的に変化する。**

ことを支持する。

したがってH-VB01 `Values & Beliefs → Experience` はpilot-002で支持された。また、同一Perceptionを固定したままValues & Beliefsのみを操作してExperience差が生じたため、Personality Formation Model v1.2におけるPerception / Experienceの**機能的分離**にも限定的な経験的支持を与える。

## Execution

- pretest: planned 24 / succeeded 24 / missing 0
  - VB quality: 16
  - Perception boundary: 8
- main Experience generation: planned 48 / succeeded 48 / missing 0
- blind evaluation: planned 48 / succeeded 48 / missing 0
- generation model: `gpt-5.6`
- evaluation model: `gpt-5.6`
- Gate / thresholdはpilot-001 FAIL後も変更していない

## Pretest result

| Gate | Result | Observed | Threshold |
|---|---|---:|---:|
| P1 VB separation | **PASS** | Learning separation 4.0; Evaluation separation 4.0; family direction 8/8 | >=2.0; >=2.0; >=7/8 |
| P2 No current-response directiveness | **PASS** | mean 0.0; max 0.0 | mean <=0.50; max <=1 |
| P3 No current-situation leakage | **PASS** | mean 0.0; max 0.0 | mean <=0.50; max <=1 |
| P4 Perception boundary | **PASS** | mean 0.50; max 1.0 | mean <=0.50; max <=1 |
| P5 Relationship neutrality | **PASS** | mean 0.0; max 0.0 | mean <=0.50; max <=1 |

`all_gates_pass = true`

P4は閾値上限でPASSした。したがって、Perception / Experience境界が完全に明瞭であると主張するのではなく、**今回のmainを実施するために事前定義した境界品質を満たした**と解釈する。

## Main confirmatory result

| Gate | Result | Observed | Threshold |
|---|---|---:|---:|
| G1 Learning meaning effect | **PASS** | `ΔL = 3.5417` | >=0.75 |
| G2 Evaluation-threat meaning effect | **PASS** | `ΔE = 2.5833` | >=0.75 |
| G3 Family generalization | **PASS** | 8/8 families dual-positive | >=6/8 |
| G4 Leave-one-family-out robustness | **PASS** | min LOO `ΔL = 3.4762`; min LOO `ΔE = 2.4286` | both >0 |
| G5 Experience boundary quality | **PASS** | response leakage mean 0.0417; max 1.0 | mean <=0.50; max <=1 |

`all_gates_pass = true`

Condition means:

- `learning_mean_VB-L = 3.5833`
- `learning_mean_VB-E = 0.0417`
- `evaluation_threat_mean_VB-L = 1.4167`
- `evaluation_threat_mean_VB-E = 4.0`

全8 familyで `ΔL_f > 0` かつ `ΔE_f > 0` を満たした。

## Family effects

| Family | Δ Learning meaning | Δ Evaluation threat | Dual positive |
|---|---:|---:|---|
| F01 | 3.6667 | 2.0000 | yes |
| F02 | 3.0000 | 1.3333 | yes |
| F03 | 3.0000 | 2.0000 | yes |
| F04 | 3.6667 | 2.6667 | yes |
| F05 | 3.6667 | 3.3333 | yes |
| F06 | 4.0000 | 2.3333 | yes |
| F07 | 3.3333 | 3.6667 | yes |
| F08 | 4.0000 | 3.3333 | yes |

## Secondary observations

以下はconfirmatory gateではなく探索的結果としてのみ扱う。

- Experience valence mean: VB-L `0.0417` / VB-E `-2.0`
- Experience arousal mean: VB-L `2.5417` / VB-E `3.0417`
- dual-meaning coactivation rate: `0.25`
- VB lexical repetition mean: `0.1346`

25%のExperienceでLearning meaningとEvaluation-threat meaningが同時に一定以上観測された。この結果は、両者が単純な一軸の両極ではなく共存し得る可能性を示唆するが、本pilotでは探索的観察に留める。

## Interpretation boundary

本pilotが直接支持するのは、

> **固定されたSituation・Perception・neutral Relationshipのもとで、Learning / ImprovementとEvaluation / Competence-protectionというValues & Beliefs contrastが、生成されるExperienceの意味を対応する方向へ変化させ得る。**

という限定された主張である。

本pilotだけでは次を主張しない。

- PerceptionとExperienceが人間心理において完全に離散した二段階であること
- `Relationship → Experience` の効果
- `Experience → Response` の効果
- Values & Beliefsの自然な形成・更新機構
- Learning / Evaluation以外のValues & Beliefs次元への一般化
- 実世界の人間への一般化
- 別モデル・人手Evaluatorでも同じ効果量が再現されること

特にgenerationとblind evaluationの双方に`gpt-5.6`を用いているため、同一モデル体系内の意味整合性が結果を強めた可能性は残る。独立Evaluatorまたは人手blind評価による再評価は、次の堅牢性確認候補とする。

## Model implication

Personality Formation Model v1.2の

`E_t = h(P_t, VB_t, Rel_t)`

のうち、pilot-002は **`VB_t → E_t` の条件付き寄与**を支持した。

同じPerceptionを固定した状態でValues & Beliefsだけを変えてExperience差が生じたため、現時点ではPerceptionとExperienceを統合するより、両者を機能的に分離したv1.2の構造を維持する方が実験結果と整合する。

一方、`Rel_t → E_t` は未検証であるため、式全体が検証済みになったとは扱わない。

## Audit

- pilot-001は `PRETEST FAIL / main not run` のまま保持する
- pilot-002のGate / thresholdは実行後に変更しない
- Raw generation / evaluation responsesは公開しない現行方針を維持する
- 本結果をPF-EXP-0001〜0004の事後的な再判定には使用しない

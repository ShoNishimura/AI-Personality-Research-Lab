# PF-EXP-0006 pilot-001 summary

> Result: **OVERALL PASS**  
> Experiment: PF-EXP-0006  
> Phase: pilot-001  
> Target hypothesis: H-REL01 `Trust within Relationship → Experience`  
> Canonical model at execution: APRL Personality Formation Model v1.2

## Conclusion

PF-EXP-0006 pilot-001は、事前に固定したpretest P1〜P5とmain confirmatory gate G1〜G5をすべてPASSした。

この結果は、今回の実験条件において、

> **同一のSituation・Perception・target-neutral Values & Beliefsのもとでも、特定相手とのTrust状態の違いによってExperienceの意味が再現可能かつ方向整合的に変化する。**

ことを支持する。

したがってH-REL01 `Trust within Relationship → Experience` はpilot-001で支持された。PF-EXP-0005 pilot-002の `Values & Beliefs → Experience` と合わせると、Personality Formation Model v1.2の `E_t = h(P_t, VB_t, Rel_t)` において、Values & BeliefsとRelationshipのTrust状態をそれぞれ独立に操作してExperienceへの条件付き寄与を確認したことになる。

## Execution

- pretest: 24 evaluated
  - Relationship quality: 16
  - Perception boundary: 8
- main blind evaluation: 48 evaluated
- generation model: `gpt-5.6`
- evaluation model: `gpt-5.6`
- pretest model: `gpt-5.6`
- Gate / threshold / stimulus / prompt / schemaはmain実行前に固定した

## Pretest result

| Gate | Result | Observed | Threshold |
|---|---|---:|---:|
| P1 Trust separation | **PASS** | Trust separation 3.125; Distrust separation 3.0; family direction 8/8 | >=2.0; >=2.0; >=7/8 |
| P2 No current-response directiveness | **PASS** | mean 0.0; max 0.0 | mean <=0.50; max <=1 |
| P3 No current-situation leakage | **PASS** | mean 0.0; max 0.0 | mean <=0.50; max <=1 |
| P4 Trust isolation | **PASS** | generalized VB 0.0/0.0; Closeness-Affection 0.0/0.0; Power-Dependency 0.0/0.0 | each mean <=0.50; max <=1 |
| P5 Perception boundary | **PASS** | Experience meaning preload mean 0.0; max 0.0 | mean <=0.50; max <=1 |

`all_gates_pass = true`

全8 familyでTrust / Distrustの操作方向が正だった。P4では、Trust packetが一般化Values & Beliefs、Closeness / Affection、Power / Dependencyを同時に操作しているというleakageは観測されなかった。

## Main confirmatory result

| Gate | Result | Observed | Threshold |
|---|---|---:|---:|
| G1 Benign / good-faith meaning effect | **PASS** | `Delta_B = 2.5833` | >=0.75 |
| G2 Suspicious / adverse-intent meaning effect | **PASS** | `Delta_S = 2.0417` | >=0.75 |
| G3 Family generalization | **PASS** | 8/8 families dual-positive | >=6/8 |
| G4 Leave-one-family-out robustness | **PASS** | min LOO `Delta_B = 2.4762`; min LOO `Delta_S = 1.9048` | both >0 |
| G5 Experience boundary quality | **PASS** | response leakage mean 0.125; max 1.0 | mean <=0.50; max <=1 |

`all_gates_pass = true`

Condition means:

- `benign_mean_REL-T = 2.7917`
- `benign_mean_REL-D = 0.2083`
- `suspicious_mean_REL-T = 0.2083`
- `suspicious_mean_REL-D = 2.25`

全8 familyで `Delta_B_f > 0` かつ `Delta_S_f > 0` を満たした。

## Family effects

| Family | Delta benign / good-faith | Delta suspicious / adverse-intent | Dual positive |
|---|---:|---:|---|
| F01 | 2.6667 | 1.6667 | yes |
| F02 | 2.0000 | 1.3333 | yes |
| F03 | 3.3333 | 3.0000 | yes |
| F04 | 3.0000 | 1.3333 | yes |
| F05 | 2.6667 | 3.0000 | yes |
| F06 | 2.3333 | 2.3333 | yes |
| F07 | 1.6667 | 2.3333 | yes |
| F08 | 3.0000 | 1.3333 | yes |

## Leave-one-family-out

| Excluded family | Delta benign / good-faith | Delta suspicious / adverse-intent |
|---|---:|---:|
| F01 | 2.5714 | 2.0952 |
| F02 | 2.6667 | 2.1429 |
| F03 | 2.4762 | 1.9048 |
| F04 | 2.5238 | 2.1429 |
| F05 | 2.5714 | 1.9048 |
| F06 | 2.6190 | 2.0000 |
| F07 | 2.7143 | 2.0000 |
| F08 | 2.5238 | 2.1429 |

## Secondary observations

以下はconfirmatory gateではなく探索的結果としてのみ扱う。

- Experience valence mean: REL-T `0.0833` / REL-D `-0.9583`
- Experience arousal mean: REL-T `1.1667` / REL-D `1.25`
- dual-meaning coactivation rate: `0.0208`
- Relationship lexical repetition mean: `0.0433`

REL-T / REL-Dでvalence差は観測されたが、arousal差は小さい。good-faith meaningとsuspicious meaningの強い共存も少なかった。ただし、いずれもconfirmatory resultではない。

## Design hashes

pretest解析時に記録されたdesign hashは次のとおり。

| File | SHA-256 |
|---|---|
| `experiment.yaml` | `c03ac9c2189e5dcbb962492a1a6b0bfe418583d7b3db655846c8824136f43cab` |
| `stimuli.yaml` | `f91eed4fa4aa382b8b35250d625bcc965839d851250395cc53f5a332884763d5` |
| `thresholds.yaml` | `cdd5468bb78719190ed8a8084e5439cb67d8ae0d96f2b49f0aa4d5441646ea5e` |
| `output.schema.json` | `cee665f687b9fa2be9c881dd0610af7ed2703f252d26a1f7d90f0e8da08b7b3c` |
| `evaluation.schema.json` | `37d4ac5dcbf6dc783aa9b78d1517e80b8934012ac3261cd9ca2c8b0872f6f507` |
| `pretest.schema.json` | `ceeaa25e49f7b57acfa520137e91c7d22cdcaed588279c9c90c3e963e0178f22` |
| `prompts/system.md` | `a82fba9c6d0e1c18df448783a54d77435b44e08be71badd9932d77dbb946df17` |
| `prompts/task.md` | `74fcd0e4982baada8e046e0ff9be1b10f6aba6daac5d9aca7662c5ad19988498` |
| `prompts/evaluator-system.md` | `13785a7fd69b04f196b1217407e8caf1cd65ce95a74732457e80c3329e29a52a` |
| `prompts/evaluator-task.md` | `702148a4e3feeee86b44955397d6681f0e6fef9ec2b76897b510455a013d02bf` |
| `prompts/pretest-system.md` | `40ca12ffa985e66daf14c5ea459602bc187e5d8fb73cdfbd41d972cade9c8575` |
| `prompts/pretest-task.md` | `7a8fe8de87a12b73736c687abb9fe54712ca13e8355203fefc7af8f6be716629` |

## Interpretation boundary

本pilotが直接支持するのは、

> **固定されたSituation・Perception・target-neutral Values & Beliefsのもとで、特定相手とのTrust状態の違いが、生成されるExperienceの意味を対応する方向へ変化させ得る。**

という限定された主張である。

本pilotだけでは次を主張しない。

- Relationship全体がTrust一軸で十分であること
- Trust以外のRelationship次元へ一般化できること
- Relationshipの自然な形成・更新機構
- Relationshipが自然なPerception形成へ影響しないこと
- `Experience → Response` の効果
- 実世界の人間への一般化
- 別モデル・人手Evaluatorでも同じ効果量が再現されること

特にgeneration、pretest、blind evaluationのすべてに`gpt-5.6`を用いているため、同一モデル体系内の意味整合性が結果を強めた可能性は残る。独立Evaluatorまたは人手blind評価による再評価は、引き続き堅牢性確認候補とする。

## Model implication

Personality Formation Model v1.2の

`E_t = h(P_t, VB_t, Rel_t)`

のうち、pilot-001は **Relationship内のTrust状態による `Rel_t → E_t` の条件付き寄与**を支持した。

PF-EXP-0005とPF-EXP-0006を合わせると、同一Perceptionを固定した状態で、Values & BeliefsとRelationshipのTrust状態をそれぞれ独立に変更してExperience差を観測している。したがって、現時点ではExperienceを `P_t` のみへ縮約するより、`VB_t` と `Rel_t` を独立入力として保持するv1.2の構造が実験結果と整合する。

一方、Relationshipの内部次元そのものは未確定であり、TrustをRelationship全体の唯一の要素とは扱わない。

## Audit

- pilot-001のGate / threshold / stimulus / prompt / schemaは実行後に変更しない
- Raw generation / evaluation responsesは公開しない現行方針を維持する
- 本結果をPF-EXP-0001〜0005の事後的な再判定には使用しない
- Secondary observationsをconfirmatory resultへ昇格させない
- 将来Closeness / Power等を検証する場合も、本pilotの刺激・閾値・結果を書き換えない

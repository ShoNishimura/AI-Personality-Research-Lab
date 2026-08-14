# PF-EXP-0005 pilot-001 pretest summary

> Result: **PRETEST FAIL / main not run**  
> Experiment: PF-EXP-0005  
> Phase: pilot-001  
> Target hypothesis: H-VB01 `Values & Beliefs → Experience`

## Execution

- pretest planned: 16
- pretest succeeded: 16
- missing: 0
- main generation: **not run**
- blind main evaluation: **not run**

## Frozen gate result

| Gate | Result | Observed | Threshold |
|---|---|---:|---:|
| P1 VB separation | PASS | Learning separation 3.125; Evaluation separation 4.0; family direction 8/8 | >=2.0; >=2.0; >=7/8 |
| P2 No current-response directiveness | **FAIL** | mean 0.5625; max 1.0 | mean <=0.50; max <=1 |
| P3 No current-situation leakage | PASS | mean 0.0; max 0.0 | mean <=0.50; max <=1 |
| P4 Perception boundary | **FAIL** | mean 0.625; max 2.0 | mean <=0.50; max <=1 |
| P5 Relationship neutrality | PASS | mean 0.0; max 0.0 | mean <=0.50; max <=1 |

`all_gates_pass = false`

事前プロトコルに従い、main Experience generationへ進んでいない。

## Manipulation observations

VB manipulation自体は強く分離した。

- `learning_orientation_mean_VB-L = 4.0`
- `learning_orientation_mean_VB-E = 0.875`
- `learning_orientation_separation = 3.125`
- `evaluation_protection_mean_VB-L = 0.0`
- `evaluation_protection_mean_VB-E = 4.0`
- `evaluation_protection_orientation_separation = 4.0`
- 8 / 8 familiesで両方向のcontrastが正

P2は0/1のみだったが、9 / 16 itemsが1となりmean Gateを超えた。内訳ではVB-Eが6 / 8、VB-Lが3 / 8で1だった。

P4ではF03 / VB-Eが2となった。また、同一familyでPerception文字列が同じにもかかわらずVB-L / VB-E間でP4 scoreが異なるfamilyがあった。pilot-001のpretestはP4評価時にもVB packetを同時提示していたため、P4をPerception単独の境界評価として分離できていなかった。

この観察はH-VB01の結果ではなく、**pilot-001 pretest測定設計の診断**として扱う。

## Interpretation boundary

pilot-001が示したのは、

> VB操作とSituation / Relationship controlの一部は事前品質基準を満たしたが、current-response directivenessとPerception / Experience boundaryの事前品質基準を満たさなかった。

ということに限る。

H-VB01 `VB → Experience` はmainを実行していないため、**未検証であり、支持も棄却もされていない**。

Perception / Experienceを分離する概念モデル自体も、このpretest FAILだけでは支持・反証しない。

## Next pilot

pilot-002では以下を行う。

- P1〜P3をSituation + VBのみで評価
- P4〜P5をSituation + Perception + Relationshipのみで評価
- P4評価時にVBを提示しない
- VB packetの行動指示性を弱める
- F03 / F06 Perceptionを修正
- thresholdは変更しない

pilot-001の実行済み結果、Gate、threshold、design hashは変更しない。

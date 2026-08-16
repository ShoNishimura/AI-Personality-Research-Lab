# Current Experiments

このディレクトリには、Primary Research TrackであるPersonality Formationの実験と監査記録を置く。現行正本は [APRL Research Framework v1.0.2](../../docs/APRL_Research_Framework.md) と [Personality Formation Model v1.2](../../docs/models/Personality_Formation_Model.md) である。

各実験は**実行時点のモデル、用語、Gate、閾値、hash、結果を監査記録として保持**し、後続の正本改訂によって書き換えない。

旧 `T0=(S,N,C)` 系列の `EXP-0001` とpilot記録は、監査履歴を保持したまま [`../legacy/canonical-v1/experiments/EXP-0001/`](../legacy/canonical-v1/experiments/EXP-0001/) へ隔離した。

## Experiment index

| ID | Status | Question |
|---|---|---|
| [PF-EXP-0001](PF-EXP-0001-temperament-interpretation/) | **pilot-002 completed / overall FAIL (G4 only)** | S / N は同一ExperienceのPerceptionへ、想定した方向の独立した偏りを与えるか |
| [PF-EXP-0002](PF-EXP-0002-opportunity-danger-interaction/) | **pilot-001 completed / overall FAIL** | Opportunityが強まるとDanger Salienceは弱まり、その弱化はHigh Sで大きくなるか |
| [PF-EXP-0003](PF-EXP-0003-concurrent-salience/) | **pilot-001 completed / overall FAIL** | High SはOpportunity Salienceを高めながらDanger Salienceを保持できるか |
| [PF-EXP-0004](PF-EXP-0004-history-conditioned-response/) | **pilot-001 pretest FAIL / main not run** | 同一Perceptionのもとで、過去の結果履歴は現在のResponseを再現可能に変えるか |
| [PF-EXP-0005](PF-EXP-0005-values-beliefs-experience/) | **pilot-002 completed / overall PASS** | 同一Situation / Perception / Relationshipのもとで、Values & Beliefsの違いはExperienceの意味を再現可能に変えるか |
| [PF-EXP-0006](PF-EXP-0006-relationship-experience/) | **pilot-001 implementation ready / pretest not run** | 同一Situation / Perception / Values & Beliefsのもとで、RelationshipのTrust状態はExperienceの意味を再現可能に変えるか |

## Experiment continuity

PF-EXP-0001〜0003の入力として用いた `Experience` は、v1.2では外部 `Situation` として概念的に対応づけられる。一方、実行時の生成対象 `Interpretation` は、v1.2でPerceptionとExperienceを分離する以前の概念であり、両者の境界そのものを直接検証したものではない。Opportunity / Danger SalienceおよびSeeking / Negative Activation等の評価は、SituationとTemperamentによるPerception側の偏りを観測する指標として引き続き参照できる。実行済みデータ、Gate、閾値、hash、集計結果は変更しない。

PF-EXP-0001 pilot-002ではS / Nの主効果と弁別性は確認されたが、Conflict coactivationの事前Gate G4を未達とした。

PF-EXP-0002では、High SがOpportunityによるDanger attenuationを強めるという仮説は支持されなかった。

PF-EXP-0003では、OpportunityとDangerが同時に高いSalienceを持ち得ることは観測されたが、その同時保持がHigh Sによって特別に強化されるという仮説は支持されなかった。

PF-EXP-0004はv1.1の `History → Response` を単独で検証する計画だった。pilot-001はpretest P2をFAILしたためmainへ進まず、confirmatory hypothesisは未検証である。

Personality Formation Model v1.2では、一次入力をSituationへ分離し、Experienceを主観的経験として再定義し、HistoryをMinimum Modelから外してValues & Beliefsを導入した。これは後続モデルの変更であり、上記実験結果の事後的な再判定には使用しない。

PF-EXP-0005はv1.2の `E_t=h(P_t,VB_t,Rel_t)` のうち `VB → Experience` を単独検証した。pilot-001はP2 / P4 pretest FAILでmainへ進まなかった。pilot-002ではGateとthresholdを変えず、VB qualityとPerception boundaryのpretestを分離した結果、P1〜P5をすべてPASSした。その後main generation 48 / 48、blind evaluation 48 / 48を完了し、G1〜G5をすべてPASSした。`ΔL=3.5417`、`ΔE=2.5833`、8 / 8 familyでdual-positive effectを確認したため、今回の実験条件ではH-VB01 `VB → Experience` を支持する。詳細は [`PF-EXP-0005/reports/pilot-002-summary.md`](PF-EXP-0005-values-beliefs-experience/reports/pilot-002-summary.md) を参照する。

この結果は、同一Perceptionを固定したままValues & Beliefsのみを変えてExperience差が生じ得ることを示し、Perception / Experienceの機能的分離にも限定的な支持を与える。一方、`Relationship → Experience`、人間への一般化、独立Evaluatorによる再現は未検証である。

PF-EXP-0006は、この未検証部分のうち `Relationship → Experience` を次に単独検証する。pilot-001ではSituation、Perception、target-neutral Values & Beliefsを固定し、RelationshipのTrust状態だけをREL-T / REL-Dで操作する。8つのrelationship-generic scenario family、split pretest 24件、main generation 48件、blind evaluation 48件の実行系を実装済みで、pretestは未実行である。Relationship qualityとPerception boundaryのpretestを分離し、P4ではgeneralized VB / Closeness-Affection / Power-Dependencyへのcross-dimension leakageを別々に監査する。Trust以外のRelationship次元はpilot-001では扱わない。

現行系列では、実験IDに `PF-`（Personality Formation）prefixを付け、旧系列の `EXP-0001` と区別する。

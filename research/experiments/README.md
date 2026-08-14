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
| [PF-EXP-0005](PF-EXP-0005-values-beliefs-experience/) | **pilot-001 pretest FAIL / main not run; pilot-002 ready** | 同一Situation / Perception / Relationshipのもとで、Values & Beliefsの違いはExperienceの意味を再現可能に変えるか |

## Experiment continuity

PF-EXP-0001〜0003の入力として用いた `Experience` は、v1.2では外部 `Situation` として概念的に対応づけられる。一方、実行時の生成対象 `Interpretation` は、v1.2でPerceptionとExperienceを分離する以前の概念であり、両者の境界そのものを直接検証したものではない。Opportunity / Danger SalienceおよびSeeking / Negative Activation等の評価は、SituationとTemperamentによるPerception側の偏りを観測する指標として引き続き参照できる。実行済みデータ、Gate、閾値、hash、集計結果は変更しない。

PF-EXP-0001 pilot-002ではS / Nの主効果と弁別性は確認されたが、Conflict coactivationの事前Gate G4を未達とした。

PF-EXP-0002では、High SがOpportunityによるDanger attenuationを強めるという仮説は支持されなかった。

PF-EXP-0003では、OpportunityとDangerが同時に高いSalienceを持ち得ることは観測されたが、その同時保持がHigh Sによって特別に強化されるという仮説は支持されなかった。

PF-EXP-0004はv1.1の `History → Response` を単独で検証する計画だった。pilot-001はpretest P2をFAILしたためmainへ進まず、confirmatory hypothesisは未検証である。

Personality Formation Model v1.2では、一次入力をSituationへ分離し、Experienceを主観的経験として再定義し、HistoryをMinimum Modelから外してValues & Beliefsを導入した。これは後続モデルの変更であり、上記実験結果の事後的な再判定には使用しない。

PF-EXP-0005はv1.2の `E_t=h(P_t,VB_t,Rel_t)` のうち `VB → Experience` を単独検証する。pilot-001はpretest 16/16を完了したが、P2 No current-response directivenessとP4 Perception boundaryをFAILしたためmainを実行していない。H-VB01は未検証である。pilot-002ではGateとthresholdを変えず、P1〜P3のVB quality評価とP4〜P5のPerception boundary評価を分離し、P4評価時にVBを提示しない。

現行系列では、実験IDに `PF-`（Personality Formation）prefixを付け、旧系列の `EXP-0001` と区別する。

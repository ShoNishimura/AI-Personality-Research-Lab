# Current Experiments

このディレクトリには、現行の [APRL Research Framework v1.0.1](../../docs/APRL_Research_Framework.md) と [Personality Formation Model v1.1](../../docs/models/Personality_Formation_Model.md) に基づく実験だけを置く。

旧 `T0=(S,N,C)` 系列の `EXP-0001` とpilot記録は、監査履歴を保持したまま [`../legacy/canonical-v1/experiments/EXP-0001/`](../legacy/canonical-v1/experiments/EXP-0001/) へ隔離した。

現在は人格形成をPrimary Research Trackとする。

## Experiment index

| ID | Status | Question |
|---|---|---|
| [PF-EXP-0001](PF-EXP-0001-temperament-interpretation/) | **pilot-002 completed / overall FAIL (G4 only)** | S / N は同一ExperienceのPerceptionへ、想定した方向の独立した偏りを与えるか |
| [PF-EXP-0002](PF-EXP-0002-opportunity-danger-interaction/) | **pilot-001 completed / overall FAIL** | Opportunityが強まるとDanger Salienceは弱まり、その弱化はHigh Sで大きくなるか |
| [PF-EXP-0003](PF-EXP-0003-concurrent-salience/) | **pilot-001 completed / overall FAIL** | High SはOpportunity Salienceを高めながらDanger Salienceを保持できるか |
| [PF-EXP-0004](PF-EXP-0004-history-conditioned-response/) | **implementation ready / pretest not run** | 同一Perceptionのもとで、過去の結果履歴は現在のResponseを再現可能に変えるか |

## Current interpretation

PF-EXP-0001〜0003は、実行時には生成対象を `Interpretation` と呼んでいた。Personality Formation Model v1.1では、それらのOpportunity / Danger SalienceおよびSeeking / Negative Activationを **Perceptionの観測**として再位置づける。実行済みデータ、Gate、閾値、hash、集計結果は変更しない。

PF-EXP-0001 pilot-002ではS / Nの主効果と弁別性は確認されたが、Conflict coactivationの事前Gate G4を未達とした。

PF-EXP-0002では、High SがOpportunityによるDanger attenuationを強めるという仮説は支持されなかった。

PF-EXP-0003では、OpportunityとDangerが同時に高いSalienceを持ち得ることは観測されたが、その同時保持がHigh Sによって特別に強化されるという仮説は支持されなかった。

PF-EXP-0004はResponse側へ進む最初の実験として、`R_t=g(P_t,H_t,Rel_t)` のうち **History → Response** を単独で検証する。Perceptionを固定し、Relationshipをneutral / noneに固定して、類似状況における過去Responseの結果履歴だけを操作する。実装は完了しているが、history pretestおよびpilot-001はまだ実行していない。

現行系列では、実験IDに `PF-`（Personality Formation）prefixを付け、旧系列の `EXP-0001` と区別する。

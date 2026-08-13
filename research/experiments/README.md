# Current Experiments

このディレクトリには、現行の [APRL Research Framework v1.0](../../docs/APRL_Research_Framework.md) と [Personality Formation Model v1.0](../../docs/models/Personality_Formation_Model.md) に基づく実験だけを置く。

旧 `T0=(S,N,C)` 系列の `EXP-0001` とpilot記録は、監査履歴を保持したまま [`../legacy/canonical-v1/experiments/EXP-0001/`](../legacy/canonical-v1/experiments/EXP-0001/) へ隔離した。

現在は人格形成をPrimary Research Trackとする。

## Experiment index

| ID | Status | Question |
|---|---|---|
| [PF-EXP-0001](PF-EXP-0001-temperament-interpretation/) | **pilot-002 completed / 4 of 5 gates passed** | S / N は同一ExperienceのInterpretationへ、想定した方向の独立した偏りを与えるか |
| [PF-EXP-0002](PF-EXP-0002-opportunity-danger-interaction/) | **pilot-001 completed / target interaction not supported** | Opportunityが強まるとDanger Salienceは弱まり、その弱化はHigh Sで大きくなるか |
| [PF-EXP-0003](PF-EXP-0003-concurrent-salience/) | **planned / gates frozen before responses** | High SはOpportunity Salienceを高めながらDanger Salienceを保持できるか |

PF-EXP-0001 pilot-001はgeneration 89/96でtechnical incomplete。pilot-002は96/96 generation・96/96 evaluationを完了し、G1/G2/G3/G5をPASS、G4のみ事前閾値を未達とした。

PF-EXP-0001のGate判定後に見つかった `ST-C-01` のsub-additive patternはDiscovery扱いせず、PF-EXP-0002で独立に検証した。PF-EXP-0002はstimulus pretest・Temperament主効果をPASSしたが、High SでOpportunityがDangerをより弱めるというtarget interactionは支持されなかった。

PF-EXP-0002のGate判定後の記述分析では、High S / High NでOpportunity Salienceが高まりつつDanger Salienceが保持される探索的patternが見えた。このpost-hoc observationもDiscovery扱いせず、PF-EXP-0003の独立仮説として事前固定する。

現行系列では、実験IDに `PF-`（Personality Formation）prefixを付け、旧系列の `EXP-0001` と区別する。

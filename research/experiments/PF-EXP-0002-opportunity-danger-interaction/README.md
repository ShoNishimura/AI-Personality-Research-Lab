# PF-EXP-0002 — Opportunity × Danger Interaction

> Status: **completed / target interaction not supported**  
> Current Canonical Model: [Personality Formation Model v1.1](../../../docs/models/Personality_Formation_Model.md)  
> Execution-time term: **Interpretation**

## Terminology alignment

PF-EXP-0002はv1.0時点で実行され、生成対象を `Interpretation` と呼んでいた。

v1.1では、Opportunity Salience / Danger Salience / Seeking Activation / Negative Activationを **Perceptionの観測量**として再位置づける。

実行済みprompt、schema、config、artifact field、Gate、閾値、hash、集計結果は変更しない。

## Research Question

> **Opportunity Valueが高くなるとDanger Salienceは弱まり、その弱化はSeeking ReactivityがHighのとき大きいか。**

現行モデルでは、Experience特性とTemperamentがPerceptionへ与える相互作用を検証した実験として扱う。

## Design

`S × N × Opportunity × Danger = 2 × 2 × 2 × 2`

6 scenario families × 4 O/D variants × 4 S/N conditions × 2 replicates = **192 runs**。

blind evaluatorは実行時名称 `Interpretation` の生成テキストから次を0–4で評価した。

- Opportunity Salience
- Danger Salience
- Seeking Activation
- Negative Activation

## Result

- pretest: **24/24**
- generation: **192/192**
- blind evaluation: **192/192**
- Seeking main effect: **1.271**
- Negative main effect: **1.021**
- primary interaction: **+0.250**（事前仮説は負方向）
- G1/G2: **PASS**
- G3/G4: **FAIL**
- overall: **FAIL**

事前Gateは変更していない。

詳細は [`reports/pilot-001-summary.md`](reports/pilot-001-summary.md) を参照。

## Post-gate observation

N=High / Danger=Highの記述分析では、T11でOpportunity Salienceが高い場合にもDanger Salienceが維持される探索的patternが見られた。

このpatternはDiscovery扱いせず、PF-EXP-0003で新規stimuliを用いて独立検証した。

## v1.1 interpretation of the result

PF-EXP-0002は現行モデルの `P=f(E,T0)` に対応するPerception実験である。

Response、History、Relationshipについての結論は含まない。
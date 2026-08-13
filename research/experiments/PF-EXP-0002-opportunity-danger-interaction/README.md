# PF-EXP-0002 — Opportunity × Danger Interaction

> Personality Formation Model v1.0  
> Pilot-001  
> Status: **completed / target interaction not supported**

## 30秒概要

PF-EXP-0001の事後探索から、次を新しい6 scenario familyで検証した。

> **Opportunity Valueが高くなるとDanger Salienceは弱まり、その弱化はSeeking ReactivityがHighのとき大きいか。**

Stimulus pretestとS/N主効果はPASSしたが、target interactionは支持されなかった。

- pretest: **24/24**
- generation: **192/192**
- blind evaluation: **192/192**
- Seeking main effect: **1.271**
- Negative main effect: **1.021**
- frozen primary interaction: **+0.250**（仮説は負方向）
- Gate: **G1/G2 PASS, G3/G4 FAIL**

正式な集計・監査結果は [`reports/pilot-001-summary.md`](reports/pilot-001-summary.md) を参照。

## Design

`S × N × Opportunity × Danger = 2 × 2 × 2 × 2`

6 scenario families × 4 O/D variants × 4 S/N conditions × 2 replicates = **192 runs**。

PF-EXP-0001のstimulus本文は再利用していない。

CharacterはInterpretationのみ生成し、blind evaluatorが0–4で次を評価した。

- Opportunity Salience
- Danger Salience
- Seeking Activation
- Negative Activation

## Frozen hypothesis

`N=High` / `Danger=High`で、

`C = [Danger(T11,O-high)-Danger(T11,O-low)] - [Danger(T01,O-high)-Danger(T01,O-low)]`

を計算した。

事前仮説は `C < 0`。

Pilot Gateは、

- mean `C <= -0.50`
- 6 family中4以上で `C < 0`
- leave-one-family-out meanの最大値 `<= -0.25`

として事前固定した。

実測は `C = +0.250` で、6 family中0 familyが負方向だった。Gateは事後変更していない。

## Post-gate descriptive observation

N=High / Danger=Highの4セルをscoreだけで記述すると、T11ではOpportunity High時にもDanger Salienceが低下しなかった。

| Condition | Opportunity | Opportunity Salience | Danger Salience |
|---|---|---:|---:|
| T01 | Low | 0.917 | 3.250 |
| T01 | High | 2.333 | 3.083 |
| T11 | Low | 2.083 | 2.750 |
| T11 | High | 3.000 | 2.833 |

このpatternは**探索的**であり、Discovery扱いしない。

次の独立pilot [PF-EXP-0003 — Concurrent Salience](../PF-EXP-0003-concurrent-salience/) で、新規stimuliを用いて検証する。

## Data / audit

- Raw InterpretationはGit管理外
- Raw Interpretation本文は研究者未閲覧
- `store=false`
- evaluationはAPI credit exhaustionで168件時点に一度中断したが、条件変更なしでresumeし192/192完了
- 正本Personality Formation Modelは変更しない

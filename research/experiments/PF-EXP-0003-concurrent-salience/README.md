# PF-EXP-0003 — Concurrent Salience

> Status: **completed / gate fail**  
> Current Canonical Model: [Personality Formation Model v1.1](../../../docs/models/Personality_Formation_Model.md)  
> Execution-time term: **Interpretation**

## Terminology alignment

PF-EXP-0003はv1.0時点の用語で実行され、生成対象を `Interpretation` と呼んでいた。

v1.1では、Opportunity / Danger SalienceおよびSeeking / Negative Activationを **Perceptionの観測量**として再位置づける。

実行済みprompt、schema、config、artifact field、Gate、閾値、hash、集計結果は変更しない。

## Research Question

> **OpportunityとDangerが同時に存在するとき、High Seeking ReactivityはOpportunity Salienceを高めながら、Danger Salienceを失わずに保持するか。**

現行モデルでは `P=f(E,T0)` に対応するPerception実験として扱う。

## Design

N=High、Danger=Highを固定し、SとOpportunityだけを操作した。

8 scenario families × 2 Opportunity variants × 2 S conditions × 3 replicates = **96 runs**。

Response、History、Relationshipは扱っていない。

## Result

- Pretest: **16 / 16 succeeded; all pretest gates passed**
- Main generation: **96 / 96 succeeded**
- Blind evaluation: **96 / 96 succeeded**
- G1: PASS
- G2: PASS
- G3: **FAIL** — primary interaction **+0.083 < +0.20**
- G4: **FAIL** — positive family interactions **4/8**、minimum leave-one-family-out **-0.048**
- G5: PASS — T11/O-high Opportunity **3.000**、Danger **2.792**、Concurrent Rate **1.000**
- Overall: **FAIL**

詳細は [`reports/pilot-001-summary.md`](reports/pilot-001-summary.md) を参照する。

## v1.1 interpretation of the result

> **OpportunityとDangerはPerception内で同時に高いSalienceを持ち得るが、その同時保持がHigh Seeking Reactivityによって特別に強化されるという証拠は得られなかった。**

このpilotから新しいConcurrent Salience機構を追加しない。Response、History、Relationshipについての結論も含まない。

## Audit boundary

数値、Gate、閾値、raw artifact、実行時field名は変更しない。`interpretation` という実行時名称は監査記録として保持する。
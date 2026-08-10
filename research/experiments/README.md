# Experiments

APRL Concept Model v1.0.3以降の現行実験を格納します。

各実験は固有のIDを持ち、仮説、反証条件、実験条件、刺激、プロンプト、出力スキーマ、実行記録、評価、分析、結果を追跡可能にします。

現行実験は、正本v1系に基づく独立した系列 `canonical-v1` として `EXP-0001` から開始します。旧 `EXP-0001` と `EXP-0002` は系列 `legacy-simulation-v0` のIDを維持したまま、[`../legacy/simulation-v0/`](../legacy/simulation-v0/) に保存します。

各実験のメタデータには、少なくとも次を記録します。

```yaml
experiment_id: EXP-0001
series: canonical-v1
canonical_model: APRL Concept Model v1.0.3
status: planned
legacy_continuation: false
```

系列をまたいで引用するときは、現行実験を `APRL-CM1-EXP-0001`、旧実験を `legacy-simulation-v0/EXP-0001` のように完全修飾し、同じ短縮IDを混同しないようにします。

## Current experiments

| ID | Title | Status |
|---|---|---|
| [`APRL-CM1-EXP-0001`](EXP-0001/) | 気質がInterpretationとResponseへ与える影響 | planned |

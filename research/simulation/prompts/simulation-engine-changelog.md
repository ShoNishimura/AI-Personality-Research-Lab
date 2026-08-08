# Simulation Engine Change Log

Simulation Engine の設計変更履歴を記録する。

目的は、

「何を変更したか」

ではなく、

「なぜ変更したか」

を残すことである。

---

# v0.1

## Date

2026-08-08

## Summary

Simulation Engine の初版を作成した。

当初は、

Simulation Engine の仕様を整理することを目的としていた。

そのため、

Purpose、

Principle、

Execution Flow などを中心とした

Specification 形式で記述した。

## Output

- Persona Output
- Reasoning
- Action
- Memory Candidate
- Decision Confidence
- Missing Information

## Findings

Simulation Engine の役割を整理できた。

一方で、

この文書は AI が実行する Prompt ではなく、

人間向けの Specification となっていた。

---

# v0.2

## Date

2026-08-08

## Trigger

EXP-0001

RUN-0001

RUN-0002

## Motivation

Simulation Engine を実際に使用した結果、

Specification よりも、

AI が直接実行できる Prompt の方が重要であることが分かった。

また、

Decision Confidence は、

Simulation Engine の主観による評価となり、

再現性が低いことが分かった。

### Changes

- simulation-engine.md を Prompt として再設計する。
- Persona Results を標準出力とする。
- Interpretation を追加する。
- Comparison を標準出力とする。
- Observation を廃止する。
- Decision Confidence を削除する。
- Missing Information を強化する。
- Persona Output を「発言」ではなく「反応」として定義する。

## Discussion

Simulation Engine が評価すべきなのは、

AI の自信ではない。

Simulation Engine が評価すべきなのは、

判断に必要な情報が十分だったかどうかである。

Decision Confidence は廃止し、

Information Sufficiency の導入を今後検討する。

Persona Output は発言のみを表すものではない。

Persona は、

- 発言する
- 沈黙する
- 表情を変える
- 行動で示す

など、

様々な方法で反応する。

そのため、

Persona Output は

「Persona として自然な反応」

として定義する。

## Status

Current

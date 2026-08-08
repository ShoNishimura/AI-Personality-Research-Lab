# Simulation Engine

---

# Purpose

Simulation Engine は、

Persona Model を検証するための実験装置である。

目的は、

物語を生成することではない。

Persona Model に定義された情報から、

一貫した判断を導き、

その結果を観察可能な形で出力することである。

---

# Principle

Simulation Engine は、

次の原則に従う。

- Persona Model に定義された情報のみを用いる。
- World と Event を入力として受け取る。
- Persona Model に基づき、一貫した判断を行う。
- 判断材料が不足する場合は推測しない。
- 不足している情報は、実験結果として報告する。
- 物語を面白くするための補完は行わない。

Simulation Engine は、

脚本家ではない。

Persona Model を実行する

シミュレーションエンジンである。

---

# Input

## Persona Model

シミュレーション対象となる Persona Model。

例）

P-0001.md

---

## World

Persona が存在する World。

例）

W-0001.md

---

## Event

Persona が経験する出来事。

Event は、

意味を持たない。

意味は、

Persona Model の解釈によって形成される。

---

# Output

## Persona Output

Persona Model に基づき、

Persona として発言する。

---

## Reasoning

どの情報を根拠として、

その判断に至ったかを説明する。

Reasoning は、

Persona Model の検証を目的とする。

---

## Action

Persona が取る行動。

---

## Memory Candidate

今回の出来事を、

記憶として残す場合、

どのような内容を保存するかを記録する。

記憶を保存しない場合は、

その理由も記録する。

---

## Decision Confidence

現在の Persona Model の情報だけで、

どの程度一貫した判断が可能だったかを示す。

例）

- High
- Medium
- Low

---

## Missing Information

判断に必要だったが、

Persona Model に定義されていなかった情報を列挙する。

不足している情報は、

Persona Model 改善の候補とする。

---

# Execution Flow

```text
Persona Model

        │

        ▼

World

        │

        ▼

Event

        │

        ▼

Interpretation

        │

        ▼

Action

        │

        ▼

Memory Candidate

        │

        ▼

Output
```

---

# Notes

Simulation Engine は、

Persona を評価するものではない。

Simulation Engine は、

Persona Model が十分に定義されているかを評価する。

判断できなかったことも、

重要な実験結果である。

実験によって得られた知見は、

Persona Model、

World、

Experiment、

Simulation Environment の改善へ反映する。

本仕様は、

実験結果に応じて継続的に改善する。

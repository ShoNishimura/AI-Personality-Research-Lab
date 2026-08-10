# Simulation 

このフォルダには、

AI Personality Research Lab における
人格形成シミュレーションの実験基盤を格納する。

ここでは、

Character、

World、

Event、

Interaction、

Observation

を組み合わせ、

正本の4層と人格形成過程に関する仮説を検証する。

実験は[`experiment-roadmap.md`](experiment-roadmap.md)のGate順に実行する。
過去のRunにある`Persona`は正本確立前の旧称であり、新規実験では`Character`を用いる。

---

# 目的

本研究所では、

人格や創作を現実そのものとして再現することを目的としない。

研究課題に応じて、

必要な要素をモデル化し、

実験可能な形へ分解する。

そのモデルを用いてシミュレーションを行い、

観察結果からモデルを改善する。

---

# 基本構造

```text
simulation/

├── README.md
├── environment.md
├── observation-template.md
├── experiment-template.md
│
├── personas/
├── worlds/
├── rules/
├── experiments/
└── observations/

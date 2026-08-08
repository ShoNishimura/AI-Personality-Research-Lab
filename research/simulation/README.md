# Simulation

このフォルダには、

AI Personality Research Lab における
人格形成シミュレーションの実験基盤を格納する。

ここでは、

Persona、

World、

Event、

Interaction、

Observation

を組み合わせ、

人格形成や創作に関する仮説を検証する。

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

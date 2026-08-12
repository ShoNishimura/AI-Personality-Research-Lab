# N-0007

# Information Sufficiency

---

# 背景

Simulation Engineでは、

Decision Confidenceを出力していた。

しかし、

Decision Confidenceは、

LLM自身の主観的な評価であり、

客観的な再現性を持たない。

---

# 気付き

Simulation Engineが評価すべきなのは、

AIの自信ではない。

判断に必要な情報が、

十分に与えられていたかどうかである。

---

# 例

今回の実験では、

Eventは比較的具体的であった。

一方、

Worldの情報は少なかった。

そのため、

判断は可能だったが、

Worldに依存する解釈については、

十分な検証ができなかった。

---

# 提案

Decision Confidenceを、

Information Sufficiencyへ置き換えることを検討する。

評価対象は、

- Persona Model
- World
- Event

それぞれについて、

判断に十分な情報が与えられていたかを記録する。

---

# 今後

Information Sufficiencyを導入するかどうかは、

今後の実験結果を踏まえて判断する。

現時点では、

概念のみを記録し、

Simulation Engineへの導入は保留とする。

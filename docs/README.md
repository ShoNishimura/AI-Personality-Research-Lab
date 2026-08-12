# Documentation

このフォルダには、AI Personality Research Lab（APRL）の**現行正本だけ**を置く。

APRLの正本は、2026-08-12から次の二段構造で管理する。

## Canonical documents

| Layer | Canonical document | Role |
|---|---|---|
| Upper | [APRL Research Framework v1.0](APRL_Research_Framework.md) | GRQとAPRL全体の研究地図を定義する |
| Current Research Model | [Personality Formation Model v1.0](models/Personality_Formation_Model.md) | 直近の研究対象である人格形成の詳細モデルを定義する |

両者は**独立してversioning**する。下位Research Modelの改訂だけで、上位Frameworkのversionを上げる必要はない。

## Supporting document

- [Glossary](glossary.md) — 現行Framework / Modelで用いる共通語彙

## Historical documents

旧版・旧概念を含む文書は `docs/` に混在させない。

- [Legacy Research Archive](../research/legacy/README.md)
- [旧Concept Model v1.0と二段構造への仕分け](../research/legacy/concept-model-v1/README.md)

旧Manifesto、Philosophy、Personality Theory、AI Personality Blueprintは [pre-canonical archive](../research/legacy/pre-canonical/) へ隔離した。

## Documentation principle

- `docs/`：現行正本と、それに整合する現行用語だけ
- `research/`：問い、仮説、実験、発見
- `research/legacy/`：旧版・旧モデル・旧実験。読み取り専用の研究史

一つの概念の正本は一か所に置き、詳細化が必要な場合は上位Frameworkへ詰め込まず、下位Research Modelとして分離する。
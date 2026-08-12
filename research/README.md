# Research

このディレクトリには、APRLの問いから検証、発見までの研究過程を記録する。

現行研究は、上位の [APRL Research Framework v1.0](../docs/APRL_Research_Framework.md) と、直近のPrimary Research Modelである [Personality Formation Model v1.0](../docs/models/Personality_Formation_Model.md) との整合性を確認する。

## Current focus

**Primary Research Track: Personality Formation**

中心的な問いは、

**「人格はどのように形成されるのか。」**

である。

## Directory roles

| Directory | Role |
|---|---|
| [`notes/`](notes/) | 現行Framework / Modelに整合する問い、仮説、未確定の考察 |
| [`experiments/`](experiments/) | 現行モデルを検証する実験設計、実行記録、分析、報告 |
| [`discoveries/`](discoveries/) | 現行系列の実験結果から得られた根拠付きの発見 |
| [`legacy/`](legacy/) | 旧版、旧モデル、旧実験を隔離した読み取り専用Archive |

研究は原則として `notes → experiments → discoveries → docs/models` と進める。

APRL全体のFrameworkを変更する必要がある発見だけを、十分な検証後に `docs/APRL_Research_Framework.md` へ反映する。

## Canonical reset

2026-08-12の二段構造化に伴い、旧 `T0=(S,N,C)` を用いた `EXP-0001` は [`legacy/canonical-v1/`](legacy/canonical-v1/) へ移した。

その実験記録は研究史・監査資料として保持するが、現行 `T0=(S,N)` + Regulation分離モデルの直接的な検証結果とはみなさない。

初期のNotes、D-0001、旧Manifesto / Philosophy等も [`legacy/pre-canonical/`](legacy/pre-canonical/) へ隔離した。

新しい研究では、現行Framework / Modelのversionを実験記録に明示し、Legacy資料を現行仕様として引用しない。
# Documentation

このフォルダには、AI Personality Research Labの正本と、現在参照する補助文書を格納します。研究中の問い、実験、発見は [`research/`](../research/) に記録し、十分に検証された内容だけをここへ反映します。

## Canonical document

| Document | Version | Status | Role |
|---|---:|---|---|
| [APRL Concept Model](concept-model/APRL_Concept_Model_v1.0.3_Canonical_Edition.md) | 1.0.3 | **Canonical** | APRLの議論、設計、用語、実験の基準 |

旧版は現行ツリーに重複して置かず、Git履歴で保存します。正本を更新する場合は、最新版のファイルとVersion Historyを同時に更新してください。

## Supporting documents

| Document | Status | Treatment |
|---|---|---|
| [Manifesto](manifesto.md) | Active | 正本を補助する思想・価値観 |
| [Philosophy](philosophy.md) | Active | 正本を補助する創作哲学 |
| [Glossary](glossary.md) | `retained-for-reassessment` | 実験結果と照合し、v1.0.3との用語整合を再評価するため保持 |
| [Personality Theory](personality-theory.md) | `retained-for-reassessment` | 旧概念を実験結果と照合し、再構成の要否を評価するため保持 |
| [AI Personality Blueprint](ai-personality-blueprint.md) | `retained-for-reassessment` | Biography中心モデルとの関係を実験を通して再評価するため保持 |

`retained-for-reassessment` の文書は現行仕様ではありません。今後の実験結果との比較、概念の再評価、再構成のために保持します。内容が正本と矛盾する場合はv1.0.3を優先し、整合確認なしに現行仕様として引用しないでください。

## Documentation principle

一つの情報は一つの場所にだけ記述し、正本と補助文書の役割を分離します。文書の状態は次の語で表します。

- `Canonical`: 唯一の正本
- `Active`: 正本と整合する補助文書
- `retained-for-reassessment`: 現行仕様ではないが、実験を通じた再評価のために保持する文書
- `Superseded`: 新しい正本に置き換えられた文書

# Canonical-v1 Experiment Archive

このディレクトリは、APRL Concept Model v1.0.3時代の実験系列を保持する読み取り専用Archiveである。

この系列では旧Temperament定義 `T0=(S,N,C)` を前提としており、2026-08-12以降の現行 [Personality Formation Model v1.0](../../../docs/models/Personality_Formation_Model.md) が採用する `T0=(S,N)` とRegulation分離モデルとは一致しない。

## Included experiment

- `experiments/EXP-0001/` — 旧canonical-v1系列のEXP-0001。pilot-001 / pilot-002、runner、manifest、監査記録を含む。

PR #7で追加されたpilot-002完了記録、OpenAI client routingの明示化、エラー監査改善も、このArchiveに統合して保持する。

## Interpretation rule

この実験は研究史・再解析・監査には利用できるが、現行Personality Formation Modelの直接的な検証結果とはみなさない。

再利用する場合は、現行モデルに基づいて仮説・操作・条件・観測量を再設計する。
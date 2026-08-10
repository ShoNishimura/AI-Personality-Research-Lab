# EXP-0001 pilot-001 実験履歴

## 位置づけ

このディレクトリは、2026-08-10に実行したEXP-0001の最初のpilotを、追記専用の監査証跡として保存する。

- 技術的実行: 24/24 run成功
- 状態: `completed_with_design_issues`
- confirmatory利用: 不可（`confirmatory_eligible: false`）
- 正本: APRL Concept Model v1.0.3 Canonical Edition
- 実行commit: `1dfd784`
- 要求モデル: `gpt-5.6`
- 実行モデル: `gpt-5.6-sol`
- randomization seed: `20260810`
- OpenAI側の保存: `store=false`

`manifest.jsonl` は実行時manifestであり、GitHubで公開する。24件のraw run記録は内容を変更せず管理対象の非公開ストレージで保持し、raw本体と具体的な保存場所はGitHubに掲載しない。監査用にrawのレコード数、SHA-256、Git非掲載の状態だけを `status.yaml` に記録する。

## 合格基準ごとの判定

| # | 基準 | 判定 | 根拠 |
|---:|---|:---:|---|
| 1 | 24 runが予定どおり実行される | 合格 | 24レコード、run IDはすべて一意、全件`succeeded` |
| 2 | JSONスキーマ妥当率が十分に高い | 合格 | 24/24件を解析可能、必須フィールド欠落なし |
| 3 | 空応答・拒否・パース失敗・再試行が記録される | 判定保留 | 問題は0件、全件`attempt=1`で、失敗時記録は未検証 |
| 4 | requested/returned modelが記録される | 合格 | 全件で`gpt-5.6` / `gpt-5.6-sol`を記録 |
| 5 | `store`が全件`false` | 合格 | 24/24件で`false` |
| 6 | InterpretationとActionが刺激の単なる言い換えではない | 合格 | 全件に追加的解釈と具体的行動がある |
| 7 | 1〜7尺度が常に同じ値へ集中しない | 合格（注意） | 各尺度に複数値あり。ただし1は未使用、`latency=2`は12/24件 |
| 8 | 特定刺激がActionやLatencyを一方向に固定しない | 不合格 | `DEV-HN-02`は4/4件`help`、`DEV-LF-02`は2/2件`defend`かつLatency=2など |
| 9 | S・N・Cプロンプトが決定論的命令として作用しない | 不合格 | C=0のregulationは2〜3、C=1は6〜7で完全分離 |
| 10 | 条件名・仮説を伏せて人手評価できる | 不合格 | 現データには`condition_id`があり、盲検用派生データが未作成 |

## 総合判定

- 構造的hard gate: 通過
- pilot全体: 不合格／再pilotが必要
- 仮説検定・confirmatory dataへの使用: 禁止

主な設計問題は、C操作が`regulation`をほぼ直接指定している可能性、一部刺激でのAction／Latency固定傾向、盲検評価データの未作成、4レコードの文字化けである。

## 次回対応

1. Cプロンプトを弱化する。
2. 文字コード処理を修正する。
3. 条件名を除いた盲検評価用の派生データを生成する。
4. 刺激ごとの割当数を増やして固定傾向を再確認する。
5. 修正後のrunは`pilot-002`として別保存し、本データを削除・上書きしない。

raw dataの訂正が必要になった場合も保存済みraw自体は変更せず、変更理由と変換手順を伴う派生データとして追加する。

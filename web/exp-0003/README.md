# EXP-0003 実験ページ

「記憶の選び方は、人格の魅力を高めるのか」を5人程度で探索する、ビルド不要の実験ページです。

## 実施

`index.html` をブラウザで開き、同じ端末を回答者へ順番に渡します。

各回答はそのブラウザの `localStorage` にだけ保存され、ネットワークへ送信されません。実験終了後、「結果をJSONで保存」から結果を取得してください。

ローカルHTTPサーバーを使う場合：

```bash
python3 -m http.server 8000 --directory web/exp-0003
```

その後、`http://localhost:8000` を開きます。

## 集計

保存したJSONの `responses` を確認します。

Node.js がある場合は、簡易集計も実行できます。

```bash
node web/exp-0003/analyze.mjs EXP-0003-results-2026-08-10.json
```

- `selected_condition`: 選択された実験条件（`fact` / `memory_selection`）
- `reason`: 選択理由
- `improvement`: 分かりにくかった点
- `presentation_order`: 表示順
- `elapsed_ms`: 回答時間

成功条件と研究上の位置づけは [`research/simulation/experiments/EXP-0003.md`](../../research/simulation/experiments/EXP-0003.md) を参照してください。

# EXP-0001 pilot-002 execution record

このディレクトリは、EXP-0001 pilot-002の追記専用監査記録を保持する。固定manifestは公開するが、raw結果、盲検評価出力、条件対応表、blind用salt、および非公開ストレージの具体的な場所はGitHubへ含めない。

## Execution outcome

2026-08-10の再開前に、正本 `APRL Concept Model v1.0.3 Canonical Edition` と実験設計の対象（Experience、Interpretation、Response、初期Temperamentによる確率的偏り）を照合した。テスト、lint、dry-run、および固定manifestの96 run（8条件×12刺激、重複なし）を確認した後、manifest先頭のrunをカナリアとして開始した。

カナリアは初回と、事前指定された最大1回の再試行の両方でHTTP 401となった。このため大量実行を停止し、残り95 runには進まなかった。成功は0 run、失敗は1 run（2 attempts）である。pilot-002は未完了であり、盲検評価用ファイルと事後完全性検証は生成していない。

## Audit chronology

以下は既存記録を置換せず、実行再開時に把握していた経緯を追記したものである。過去事象について取得できなかった詳細は推測で補わない。

1. 過去の実行準備中にHTTP 401が発生した。
2. 過去の実行準備中にHTTP 400が発生した。
3. 過去の試行は技術的理由で中断され、pilot-002の96 runには算入されなかった。
4. 2026-08-10に、`model=gpt-5.6`、`max_output_tokens=16`、`store=false` の独立した認証テストがHTTP 200で成功した。この認証テストは実験runに算入していない。
5. 認証成功後、固定設定 `model=gpt-5.6`、`max_output_tokens=700`、`store=false` でpilot-002を再開した。
6. manifest先頭のカナリアがHTTP 401（`error.type` は取得値なし、`error.code=unauthorized_unknown`）となり、規定の1回再試行後に停止した。

raw attempt記録は内容を変更せずGit管理外で保持する。公開監査情報は [`status.yaml`](status.yaml) に限定する。

## Authentication-route diagnosis

HTTP 200だった最小POSTは、標準ライブラリのHTTPクライアントから `https://api.openai.com/v1/responses` へ直接送信し、同じプロセスの `OPENAI_API_KEY` から `Authorization: Bearer <OPENAI_API_KEY>` を組み立てていた。OrganizationおよびProjectヘッダーは付けていなかった。

修正前のrunnerは公式OpenAI Python SDKを使用していたが、引数なしの `OpenAI()` 初期化により、環境の `OPENAI_BASE_URL` を継承して標準Responses APIとは異なる経路へ送信していた。キーはSDKによって同じ `OPENAI_API_KEY` から読み込まれ、Authorization値には二重の `Bearer `、引用符、伏字、別変数の混入はなかった。OrganizationおよびProjectの環境変数は設定されていなかった。

runnerを、公式OpenAI Python SDKへ `OPENAI_API_KEY` と標準API endpointを明示的に渡す初期化へ変更した。OrganizationおよびProjectは明示的に無効化し、環境に残ったrouting metadataを継承しない。テストでは、古いbase URLとOrganization／Project値を環境へ注入しても、それらがリクエストへ入らないことを確認する。

修正後、固定manifest先頭のrunを再試行なしで診断カナリアとして1回だけ実行し、HTTP 200を得た。両経路のキーは長さ164、SHA-256先頭8文字 `218ef80b` で一致した。SDK応答からHTTPヘッダーの `x-request-id` を保存する処理が当該呼び出し時点になかったため、その値は取得不能であり、response IDで代用しない。診断指示に従い残り95 runには進んでいない。

## Resumption and completion

HTTP 200だった診断カナリアを固定manifestの正式な1件目として再利用し、再送信せず、修正済みの公式SDK経路で残り95件を実行した。95件はすべて初回attemptでHTTP 200となり、pilot-002は合計96件で完了した。成功した全runでHTTPステータスを保存し、カナリアを除く95件では `x-request-id` も保存した。カナリアの取得不能な `x-request-id` は引き続きnullとし、別の識別子では補完していない。

事後検証では、96件すべてが固定manifestと一致し、欠損0、成功runの重複0、manifest不一致0、文字化け0だった。各条件は12件ずつ（8条件×12刺激）で、各刺激は8条件へ1回ずつ割り当てられている。過去の誤経路による失敗2 attemptsは追記専用raw監査履歴に保持するが、成功済みカナリアを含む正式な96 runとは別に数える。

盲検評価用ファイルを96件で生成した。評価用ファイル、条件対応表、salt、raw結果、および具体的な非公開保存場所はGitへ含めない。公開監査情報には件数、完全性検証結果、および非公開成果物のSHA-256のみを記録する。

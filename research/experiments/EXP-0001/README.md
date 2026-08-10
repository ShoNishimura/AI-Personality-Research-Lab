# APRL-CM1-EXP-0001

## 気質がInterpretationとResponseへ与える影響

```yaml
experiment_id: EXP-0001
qualified_id: APRL-CM1-EXP-0001
series: canonical-v1
canonical_model: APRL Concept Model v1.0.3
status: planned
legacy_continuation: false
```

## 目的

初期気質 $T_0=(S,N,C)$ が、同一のExperienceに対するInterpretationとResponseへ、再現可能かつ予測可能な確率的偏りを与えるか検証する。

本実験は、正本v1.0.3の次の最小Characterモデルを最初に検証する。

$$
I_0=f(E_0,T_0,H_0)
$$

$$
R_0=g(I_0,T_0,H_0),\quad R_0=(Action_0,Intensity_0,Latency_0)
$$

$H_0$ は全条件で空に固定する。Biography、複数Character、Communicator、Audience、Biographical Resonanceは本実験の対象外とする。

## Research questions

1. $S$、$N$、$C$ の操作はInterpretationとResponseの分布に予測可能な差を生むか。
2. 三次元の気質モデルは、気質指定なし・偽操作・単一軸モデルよりholdout刺激のResponseをよく予測するか。
3. 気質とResponseの関係の一部はInterpretationを介して現れるか。
4. 観測された効果はseed、刺激、プロンプト表現を変えても方向が安定するか。

## Preregistered hypotheses

| ID | Hypothesis |
|---|---|
| H1 | 高$S$は接近・探索・発言Actionの増加と短いLatencyに関連する。 |
| H2 | 高$N$は脅威・拒絶・喪失・失敗条件で警戒・回避・防御ActionとIntensityの増加に関連する。 |
| H3 | 高$C$は優勢反応の抑制・保留・切替・調整に関連する。$C$単独ではLatencyの方向を固定しない。 |
| H4 | $S\times C$ と $N\times C$ の交互作用を含むモデルは、単一軸モデルよりholdout刺激をよく予測する。 |
| H5 | 気質操作によるResponse差の一部は、Interpretationの差によって媒介される。 |

## Design

### Experimental unit

独立したモデル呼び出し1回を1 runとする。会話履歴とrun間の状態は共有しない。

### Temperament conditions

$S$、$N$、$C$ を高・低の2水準で完全要因化した8条件を使用する。値は連続尺度の端点ではなく、同程度の強さで記述したカテゴリ操作とする。

| S | N | C | Preregistered tendency |
|---|---|---|---|
| high | high | high | 接近と警戒を認識し、状況確認後に調整して反応する |
| high | high | low | 接近または防御の優勢反応を強く早く開始する |
| high | low | high | 接近意欲を保ちつつ確認・調整して動く |
| high | low | low | 接近・探索・発言を早く直接的に開始する |
| low | high | high | 警戒しつつ反応を保留・調整する |
| low | high | low | 回避・防御を早く開始する |
| low | low | high | 観察し、必要性を判断してから動く |
| low | low | low | 反応開始の駆動が弱く、待機しやすい |

### Controls

- `no-temperament`: 気質情報を与えない。
- `sham-label`: 行動上の意味を持たないランダムなラベルを3つ与える。
- `single-axis-S`、`single-axis-N`、`single-axis-C`: 対象軸のみ高・低を操作し、他軸を指定しない。

### Experiences

以下の6 Event Typeを使用する。各Typeについて意味内容の異なる刺激を作り、開発用とholdoutに事前分割する。

1. 新奇・報酬
2. 脅威・拒絶
3. 喪失・失敗
4. 曖昧な社会的状況
5. 援助を必要とする状況
6. 接近と回避が競合する状況

各刺激は、固有名詞、性別、文化的手がかり、既知作品への連想を極力避け、条件間では同一本文を用いる。刺激セット確定後、run開始前に `stimuli.yaml` へID、Event Type、分割、本文を凍結する。

### Randomization and masking

- condition、stimulus、seedの実行順を無作為化する。
- 生成モデルには評価基準と仮説を開示しない。
- 人手評価者にはcondition、seed、仮説を伏せる。
- 自動評価で生成モデルと同系列のモデルを使う場合は、その事実を記録し、異系列モデルまたは人手評価による感度分析を行う。

### Sample size

run数はpilot完了後、confirmatory runの出力を見る前に固定する。pilotはプロンプト・スキーマ・刺激の不具合検出だけに使用し、仮説検定には含めない。

confirmatory designは次を満たす均衡計画とする。

```text
8 temperament conditions × 6 event types × K stimuli × R seeds
+ controls
```

$K$、$R$ と総run数、ならびに検出対象とする最小効果量は、費用見積りとpilot分散に基づいて `preregistration.md` に追記し、実行前にstatusを `preregistered` へ変更する。結果確認後のrun追加は禁止する。

## Procedure

1. モデル名、モデル版、推論設定、temperature、seed対応、system promptを固定する。
2. 各runにcondition promptとExperienceを与える。
3. モデルはInterpretationとResponseを [`output.schema.json`](output.schema.json) に従って返す。
4. 生出力、パース結果、エラー、再試行をすべて保存する。
5. 自動評価と、conditionを伏せた人手評価を独立に実施する。
6. 開発刺激で分析方法を確定後、holdout刺激を一度だけ評価する。

## Outcomes

### Primary outcomes

- `action_category`: 接近、探索、発言、援助、防御、回避、保留、観察、その他のカテゴリ分布
- `intensity`: 反応強度（1–7）
- `latency`: 反応開始の相対的早さ（1–7。高いほど遅い）
- holdout刺激における予測対数尤度または交差エントロピー

Latencyは実時間ではなく、出力された行動計画上の相対指標として測定する。実API応答時間はシステム負荷の影響を受けるため主要評価に含めない。

### Secondary outcomes

- Interpretationに含まれる接近価、脅威価、統制・再評価の評定
- 操作チェック（各軸の意図した表出）
- Event Typeとの交互作用
- Interpretationによる媒介
- seed・刺激・プロンプト言い換えに対する頑健性
- JSON妥当率、拒否率、再試行率

## Analysis plan

- Actionは多項ロジスティック階層モデルで分析する。
- IntensityとLatencyは順序ロジスティック階層モデルで分析する。
- conditionとEvent Type、および事前指定した $S\times C$、$N\times C$ を固定効果とし、stimulusとseedを変量効果とする。
- 三次元モデルと対照・単一軸モデルはholdout予測性能で比較する。
- Interpretationの媒介分析は探索的結果と明記し、因果媒介として断定しない。
- 効果量、区間推定、モデル診断、全条件の分布を報告する。p値だけで支持を判定しない。
- 欠損・スキーマ違反・再試行を条件別に報告し、都合のよいrunだけを除外しない。

## Exclusion and retry rules

- API障害、空応答、JSONとして復元不能な出力のみ技術的失敗とする。
- 技術的失敗は同一設定で最大1回再試行し、初回と再試行の両方を保存する。
- 内容が仮説に反すること、`other` Actionであること、弱い気質表出は除外理由にしない。
- 安全上の拒否は除外せず、Responseの一種として件数を報告する。
- 事前規則外の除外は、理由と影響を明示した感度分析としてのみ扱う。

## Falsification criteria

次の結果は、少なくとも現在の気質実装を支持しない証拠とする。

- 主要な条件差が対照条件より安定して大きくならない。
- 事前指定した効果方向が刺激、seed、プロンプト言い換えで反転する。
- 三次元モデルがholdout刺激で単一軸・対照モデルを上回らない。
- InterpretationとResponseの対応が再現されない。
- 操作チェックだけが成功し、行動上の予測力が得られない。

これは正本全体の否定ではなく、$T_0=(S,N,C)$ の操作的定義、実装方法、または最小Characterモデルにおける役割を見直す根拠とする。

## Reproducibility records

実行時には、少なくとも次を保存する。

- プロトコルとpreregistrationのcommit SHA
- モデル提供者、モデルID、取得可能なら版・snapshot
- 全推論パラメータとseed
- system・condition・task promptの完全な本文
- stimulus IDと分割
- UTC timestamp、run ID、再試行元run ID
- 生出力、構造化出力、評価値、評価者情報
- 実行コードと依存関係のlockfile
- 予定run、失敗run、除外runを含むmanifest

## Status gates

| Status | Requirement |
|---|---|
| `planned` | 本計画がレビュー可能である |
| `piloting` | 刺激、prompt、runner、評価手順を検証中である |
| `preregistered` | 刺激、run数、解析、除外規則を凍結しcommitを記録した |
| `running` | confirmatory runを実行中である |
| `analyzed` | 凍結した解析と感度分析を完了した |
| `reported` | 肯定・否定を問わず結果と全記録を公開した |

## Files planned for execution

```text
EXP-0001/
├── README.md
├── output.schema.json
├── preregistration.md
├── stimuli.yaml
├── prompts/
├── src/
├── runs/
├── analysis/
└── results/
```

本PRでは実験計画と出力スキーマだけを追加する。刺激、prompt、run数、実行コードはpilot設計時に追加し、confirmatory runの前に凍結する。

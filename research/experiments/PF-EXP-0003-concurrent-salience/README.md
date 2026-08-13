# PF-EXP-0003 — Concurrent Salience

> Personality Formation Model v1.0  
> Pilot-001  
> Status: **implemented / ready to pretest**

## 30秒概要

PF-EXP-0002では「High SでOpportunityが強まるほどDanger Salienceがより低下する」という仮説は支持されなかった。Gate判定後の記述分析では逆に、High SでOpportunity Salienceが上がってもDanger Salienceが低下しない探索的パターンが見えた。

PF-EXP-0003は新規stimuliで次を独立検証する。

> **OpportunityとDangerが同時に存在するとき、High Seeking ReactivityはOpportunity Salienceを高めながら、Danger Salienceを失わずに保持するか。**

正本 `I_t = f(E_t,T_0,H_t)` は変更しない。

## Design

N=High、Danger=Highを固定し、SとOpportunityだけを操作する2×2計画。

| Cell | Condition | S | N | Opportunity | Danger |
|---|---|---|---|---|---|
| C1 | T01 | Low | High | Low | High |
| C2 | T01 | Low | High | High | High |
| C3 | T11 | High | High | Low | High |
| C4 | T11 | High | High | High | High |

8つの新規scenario family × 2 Opportunity variants × 3 replicates。

- Pretest: **16 API requests**
- Main generation: **96 API requests**
- Blind evaluation: **96 API requests**
- Total: **208 API requests**

CharacterはInterpretationだけを生成する。Response / Regulation操作 / History / Biography / Relationshipは扱わない。

## Primary hypothesis H-CS01

`ΔD_T01 = Danger(T01,O-high) - Danger(T01,O-low)`

`ΔD_T11 = Danger(T11,O-high) - Danger(T11,O-low)`

`C_D = ΔD_T11 - ΔD_T01`

仮説方向は **`C_D > 0`**。

High SがDangerそのものを増やすという仮説ではない。Opportunityが強くなった際に、Danger SalienceをLow Sより保持するかを検証する。

## Frozen pilot gates

- **G1**: Pretest全PASS
- **G2**: Seeking main >= 0.75、T11内Opportunity Salience High−Low >= 0.50
- **G3**: T11のDanger delta >= -0.25、`C_D >= +0.20`
- **G4**: 8 family中5以上で`C_D > 0`、全leave-one-family-out mean > 0
- **G5**: T11/O-highでOpportunity Salience >=2.50、Danger Salience >=2.50、両方>=2のrun率 >=0.75

閾値はPF-EXP-0003 response観測前に固定し、事後変更しない。

## Stimulus validity

16 stimuliはPF-EXP-0001/0002本文を再利用しない。各family内ではcontextとDanger wordingを完全に同一にし、Opportunity情報だけを変更する。`src.validate` がこの構造を静的検査する。

Pretest gate:

- Opportunity High−Low mean >= 1.50
- Opportunity操作によるDanger Valueのabsolute cross-effect <= 0.50
- 8 family中7以上でOpportunity High > Low

PretestがFAILした場合、main runnerは実行を拒否する。

## Setup

```powershell
cd research\experiments\PF-EXP-0003-concurrent-salience
uv run --no-project python bootstrap_lock.py
uv sync --frozen
uv run python -m src.validate
uv run pytest -q
uv run ruff check .
```

期待:

```text
PASS: PF-EXP-0003 static validation
7 passed
All checks passed!
```

## Execution sequence

### 1. Pretest dry-run

```powershell
uv run python -m src.pretest --dry-run
```

期待: `16 runs` / no API requests。

### 2. Pretest

```powershell
uv run python -m src.pretest
```

成功条件: `succeeded: 16 / missing: 0`。

### 3. Pretest analysis

```powershell
uv run python -m src.pretest_analyze
```

`all_gates_pass: true` の場合のみmainへ進む。

### 4. Main dry-run / generation

```powershell
uv run python -m src.pilot --dry-run
uv run python -m src.pilot
```

成功条件: `succeeded: 96 / missing: 0`。

### 5. Blind set / evaluation

```powershell
uv run python -m src.blind
uv run python -m src.evaluate --dry-run
uv run python -m src.evaluate
```

成功条件: blind set 96、evaluation `succeeded: 96 / missing: 0`。

### 6. Analysis

```powershell
uv run python -m src.analyze
```

G1〜G5、cell means、family interaction、leave-one-family-out、Concurrent Salienceを出力する。

## Data / audit policy

- `store=false`
- API endpointを `https://api.openai.com/v1` に固定
- raw Interpretation / blind files / private gates / runtime environmentはGit管理外
- success済みIDはresume時にskip
- API technical errorはstatus / request ID / error code等を可能な範囲で監査
- main解析前にraw Interpretation本文を研究者が読まない

## Interpretation boundary

GateがPASSしても、AttentionやSalience Competition等の新しい内部変数を正本へ追加しない。まずholdout familyを使うconfirmatory studyへ進み、そこで再現性を確認してからモデル変更要否を判断する。

# PF-EXP-0002 — Opportunity × Danger Interaction

> Personality Formation Model v1.0  
> Pilot-001  
> Status: **ready to pretest**

## 30秒概要

PF-EXP-0001 pilot-002では、S（Seeking）とN（Negative Affectivity）の主効果と弁別性は明瞭だった一方、Conflict刺激 `ST-C-01` の事後探索で、High S / High N時に両反応が単純加算より弱くなるパターンが見つかった。

本実験はこの探索的観測から、次を新しいstimuliで検証する。

> **同じDangerを含むExperienceでもOpportunity Valueが高くなるとDanger Salienceは弱くなるか。さらに、その弱化はSeeking ReactivityがHighのとき大きいか。**

これは正本の

`I_t = f(E_t, T_0, H_t)`

における `f()` が、S/Nの単純加算ではなくExperience依存の相互作用を含み得るかを検証するpilotである。正本自体は変更しない。

---

## 1. Design

Temperament:

- S: Low / High
- N: Low / High

Experience manipulation:

- O: Opportunity Value Low / High
- D: Danger Value Low / High

完全要因計画:

`S × N × O × D = 2 × 2 × 2 × 2`

Temperament condition:

| ID | S | N |
|---|---|---|
| T00 | Low | Low |
| T01 | Low | High |
| T10 | High | Low |
| T11 | High | High |

6つのscenario familyごとに、同じ状況の `O0D0 / O0D1 / O1D0 / O1D1` を作る。

- F01: 未知の分析端末
- F02: 別経路
- F03: 外部データ源
- F04: 試作ソフトウェア
- F05: 未使用の作業機器
- F06: 共同作業の申し出

PF-EXP-0001の `ST-C-01` 本文は再利用しない。

---

## 2. Primary hypothesis

Primary analysisは `N=High` かつ `D=High` に固定する。

各scenario familyについて、

`ΔO(T01) = DangerSalience(T01,O-high,D-high) - DangerSalience(T01,O-low,D-high)`

`ΔO(T11) = DangerSalience(T11,O-high,D-high) - DangerSalience(T11,O-low,D-high)`

Primary interaction contrast:

`C = ΔO(T11) - ΔO(T01)`

仮説:

`C < 0`

すなわち、Opportunityを強くしたときのDanger Salience低下がHigh Sでより大きい。

Pilot Gateでは、

- mean `C <= -0.50`
- 6 family中4 family以上で `C < 0`
- どの1 familyを除外してもmean `C <= -0.25`

を要求する。

これはPF-EXP-0001を見た後に設定したfollow-up pilot基準であり、confirmatory evidenceとして扱わない。

---

## 3. Secondary / exploratory hypothesis

逆方向も記録する。

> Danger Valueが高くなるとOpportunity Salienceが弱まり、その弱化はHigh Nで大きくなるか。

これはgateには使わず、`reciprocal_interaction_exploratory` として保存する。

---

## 4. Pretest

Main generationより前に、24 stimulus自体をTemperamentなしでblind評価する。

評価:

- `opportunity_value` 0–4
- `danger_value` 0–4

Pretest Gate:

- Opportunity main effect >= 1.50
- Danger main effect >= 1.50
- O操作によるDangerの平均absolute cross-effect <= 0.75
- D操作によるOpportunityの平均absolute cross-effect <= 0.75
- Opportunity/Dangerとも6 family中5 family以上が正方向

**PretestがFAILした場合、main generationはrunnerが拒否する。**

---

## 5. Main output and blind evaluation

CharacterはInterpretationだけを生成する。

- Historyなし
- Regulation操作なし
- Responseなし
- Biographyなし

Blind evaluatorにはInterpretation本文とblind IDだけを渡し、以下を0–4で採点する。

1. Opportunity Salience
2. Danger Salience
3. Seeking Activation
4. Negative Activation

condition / family / O-D操作 / hypothesisは評価時に渡さない。

---

## 6. Sample size

Pretest:

`6 families × 4 O/D variants × 1 replicate = 24 API runs`

Main generation:

`6 families × 4 O/D variants × 4 S/N conditions × 2 replicates = 192 runs`

Blind evaluation:

`192 runs`

合計予定: **408 API requests**

Pilotではreplicate数を増やすよりscenario familyの一般化を優先する。

---

## 7. Pilot gates

| Gate | Criterion |
|---|---|
| G1 | Stimulus pretestが全PASS |
| G2 | O-highでS main effect >= 0.75、D-highでN main effect >= 0.75 |
| G3 | Primary interaction mean <= -0.50、かつ6 family中4以上で負 |
| G4 | Leave-one-family-out interactionの最大値 <= -0.25 |

`all_gates_pass=false` でも閾値を事後変更しない。

---

## 8. Local setup

このpilotはPF-EXP-0001と同一のPython依存条件を使う。既存のcommitted lockfileからPF-EXP-0002用lockを決定論的にbootstrapする。

実験ディレクトリへ移動:

```powershell
cd research\experiments\PF-EXP-0002-opportunity-danger-interaction
```

lockfile作成:

```powershell
uv run --no-project python bootstrap_lock.py
```

依存関係同期:

```powershell
uv sync --frozen
```

Static validation:

```powershell
uv run python -m src.validate
```

期待結果:

```text
PASS: PF-EXP-0002 static validation
```

---

## 9. Execution sequence

### 9.1 Stimulus pretest dry-run

```powershell
uv run python -m src.pretest --dry-run
```

期待:

```text
pretest manifest: ... (24 runs)
dry-run: no API requests sent
```

### 9.2 Stimulus pretest

ここからAPI課金対象。

```powershell
uv run python -m src.pretest
```

成功条件:

```text
pretest summary:
  planned:   24
  succeeded: 24
  missing:   0
```

### 9.3 Pretest gate analysis

```powershell
uv run python -m src.pretest_analyze
```

`all_gates_pass: true` の場合のみmainへ進む。

### 9.4 Main generation dry-run

```powershell
uv run python -m src.pilot --dry-run
```

期待:

```text
manifest: ... (192 runs)
dry-run: no API requests sent
```

### 9.5 Main generation

```powershell
uv run python -m src.pilot
```

成功条件:

```text
generation summary:
  planned:   192
  succeeded: 192
  missing:   0
```

### 9.6 Blind set

```powershell
uv run python -m src.blind
```

期待:

```text
blind set: 192 records
```

### 9.7 Evaluation dry-run

```powershell
uv run python -m src.evaluate --dry-run
```

### 9.8 Blind evaluation

```powershell
uv run python -m src.evaluate
```

成功条件:

```text
evaluation summary:
  planned:   192
  succeeded: 192
  missing:   0
```

### 9.9 Analysis

```powershell
uv run python -m src.analyze
```

G1〜G4とfamily別interactionを出力する。

---

## 10. Data / audit policy

- `store=false`
- OpenAI API routingは `https://api.openai.com/v1` を明示
- raw InterpretationはGit管理外
- blind set / blind key / private gate JSON / runtime environmentはGit管理外
- technical failure時はresponse status、incomplete reason、request ID、usageを可能な範囲で監査
- success済みrunはresume時にskip
- 実行時のPython / package versionsは `private/environment.json` に保存
- main解析が終わるまでInterpretation本文を研究者が読まないことを推奨

---

## 11. Confirmatory boundary

このpilotでinteractionが再現しても、直ちにPersonality Formation Modelへ新しい内部変数を追加しない。

次のholdout confirmatory studyで、

- 新規scenario families
- familyを一般化単位とした推定
- interaction threshold / CI
- exclusion / retry rule
- model parameters

を事前固定してから、正本への反映要否を判断する。

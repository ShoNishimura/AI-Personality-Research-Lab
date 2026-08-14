# PF-EXP-0004 pilot-001 summary

> Aggregate audit summary  
> Raw pretest responses remain local/private.

## Outcome

- Static validation: **PASS** (`pretest 16 / generation 48 / evaluation 48`)
- Tests: **7 / 7 passed**
- History pretest: **16 / 16 succeeded**
- Pretest overall gate: **FAIL**
- Passed: **P1, P3, P4**
- Failed: **P2**
- Main generation: **not run**
- Blind evaluation: **not run**

Pre-frozen thresholds were not changed after observing results. Because the pretest failed, the protocol requirement to stop before main generation was followed.

## Research question

> 同一のPerceptionとRelationshipのもとで、類似状況に対する過去のResponse結果の履歴は、現在のResponseを再現可能かつ方向整合的に変えるか。

The confirmatory History → Response hypothesis was **not tested** in pilot-001 because the History manipulation did not pass the pretest.

## Pretest gates

| Gate | Observed | Threshold | Result |
|---|---:|---:|---|
| P1 Outcome separation | 4.0 | >= 2.0 | PASS |
| P2 Directiveness mean | 1.0 | <= 0.5 | FAIL |
| P2 Directiveness max | 2.0 | <= 1.0 | FAIL |
| P3 Trait labeling mean | 0.0 | <= 0.5 | PASS |
| P3 Trait labeling max | 0.0 | <= 1.0 | PASS |
| P4 Family direction | 8/8 families | >= 7/8 | PASS |

Outcome valence separation was 4.0 in every family. Trait labeling was 0 for all 16 stimuli. The only failed manipulation-quality gate was current-response directiveness.

## Directiveness audit

| Family | History | Valence | Directiveness | Outcome valence | Trait labeling |
|---|---|---|---:|---:|---:|
| F01 | H+ | favorable | 2 | 2 | 0 |
| F02 | H- | adverse | 2 | -2 | 0 |
| F05 | H- | adverse | 2 | -2 | 0 |
| F02 | H+ | favorable | 1 | 2 | 0 |
| F08 | H- | adverse | 1 | -2 | 0 |
| F03 | H- | adverse | 1 | -2 | 0 |
| F04 | H+ | favorable | 1 | 2 | 0 |
| F05 | H+ | favorable | 1 | 2 | 0 |
| F08 | H+ | favorable | 1 | 2 | 0 |
| F06 | H+ | favorable | 1 | 2 | 0 |
| F07 | H- | adverse | 1 | -2 | 0 |
| F04 | H- | adverse | 1 | -2 | 0 |
| F06 | H- | adverse | 1 | -2 | 0 |
| F03 | H+ | favorable | 0 | 2 | 0 |
| F01 | H- | adverse | 0 | -2 | 0 |
| F07 | H+ | favorable | 0 | 2 | 0 |

The directiveness scores sum to 16 across 16 stimuli, giving a mean of 1.0. Three stimuli were rated 2, ten were rated 1, and three were rated 0.

## Interpretation boundary

This pretest does **not** show that History has no effect on Response. It shows that the specific pilot-001 operationalization of History — repeated past Response + Outcome episodes — did not satisfy the pre-frozen manipulation-quality requirement for low current-response directiveness.

Therefore:

- Do **not** evaluate G1–G3 from this pilot; no main responses were generated.
- Do **not** claim support or rejection of `History → Response` from pilot-001.
- Retain pilot-001 as a pretest gate-fail record.
- Do **not** loosen the frozen thresholds retroactively to convert this run into a PASS.

## Design issue discovered after the pretest

Post-pretest review identified a conceptual question about the operational meaning of `History`. The pilot-001 stimuli represented History primarily as concrete episodic records of past Response and Outcome. The intended APRL concept may instead require a more abstract representation of what the Character learned or generalized from prior experience.

This is recorded as a **design issue discovered after the pretest**, not as a post-hoc reinterpretation of the observed gate result. Any revised operational definition or canonical model change must be made prospectively and evaluated in a new pretest version.

## Design hashes at pilot-001 pretest

The successful pretest analysis recorded the following frozen design hashes:

- `experiment.yaml`: `153da10fa7184ab4d0ce615e42b9a0e995e321cddad616fae525257d38d554fc`
- `stimuli.yaml`: `fe11a49a3f6947422dc49c21a660ed888b66d59b249a7053d3112a56a8c920ad`
- `thresholds.yaml`: `06e9f40602c81c1f9b6d3db4ee03bbeacf270449d08c0f8087c5731004edb0d1`
- `output.schema.json`: `b179b90974aea655e3991d48f072cb295a7eedbc9d0d2824e488c3f3a6b67699`
- `evaluation.schema.json`: `e1874edec3850f2ff15786ecdeb6bd7eb1e2ad1705ca9856856e458ad47ce894`
- `pretest.schema.json`: `2c4b4f1b3e33f9698e73fe0aa82fc104de225c6399a9950d1f33c53fac2a8d80`
- `prompts/system.md`: `a4344c1cbf01069a3bcdc707cbd35ee73adc668aff0983c3ef2b6a68529c4cd4`
- `prompts/task.md`: `f0b74aa65743457f6e42d303bdbc29fcc56b9e2b3e0d4967f90d3c491731a7f9`
- `prompts/evaluator-system.md`: `1a71f5a0ca03d3ed653cc715a002b8d9520f7c57339805a8a858077f044a586b`
- `prompts/evaluator-task.md`: `40bf21c4bf52e6d2b4211e822463ba20ebe80dddddb9bda4dd72d7f1b055b6bb`
- `prompts/pretest-system.md`: `c9337fac4d02a2eadb77913b6fa1eb9bf951c36cbf626ef4fdc1b1a6f3c206a1`
- `prompts/pretest-task.md`: `ad48ca30625a22d8d408ccba97a53fc2343f5a0ec0d91b161686b4dfa8d2acdd`

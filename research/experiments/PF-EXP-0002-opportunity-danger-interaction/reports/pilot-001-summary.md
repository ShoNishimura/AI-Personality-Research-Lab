# PF-EXP-0002 pilot-001 summary

> Aggregate audit summary  
> Raw Interpretation remains local/private.

## Outcome

- Stimulus pretest: **24 / 24 succeeded; all pretest gates passed**
- Main generation: **192 / 192 succeeded**
- Blind evaluation: **192 / 192 succeeded**
- Overall gate: **FAIL**
- Passed: G1, G2
- Failed: G3, G4

The pre-frozen thresholds are not changed after observing results.

## Pretest

| Measure | Observed | Threshold | Result |
|---|---:|---:|---|
| Opportunity main effect | 2.000 | >= 1.50 | PASS |
| Danger main effect | 2.167 | >= 1.50 | PASS |
| Opportunity→Danger cross contamination | 0.167 | <= 0.75 | PASS |
| Danger→Opportunity cross contamination | 0.000 | <= 0.75 | PASS |
| Family direction | 6/6 each | >= 5/6 | PASS |

The stimulus manipulation therefore separated Opportunity Value and Danger Value sufficiently for the main pilot.

## Main effects and frozen gates

| Gate | Result | Key observation |
|---|---|---|
| G1 Pretest | PASS | All stimulus pretest gates passed |
| G2 Temperament replication | PASS | Seeking main = 1.271; Negative main = 1.021; both >= 0.75 |
| G3 Target interaction | FAIL | Primary interaction = **+0.250**, while hypothesis required <= -0.50; 0/6 families were negative |
| G4 Generalization | FAIL | Leave-one-family-out means = +0.20 to +0.30, while threshold required <= -0.25 |

The original hypothesis was:

> Increasing Opportunity Value would reduce Danger Salience more strongly under High Seeking Reactivity.

That directional hypothesis was **not supported**. The observed mean interaction had the opposite sign.

## Family-level target interaction

Primary interaction per family:

| Family | C |
|---|---:|
| F01 | +0.50 |
| F02 | 0.00 |
| F03 | 0.00 |
| F04 | +0.50 |
| F05 | +0.50 |
| F06 | 0.00 |

No family showed the hypothesized negative interaction.

Leave-one-family-out mean interactions remained positive in every case: **+0.20 to +0.30**.

## Post-gate descriptive analysis

After the frozen gate analysis, the N=High / Danger=High cells were summarized without reading raw Interpretation text.

| Condition | Opportunity | n | Opportunity Salience | Danger Salience | Seeking Activation | Negative Activation | Joint Salience | Concurrent Rate |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| T01 Low S / High N | Low | 12 | 0.917 | 3.250 | 0.083 | 2.667 | 0.917 | 0.083 |
| T01 Low S / High N | High | 12 | 2.333 | 3.083 | 0.250 | 2.417 | 2.333 | 1.000 |
| T11 High S / High N | Low | 12 | 2.083 | 2.750 | 1.417 | 2.167 | 2.083 | 1.000 |
| T11 High S / High N | High | 12 | 3.000 | 2.833 | 1.833 | 2.250 | 2.833 | 1.000 |

Opportunity High − Low:

| Condition | Opportunity Salience | Danger Salience | Seeking Activation | Negative Activation |
|---|---:|---:|---:|---:|
| T01 | +1.417 | -0.167 | +0.167 | -0.250 |
| T11 | +0.917 | +0.083 | +0.417 | +0.083 |

Interaction contrast `T11 delta - T01 delta`:

- Opportunity Salience: **-0.500**
- Danger Salience: **+0.250**
- Seeking Activation: **+0.250**
- Negative Activation: **+0.333**

## Interpretation boundary

The post-gate pattern is **exploratory only**. It does not establish a general Concurrent Salience mechanism.

The descriptive result motivates a new independent pilot:

> [PF-EXP-0003 — Concurrent Salience](../../PF-EXP-0003-concurrent-salience/)

PF-EXP-0003 will test whether High Seeking Reactivity allows Opportunity Salience to increase while preserving Danger Salience, using new scenario families and pre-frozen gates.

## Technical audit note

Blind evaluation was interrupted after 168 successful evaluations because the API credit balance was exhausted (`insufficient_quota / credit_balance_exhausted`). After credits were replenished, the same runner resumed by skipping already-successful blind IDs and completed **192 / 192** evaluations without changing research conditions.

This interruption is treated as a technical execution event, not a research-condition change.

# PF-EXP-0003 — Concurrent Salience

> Personality Formation Model v1.0  
> Status: **planned / hypothesis and pilot gates frozen before responses**

## 30-second summary

PF-EXP-0002 did **not** support the hypothesis that Opportunity attenuates Danger more strongly under High Seeking Reactivity. Its post-gate descriptive analysis instead showed an exploratory pattern in which High S increased Opportunity Salience while Danger Salience was preserved.

PF-EXP-0003 independently tests:

> **When Opportunity and Danger are simultaneously present, does High Seeking Reactivity increase Opportunity Salience while preserving Danger Salience?**

This does not change the canonical Personality Formation Model. It tests a possible property of the existing function:

`I_t = f(E_t, T_0, H_t)`

---

## 1. Hypothesis

Primary hypothesis **H-CS01 — Concurrent Salience**:

> Under High N and High Danger, increasing Opportunity Value will reduce Danger Salience less under High S than under Low S, while Opportunity Salience remains responsive to the Opportunity manipulation.

Define:

`ΔD_T01 = Danger(T01, O-high) - Danger(T01, O-low)`

`ΔD_T11 = Danger(T11, O-high) - Danger(T11, O-low)`

Primary interaction:

`C_D = ΔD_T11 - ΔD_T01`

Hypothesized direction:

`C_D > 0`

The hypothesis is not that High S increases Danger. The hypothesis is that High S allows Opportunity to become salient **without a corresponding loss of Danger Salience**.

---

## 2. Minimal design

Fix:

- N = High
- Danger Value = High

Manipulate only:

- S: Low / High
- Opportunity Value: Low / High

2 × 2 design:

| Cell | S | N | Opportunity | Danger |
|---|---|---|---|---|
| C1 | Low | High | Low | High |
| C2 | Low | High | High | High |
| C3 | High | High | Low | High |
| C4 | High | High | High | High |

This deliberately removes cells that are not required for the Concurrent Salience question.

---

## 3. Stimuli

Use **8 new scenario families**.

No PF-EXP-0001 or PF-EXP-0002 stimulus text is reused.

Each family has two versions:

- Opportunity Low / Danger High
- Opportunity High / Danger High

The Danger wording must remain identical within each family. Only the Opportunity-relevant information may differ.

Candidate family domains:

1. unknown communication channel
2. unverified information source
3. new collaborator-provided resource
4. untested analysis method
5. alternative transport or access path
6. unfamiliar high-value tool
7. novel data-processing shortcut
8. potentially useful external service

Final wording will be frozen before API responses.

---

## 4. Stimulus pretest

Pretest the 16 stimuli without Temperament.

`8 families × 2 Opportunity levels × 1 replicate = 16 API runs`

Blind evaluator measures:

- Opportunity Value: 0–4
- Danger Value: 0–4

Pretest gates:

- Opportunity High − Low mean >= **1.50**
- absolute Danger difference caused by Opportunity manipulation <= **0.50**
- at least **7 / 8 families** show Opportunity High > Low

Main generation must not start if pretest fails.

---

## 5. Main sample size

Use 3 replicates to reduce the influence of a single ordinal-score fluctuation.

`8 families × 4 cells × 3 replicates = 96 generation runs`

Blind evaluation:

`96 runs`

Total planned API requests:

`16 pretest + 96 generation + 96 evaluation = 208`

---

## 6. Character output

As in PF-EXP-0001 / 0002, Character generates **Interpretation only**.

Excluded:

- History / Biography
- Regulation manipulation
- Response
- Relationship

This keeps the experiment focused on `Temperament × Experience → Interpretation`.

---

## 7. Blind evaluation

Blind evaluator receives Interpretation text only and scores 0–4:

1. Opportunity Salience
2. Danger Salience
3. Seeking Activation
4. Negative Activation

Primary outcome: **Danger Salience**.

Opportunity Salience is required to verify that the Opportunity manipulation still changes Interpretation under High S.

Seeking / Negative Activation are secondary replication measures.

---

## 8. Frozen pilot gates

These gates are fixed before PF-EXP-0003 responses are observed.

### G1 — Stimulus validity

All pretest gates pass.

### G2 — S manipulation and Opportunity uptake

- High S − Low S mean Seeking Activation >= **0.75** across the four cells
- within T11, Opportunity Salience O-high − O-low >= **0.50**

### G3 — Danger preservation

Both must hold:

- within T11, `ΔD_T11 >= -0.25`
- primary interaction `C_D >= +0.20`

The first criterion prevents a positive interaction from being counted as support if Danger still declines substantially under High S.

### G4 — Family generalization

- at least **5 / 8 families** have `C_D > 0`
- every leave-one-family-out mean `C_D` remains **> 0**

### G5 — Concurrent Salience state

For T11 / Opportunity High / Danger High:

- mean Opportunity Salience >= **2.50**
- mean Danger Salience >= **2.50**
- proportion of runs with both Opportunity Salience >=2 and Danger Salience >=2 >= **0.75**

`all_gates_pass=false` does not permit post-hoc threshold changes.

---

## 9. Secondary measures

Define:

`Joint Salience = min(Opportunity Salience, Danger Salience)`

and:

`Concurrent Salience Rate = P(Opportunity Salience >= 2 AND Danger Salience >= 2)`

These are descriptive / secondary measures except for the T11/O-high rate criterion in G5.

Negative Activation preservation and Opportunity/Seeking interaction contrasts are recorded as exploratory.

---

## 10. Interpretation of outcomes

### A. Gates pass

Supports the pilot hypothesis that High S can increase Opportunity-related Interpretation while preserving Danger-related Interpretation across multiple new Experiences.

This would motivate a holdout confirmatory study. It would **not** yet justify adding a new internal variable such as Attention or Salience Competition to the canonical model.

### B. `C_D ≈ 0`

Supports a simpler independent-coexistence interpretation: S and N may act largely independently on Interpretation without systematic attenuation or preservation interaction.

### C. `C_D < 0`

The PF-EXP-0002 positive interaction was likely unstable or stimulus-dependent; Concurrent Salience is not supported.

---

## 11. Confirmatory boundary

Only after this pilot is completed should a confirmatory study be designed.

Confirmatory requirements:

- holdout scenario families
- no reuse of PF-EXP-0001/0002/0003 pilot stimuli
- family as the generalization unit
- interaction threshold and uncertainty interval fixed in advance
- model parameters / retry / exclusion policy fixed before responses

The canonical Personality Formation Model remains unchanged until evidence warrants revision.

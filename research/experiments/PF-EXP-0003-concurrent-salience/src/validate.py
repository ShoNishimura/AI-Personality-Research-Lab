from __future__ import annotations

from collections import Counter

from .common import ROOT, load_yaml, sha256_normalized_text_file


def main() -> int:
    config = load_yaml(ROOT / "experiment.yaml")
    conditions = load_yaml(ROOT / "conditions.yaml")["conditions"]
    stimuli = load_yaml(ROOT / "stimuli.yaml")["stimuli"]
    thresholds = load_yaml(ROOT / "thresholds.yaml")
    status = load_yaml(ROOT / config["status_path"])
    errors: list[str] = []

    if config["experiment_id"] != "PF-EXP-0003":
        errors.append("experiment_id must be PF-EXP-0003")
    if int(config["replicates"]) != 3 or int(config["pretest_replicates"]) != 1:
        errors.append("replicates must be 3 and pretest_replicates 1")
    if {c["id"] for c in conditions} != {"T01", "T11"}:
        errors.append("conditions must be exactly T01 and T11")
    if any(c["negative_affectivity"] != "high" for c in conditions):
        errors.append("N must be fixed High")

    if len(stimuli) != 16:
        errors.append(f"expected 16 stimuli; got {len(stimuli)}")
    families = Counter(s["family_id"] for s in stimuli)
    if len(families) != 8 or any(count != 2 for count in families.values()):
        errors.append("expected 8 families with exactly 2 variants each")
    if any(s["danger"] != "high" for s in stimuli):
        errors.append("Danger must be fixed High")

    for family in sorted(families):
        pair = [s for s in stimuli if s["family_id"] == family]
        if {s["opportunity"] for s in pair} != {"low", "high"}:
            errors.append(f"{family}: Opportunity variants must be low/high")
        if len({s["context_clause"] for s in pair}) != 1:
            errors.append(f"{family}: context_clause differs")
        if len({s["danger_clause"] for s in pair}) != 1:
            errors.append(f"{family}: danger_clause differs")
        for s in pair:
            expected_text = f'{s["context_clause"]} {s["opportunity_clause"]} {s["danger_clause"]}'
            if s["text"] != expected_text:
                errors.append(f'{s["id"]}: text does not match frozen clauses')

    p = thresholds["pretest"]
    q = thresholds["pilot"]
    expected = {
        "pre_min_opp": (p["min_opportunity_main_effect"], 1.50),
        "pre_max_cross": (p["max_opportunity_to_danger_cross_abs"], 0.50),
        "pre_family": (p["min_families_opportunity_correct_direction"], 7),
        "g2_seek": (q["min_seeking_main_effect"], 0.75),
        "g2_opp": (q["min_t11_opportunity_uptake"], 0.50),
        "g3_danger": (q["min_t11_danger_delta"], -0.25),
        "g3_interaction": (q["min_primary_danger_interaction"], 0.20),
        "g4_family": (q["min_positive_family_interactions"], 5),
        "g4_loo": (q["min_leave_one_family_out_interaction_exclusive"], 0.0),
        "g5_opp": (q["min_t11_o_high_opportunity_salience"], 2.50),
        "g5_danger": (q["min_t11_o_high_danger_salience"], 2.50),
        "g5_rate": (q["min_t11_o_high_concurrent_rate"], 0.75),
        "joint_cut": (q["concurrent_min_score_each"], 2),
    }
    for name, (actual, wanted) in expected.items():
        if float(actual) != float(wanted):
            errors.append(f"{name}: expected {wanted}, got {actual}")

    for key, filename in (("thresholds_sha256", "thresholds.yaml"), ("stimuli_sha256", "stimuli.yaml")):
        if key in status and status[key] != sha256_normalized_text_file(ROOT / filename):
            errors.append(f"status {key} does not match {filename}")

    required = [
        "src/pretest.py", "src/pretest_analyze.py", "src/blind.py", "src/evaluate.py",
        "src/analyze.py", "tests/test_design.py", "tests/test_analysis.py",
    ]
    for rel in required:
        if not (ROOT / rel).exists():
            errors.append(f"missing required file: {rel}")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: PF-EXP-0003 static validation")
    print("  pretest: 16 / generation: 96 / evaluation: 96")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

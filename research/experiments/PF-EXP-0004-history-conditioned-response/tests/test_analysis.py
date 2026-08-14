from src.analyze import analyze_rows
from src.common import ROOT, load_yaml
from src.pretest_analyze import analyze_rows as analyze_pretest_rows


def _main_rows() -> list[dict]:
    rows = []
    for family_index in range(1, 9):
        family = f"F{family_index:02d}"
        for history_id, approach in (("H+", 3), ("H-", 1)):
            for replicate in range(1, 4):
                rows.append(
                    {
                        "family_id": family,
                        "history_id": history_id,
                        "replicate_id": f"R{replicate:03d}",
                        "approach_commitment": approach,
                        "caution_information_seeking": 2,
                        "response_intensity": 2,
                        "response_latency": 1,
                        "action_category": "limited_trial" if history_id == "H+" else "information_seek",
                    }
                )
    return rows


def test_main_gates_pass_for_clear_history_effect() -> None:
    thresholds = load_yaml(ROOT / "thresholds.yaml")["pilot"]
    result = analyze_rows(_main_rows(), thresholds)
    assert result["primary_approach_effect"] == 2
    assert result["positive_family_count"] == 8
    assert min(result["leave_one_family_out"].values()) == 2
    assert result["all_gates_pass"] is True


def test_pretest_gates_pass_for_clean_manipulation() -> None:
    rows = []
    for family_index in range(1, 9):
        family = f"F{family_index:02d}"
        rows.extend(
            [
                {
                    "family_id": family,
                    "history_id": "H+",
                    "outcome_valence": 2,
                    "current_response_directiveness": 0,
                    "trait_labeling": 0,
                },
                {
                    "family_id": family,
                    "history_id": "H-",
                    "outcome_valence": -2,
                    "current_response_directiveness": 0,
                    "trait_labeling": 0,
                },
            ]
        )
    thresholds = load_yaml(ROOT / "thresholds.yaml")["pretest"]
    result = analyze_pretest_rows(rows, thresholds)
    assert result["outcome_valence_separation"] == 4
    assert result["all_gates_pass"] is True

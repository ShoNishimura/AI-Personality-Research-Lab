from src.common import ROOT, load_yaml


def test_frozen_thresholds_match_plan():
    t = load_yaml(ROOT / "thresholds.yaml")
    assert t["pretest"]["min_opportunity_main_effect"] == 1.5
    assert t["pretest"]["max_opportunity_to_danger_cross_abs"] == 0.5
    assert t["pretest"]["min_families_opportunity_correct_direction"] == 7
    p = t["pilot"]
    assert p["min_seeking_main_effect"] == 0.75
    assert p["min_t11_opportunity_uptake"] == 0.5
    assert p["min_t11_danger_delta"] == -0.25
    assert p["min_primary_danger_interaction"] == 0.2
    assert p["min_positive_family_interactions"] == 5
    assert p["min_leave_one_family_out_interaction_exclusive"] == 0.0
    assert p["min_t11_o_high_opportunity_salience"] == 2.5
    assert p["min_t11_o_high_danger_salience"] == 2.5
    assert p["min_t11_o_high_concurrent_rate"] == 0.75
    assert p["concurrent_min_score_each"] == 2

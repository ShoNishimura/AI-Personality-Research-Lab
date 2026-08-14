from src.common import render_evaluator_prompts, render_generation_prompts, render_pretest_prompts, stimuli_for_split


def test_generation_prompt_has_no_temperament_or_condition_label() -> None:
    stimulus = stimuli_for_split("pilot")[0]
    for history_id in ("H+", "H-"):
        system, user = render_generation_prompts(stimulus, history_id)
        text = system + "\n" + user
        for forbidden in ("Temperament", "Seeking Reactivity", "Negative Affectivity", "T0", "H+", "H-"):
            assert forbidden not in text


def test_pretest_does_not_expose_condition_label() -> None:
    stimulus = stimuli_for_split("pilot")[0]
    for history_id in ("H+", "H-"):
        _, user = render_pretest_prompts(stimulus, history_id)
        assert "H+" not in user
        assert "H-" not in user


def test_evaluator_is_history_blind() -> None:
    stimulus = stimuli_for_split("pilot")[0]
    _, user = render_evaluator_prompts(
        {
            "current_experience": stimulus["current_experience"],
            "perception": stimulus["perception"],
            "response": {"action": "限定範囲で試す。", "intensity": 2, "latency": 1},
        }
    )
    assert "Past History" not in user
    assert "H+" not in user
    assert "H-" not in user

from src.common import ROOT


def test_evaluator_explicitly_allows_concurrent_salience():
    text = (ROOT / "prompts/evaluator-system.md").read_text(encoding="utf-8")
    assert "同時に高く" in text
    assert "接近" not in text or "推測" in text

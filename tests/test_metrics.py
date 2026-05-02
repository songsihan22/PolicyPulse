from src.metrics import (
    compute_communication_effect,
    compute_final_metrics,
    compute_polarization_index,
    compute_round_metrics,
)
from src.models import SimulationConfig
from src.simulator import run_simulation


def _sample_df():
    config = SimulationConfig(
        scenario_name="生成式 AI 进入高校课堂",
        num_agents=30,
        num_rounds=6,
        intervention="平衡型公共讨论",
        random_seed=21,
    )
    return run_simulation(config)


def test_stance_ratios_sum_to_one():
    df = _sample_df()
    round_metrics = compute_round_metrics(df)
    ratio_sum = (
        round_metrics["support_rate"]
        + round_metrics["neutral_rate"]
        + round_metrics["oppose_rate"]
    )
    assert ratio_sum.round(6).eq(1.0).all()


def test_metrics_are_computed_for_final_round():
    df = _sample_df()
    final_metrics = compute_final_metrics(df)
    assert "final_support_rate" in final_metrics
    assert "persona_gap" in final_metrics
    assert 0.0 <= final_metrics["final_support_rate"] <= 1.0
    assert final_metrics["persona_gap"] >= 0.0


def test_communication_effect_has_expected_keys():
    df = _sample_df()
    effect = compute_communication_effect(df)
    assert {
        "mean_attitude_delta",
        "support_rate_delta",
        "neutral_rate_delta",
        "oppose_rate_delta",
        "effect_label",
    }.issubset(effect.keys())


def test_polarization_index_has_expected_keys():
    df = _sample_df()
    polarization = compute_polarization_index(df)
    assert {"individual_polarization", "persona_gap"}.issubset(polarization.keys())

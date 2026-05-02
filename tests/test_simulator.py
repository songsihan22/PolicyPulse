import pandas as pd

from src.models import SimulationConfig
from src.simulator import run_simulation


def test_run_simulation_returns_non_empty_dataframe():
    config = SimulationConfig(
        scenario_name="生成式 AI 进入高校课堂",
        num_agents=30,
        num_rounds=6,
        intervention="平衡型公共讨论",
        random_seed=7,
    )

    df = run_simulation(config)

    assert not df.empty
    assert {"round", "agent_id", "persona_type", "attitude", "institutional_trust", "risk_sensitivity", "conformity"}.issubset(df.columns)
    assert df["round"].max() == 6


def test_run_simulation_row_count():
    config = SimulationConfig(
        scenario_name="生成式 AI 进入高校课堂",
        num_agents=24,
        num_rounds=5,
        intervention="平衡型公共讨论",
        random_seed=11,
    )
    df = run_simulation(config)
    assert len(df) == 24 * 6


def test_simulation_is_reproducible_with_fixed_seed():
    config = SimulationConfig(
        scenario_name="生成式 AI 内容监管",
        num_agents=20,
        num_rounds=4,
        intervention="专家理性说明",
        random_seed=99,
    )
    df_one = run_simulation(config)
    df_two = run_simulation(config)
    pd.testing.assert_frame_equal(df_one, df_two)

"""Plotly chart builders for the simulation results."""

from __future__ import annotations

import pandas as pd
import plotly.express as px

from src.metrics import compute_round_metrics


def plot_average_attitude(df: pd.DataFrame):
    """Plot mean attitude by round."""
    chart_df = compute_round_metrics(df)
    fig = px.line(
        chart_df,
        x="round",
        y="average_attitude",
        markers=True,
        title="群体平均态度演化趋势",
        labels={"round": "轮次", "average_attitude": "平均态度"},
    )
    fig.update_layout(yaxis_range=[-1, 1], template="plotly_white")
    return fig


def plot_group_distribution(df: pd.DataFrame):
    """Plot support/neutral/oppose ratio by round."""
    chart_df = compute_round_metrics(df).melt(
        id_vars="round",
        value_vars=["support_rate", "neutral_rate", "oppose_rate"],
        var_name="stance_key",
        value_name="ratio",
    )
    chart_df["stance"] = chart_df["stance_key"].map(
        {
            "support_rate": "支持",
            "neutral_rate": "中立",
            "oppose_rate": "反对",
        }
    )
    fig = px.area(
        chart_df,
        x="round",
        y="ratio",
        color="stance",
        title="支持、中立与反对立场的比例变化",
        labels={"round": "轮次", "ratio": "比例", "stance": "态度分类"},
        category_orders={"stance": ["支持", "中立", "反对"]},
    )
    fig.update_layout(yaxis_tickformat=".0%", template="plotly_white")
    return fig


def plot_persona_attitude(df: pd.DataFrame):
    """Plot mean attitude by persona type over time."""
    chart_df = df.groupby(["round", "persona_type"], as_index=False)["attitude"].mean()
    fig = px.line(
        chart_df,
        x="round",
        y="attitude",
        color="persona_type",
        markers=True,
        title="不同 Agent 类型的平均态度演化",
        labels={"round": "轮次", "attitude": "平均态度", "persona_type": "Agent 类型"},
    )
    fig.update_layout(yaxis_range=[-1, 1], template="plotly_white", legend_title_text="Agent 类型")
    return fig


def plot_polarization_trend(df: pd.DataFrame):
    """Plot attitude dispersion and persona gap by round."""
    chart_df = compute_round_metrics(df).melt(
        id_vars="round",
        value_vars=["attitude_std", "persona_gap"],
        var_name="metric",
        value_name="value",
    )
    chart_df["metric"] = chart_df["metric"].map(
        {
            "attitude_std": "个体态度离散度",
            "persona_gap": "群体分化差距",
        }
    )
    fig = px.line(
        chart_df,
        x="round",
        y="value",
        color="metric",
        markers=True,
        title="群体分化程度变化",
        labels={"round": "轮次", "value": "指标值", "metric": "分化指标"},
    )
    fig.update_layout(template="plotly_white", legend_title_text="分化指标")
    return fig

"""Centralized metric computations for simulation outputs."""

from __future__ import annotations

import pandas as pd


STANCE_ORDER = ["支持", "中立", "反对"]


def compute_round_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Return round-level support, neutral, oppose, attitude, and polarization metrics."""
    counts = (
        df.groupby(["round", "stance"], observed=False)
        .size()
        .unstack(fill_value=0)
        .reindex(columns=STANCE_ORDER, fill_value=0)
    )
    totals = counts.sum(axis=1).replace(0, 1)

    attitude_summary = df.groupby("round", as_index=True)["attitude"].agg(
        average_attitude="mean",
        attitude_std="std",
    )
    attitude_summary["attitude_std"] = attitude_summary["attitude_std"].fillna(0.0)

    persona_means = (
        df.groupby(["round", "persona_type"], observed=False)["attitude"]
        .mean()
        .unstack(fill_value=0)
    )
    persona_gap = persona_means.max(axis=1) - persona_means.min(axis=1)

    return pd.DataFrame(
        {
            "round": counts.index,
            "support_rate": counts["支持"] / totals,
            "neutral_rate": counts["中立"] / totals,
            "oppose_rate": counts["反对"] / totals,
            "average_attitude": attitude_summary["average_attitude"],
            "attitude_std": attitude_summary["attitude_std"],
            "persona_gap": persona_gap,
        }
    ).reset_index(drop=True)


def compute_polarization_index(df: pd.DataFrame) -> dict[str, float]:
    """Return final-round individual and persona-level polarization indicators."""
    round_metrics = compute_round_metrics(df)
    final_metrics = round_metrics.iloc[-1]
    return {
        "individual_polarization": float(final_metrics["attitude_std"]),
        "persona_gap": float(final_metrics["persona_gap"]),
    }


def compute_communication_effect(df: pd.DataFrame) -> dict[str, float | str]:
    """Compare initial and final rounds and return communication effect indicators."""
    round_metrics = compute_round_metrics(df)
    initial = round_metrics.iloc[0]
    final = round_metrics.iloc[-1]
    mean_attitude_delta = float(final["average_attitude"] - initial["average_attitude"])

    if mean_attitude_delta > 0.05:
        effect_label = "改善"
    elif mean_attitude_delta < -0.05:
        effect_label = "恶化"
    else:
        effect_label = "基本稳定"

    return {
        "mean_attitude_delta": mean_attitude_delta,
        "support_rate_delta": float(final["support_rate"] - initial["support_rate"]),
        "neutral_rate_delta": float(final["neutral_rate"] - initial["neutral_rate"]),
        "oppose_rate_delta": float(final["oppose_rate"] - initial["oppose_rate"]),
        "effect_label": effect_label,
    }


def compute_final_metrics(df: pd.DataFrame) -> dict[str, float | str]:
    """Return final-round summary metrics."""
    round_metrics = compute_round_metrics(df)
    final = round_metrics.iloc[-1]
    polarization = compute_polarization_index(df)
    communication_effect = compute_communication_effect(df)
    return {
        "final_support_rate": float(final["support_rate"]),
        "final_neutral_rate": float(final["neutral_rate"]),
        "final_oppose_rate": float(final["oppose_rate"]),
        "final_average_attitude": float(final["average_attitude"]),
        "individual_polarization": float(polarization["individual_polarization"]),
        "persona_gap": float(polarization["persona_gap"]),
        "communication_effect_delta": float(communication_effect["mean_attitude_delta"]),
        "communication_effect_label": str(communication_effect["effect_label"]),
    }

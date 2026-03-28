from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd


DEFAULT_FUNNEL = ["visit", "signup", "add_to_cart", "begin_checkout", "purchase"]


@dataclass(frozen=True)
class FunnelResult:
    metrics: pd.DataFrame
    users_by_step: pd.Series



def _first_step_per_user(events: pd.DataFrame, step: str) -> pd.DataFrame:
    step_events = events.loc[events["event_name"] == step, ["user_id", "event_timestamp"]]
    return step_events.groupby("user_id", as_index=False).event_timestamp.min()



def calculate_funnel(events: pd.DataFrame, funnel_steps: Iterable[str] = DEFAULT_FUNNEL) -> FunnelResult:
    """Calculate user-level conversion and drop-off through ordered funnel steps."""
    if events.empty:
        return FunnelResult(
            metrics=pd.DataFrame(columns=["step", "users", "step_conversion", "dropoff_rate"]),
            users_by_step=pd.Series(dtype="int64"),
        )

    steps = list(funnel_steps)
    base_users = events.loc[events["event_name"] == steps[0], "user_id"].nunique()

    users_by_step = []
    eligible_users: pd.Series | None = None

    for step in steps:
        first_hits = _first_step_per_user(events, step)

        if eligible_users is not None:
            first_hits = first_hits[first_hits["user_id"].isin(eligible_users)]

        current_users = first_hits["user_id"].nunique()
        users_by_step.append(current_users)
        eligible_users = first_hits["user_id"]

    funnel_df = pd.DataFrame({"step": steps, "users": users_by_step})
    funnel_df["step_conversion"] = funnel_df["users"] / funnel_df["users"].shift(1)
    funnel_df.loc[0, "step_conversion"] = funnel_df.loc[0, "users"] / max(base_users, 1)
    funnel_df["dropoff_rate"] = 1 - funnel_df["step_conversion"]

    return FunnelResult(metrics=funnel_df, users_by_step=funnel_df.set_index("step")["users"])



def calculate_segmented_funnel(
    events: pd.DataFrame,
    segment_col: str,
    funnel_steps: Iterable[str] = DEFAULT_FUNNEL,
) -> pd.DataFrame:
    """Compute funnel metrics per segment value."""
    outputs = []

    for segment_value, frame in events.groupby(segment_col, dropna=False):
        result = calculate_funnel(frame, funnel_steps=funnel_steps).metrics.copy()
        result[segment_col] = segment_value
        outputs.append(result)

    if not outputs:
        return pd.DataFrame(columns=["step", "users", "step_conversion", "dropoff_rate", segment_col])

    return pd.concat(outputs, ignore_index=True)

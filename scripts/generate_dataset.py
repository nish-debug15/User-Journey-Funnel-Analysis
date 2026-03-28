from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


FUNNEL = ["visit", "signup", "add_to_cart", "begin_checkout", "purchase"]


DEFAULT_N_USERS = 8000


def _probabilities(device: str, traffic_source: str) -> list[float]:
    base = np.array([0.75, 0.58, 0.71, 0.82])

    if device == "mobile":
        base += np.array([-0.08, -0.05, -0.12, -0.16])
    elif device == "tablet":
        base += np.array([-0.03, -0.02, -0.05, -0.07])

    if traffic_source == "paid_social":
        base += np.array([-0.05, -0.03, -0.06, -0.08])
    elif traffic_source == "organic_search":
        base += np.array([0.03, 0.03, 0.04, 0.03])

    return np.clip(base, 0.05, 0.95).tolist()


def generate_events(n_users: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    devices = np.array(["desktop", "mobile", "tablet"])
    sources = np.array(["organic_search", "paid_social", "direct", "email"])
    locations = np.array(["IN", "US", "AE", "SG", "UK"])

    records = []
    start = pd.Timestamp("2025-01-01")

    for user_id in range(1, n_users + 1):
        device = rng.choice(devices, p=[0.35, 0.55, 0.10])
        source = rng.choice(sources, p=[0.30, 0.28, 0.22, 0.20])
        location = rng.choice(locations, p=[0.40, 0.20, 0.10, 0.15, 0.15])

        probs = _probabilities(device, source)
        event_time = start + pd.to_timedelta(int(rng.integers(0, 365 * 24 * 60)), unit="m")

        session_events = [FUNNEL[0]]
        for idx, p in enumerate(probs, start=1):
            if rng.random() < p:
                session_events.append(FUNNEL[idx])
            else:
                break

        cart_value = float(np.round(max(10, rng.normal(75, 20)), 2))
        discount_pct = float(np.clip(rng.normal(10, 6), 0, 35))
        page_load_seconds = float(np.round(np.clip(rng.normal(2.8, 1.1), 0.8, 9.0), 2))

        for order, event in enumerate(session_events):
            timestamp = event_time + pd.to_timedelta(order * int(rng.integers(1, 25)), unit="m")
            records.append(
                {
                    "user_id": user_id,
                    "event_name": event,
                    "event_timestamp": timestamp,
                    "device_type": device,
                    "traffic_source": source,
                    "location": location,
                    "cart_value": cart_value,
                    "discount_pct": discount_pct,
                    "page_load_seconds": page_load_seconds,
                }
            )

    events = pd.DataFrame.from_records(records).sort_values(["event_timestamp", "user_id"]).reset_index(drop=True)
    return events


def generate_training_frame(events: pd.DataFrame) -> pd.DataFrame:
    user_frame = (
        events.sort_values("event_timestamp")
        .groupby("user_id", as_index=False)
        .agg(
            device_type=("device_type", "first"),
            traffic_source=("traffic_source", "first"),
            location=("location", "first"),
            cart_value=("cart_value", "first"),
            discount_pct=("discount_pct", "first"),
            page_load_seconds=("page_load_seconds", "first"),
            max_stage=("event_name", "last"),
        )
    )

    user_frame["is_purchase"] = (user_frame["max_stage"] == "purchase").astype(int)
    return user_frame.drop(columns=["max_stage"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic user journey events.")
    parser.add_argument("--n-users", type=int, default=DEFAULT_N_USERS)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--events-out", type=Path, default=Path("data/events.csv"))
    parser.add_argument("--train-out", type=Path, default=Path("data/train.csv"))
    args = parser.parse_args()

    args.events_out.parent.mkdir(parents=True, exist_ok=True)
    args.train_out.parent.mkdir(parents=True, exist_ok=True)

    events = generate_events(args.n_users, args.seed)
    train_df = generate_training_frame(events)

    events.to_csv(args.events_out, index=False)
    train_df.to_csv(args.train_out, index=False)

    print(f"Saved {len(events):,} event rows to {args.events_out}")
    print(f"Saved {len(train_df):,} training rows to {args.train_out}")


if __name__ == "__main__":
    main()

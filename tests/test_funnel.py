import pandas as pd

from src.analytics.funnel import calculate_funnel


def test_funnel_metrics_basic():
    events = pd.DataFrame(
        {
            "user_id": [1, 1, 2, 2, 2, 3],
            "event_name": ["visit", "signup", "visit", "signup", "purchase", "visit"],
            "event_timestamp": pd.to_datetime(
                [
                    "2025-01-01 10:00",
                    "2025-01-01 10:01",
                    "2025-01-01 11:00",
                    "2025-01-01 11:01",
                    "2025-01-01 11:10",
                    "2025-01-01 12:00",
                ]
            ),
        }
    )

    result = calculate_funnel(events, funnel_steps=["visit", "signup", "purchase"]).metrics
    assert list(result["users"]) == [3, 2, 1]

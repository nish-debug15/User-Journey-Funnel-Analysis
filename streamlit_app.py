from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
import plotly.express as px
import streamlit as st

from src.analytics.funnel import calculate_funnel, calculate_segmented_funnel

st.set_page_config(page_title="User Journey Funnel + ML", page_icon="📉", layout="wide")

st.title("User Journey Funnel Analysis + Conversion Modeling")
st.caption("End-to-end analytics project: funnel diagnostics, segmentation, and advanced ML scoring.")

DATA_EVENTS = Path("data/events.csv")
MODEL_PATH = Path("models/best_model.joblib")
METRICS_PATH = Path("models/metrics.json")

if not DATA_EVENTS.exists():
    st.error("Missing `data/events.csv`. Run: python scripts/generate_dataset.py")
    st.stop()

if not MODEL_PATH.exists():
    st.warning("Model not found. Run: python -m src.ml.train --data-path data/train.csv")


events = pd.read_csv(DATA_EVENTS, parse_dates=["event_timestamp"])
funnel = calculate_funnel(events).metrics

col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("Overall Funnel")
    fig = px.funnel(funnel, x="users", y="step", title="User Count by Funnel Stage")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(funnel.style.format({"step_conversion": "{:.2%}", "dropoff_rate": "{:.2%}"}), use_container_width=True)

with col2:
    st.subheader("Largest Leakage")
    leakage = funnel.sort_values("dropoff_rate", ascending=False).head(1)
    step = leakage.iloc[0]["step"]
    rate = leakage.iloc[0]["dropoff_rate"]
    st.metric("Highest drop-off stage", step)
    st.metric("Drop-off rate", f"{rate:.2%}")

st.subheader("Segmented Funnel")
segment_col = st.selectbox("Choose segment", ["device_type", "location", "traffic_source"])
segmented = calculate_segmented_funnel(events, segment_col=segment_col)
step_choice = st.selectbox("Focus step", segmented["step"].unique(), index=3)
segment_view = segmented[segmented["step"] == step_choice].sort_values("dropoff_rate", ascending=False)

fig_seg = px.bar(
    segment_view,
    x=segment_col,
    y="dropoff_rate",
    color="dropoff_rate",
    title=f"Drop-off Rate by {segment_col} at step: {step_choice}",
)
st.plotly_chart(fig_seg, use_container_width=True)
st.dataframe(segment_view.style.format({"step_conversion": "{:.2%}", "dropoff_rate": "{:.2%}"}), use_container_width=True)

st.subheader("ML Conversion Scoring")

if MODEL_PATH.exists():
    model = joblib.load(MODEL_PATH)

    c1, c2, c3 = st.columns(3)
    with c1:
        device = st.selectbox("Device", sorted(events["device_type"].unique()))
        source = st.selectbox("Traffic Source", sorted(events["traffic_source"].unique()))
    with c2:
        location = st.selectbox("Location", sorted(events["location"].unique()))
        cart_value = st.number_input("Cart Value", min_value=10.0, max_value=1000.0, value=80.0, step=1.0)
    with c3:
        discount_pct = st.slider("Discount %", min_value=0, max_value=40, value=10)
        page_load_seconds = st.slider("Page Load (s)", min_value=1.0, max_value=10.0, value=3.0, step=0.1)

    row = pd.DataFrame(
        [
            {
                "device_type": device,
                "traffic_source": source,
                "location": location,
                "cart_value": cart_value,
                "discount_pct": float(discount_pct),
                "page_load_seconds": page_load_seconds,
            }
        ]
    )

    score = model.predict_proba(row)[0, 1]
    st.metric("Predicted purchase probability", f"{score:.2%}")

    if score < 0.45:
        st.error("High drop-off risk: Consider simplified checkout and friction-reduction nudges.")
    elif score < 0.70:
        st.warning("Medium risk: Target with trust signals, payment options, or incentives.")
    else:
        st.success("High conversion likelihood: prioritize upsell/cross-sell experiments.")

    if METRICS_PATH.exists():
        with open(METRICS_PATH, "r", encoding="utf-8") as f:
            report = json.load(f)
        st.caption(f"Best model: {report['best_model']} | ROC-AUC: {report['best_metrics']['roc_auc']:.3f}")

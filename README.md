# User Journey Funnel Analysis — End-to-End Analytics + ML + Streamlit

This repository now implements a complete project flow:
1. Generate event-level funnel data.
2. Run funnel and segmented leakage analysis.
3. Train baseline + advanced ML models for conversion prediction.
4. Deploy insights and scoring in a Streamlit app.

---

## Why this project stands out

Instead of just showing descriptive charts, this project mirrors product analytics workflows used in e-commerce/SaaS:
- **Sequential funnel analysis** (visit → signup → cart → checkout → purchase)
- **Segment-level diagnosis** (device, location, traffic source)
- **Predictive modeling** for conversion risk
- **Actionable recommendations** tied to measured leakage and predicted risk

---

## Project Structure

```text
.
├── data/
├── models/
├── scripts/
│   └── generate_dataset.py
├── src/
│   ├── analytics/
│   │   └── funnel.py
│   └── ml/
│       └── train.py
├── tests/
├── requirements.txt
└── streamlit_app.py
```

---

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 1) Generate Event-Level Dataset

```bash
python scripts/generate_dataset.py --n-users 10000 --seed 42
```

Outputs:
- `data/events.csv`: user-level event stream
- `data/train.csv`: modeling table (one row per user)

Generated fields include:
- IDs and sequence: `user_id`, `event_name`, `event_timestamp`
- Segments: `device_type`, `location`, `traffic_source`
- Behavioral/numeric features: `cart_value`, `discount_pct`, `page_load_seconds`
- Label: `is_purchase`

---

## 2) Train ML Models (Baseline + Advanced)

```bash
python -m src.ml.train --data-path data/train.csv --model-dir models
```

Training includes:
- **Baseline:** Logistic Regression
- **Advanced:** Stacked Ensemble (RandomForest + HistGradientBoosting + Logistic meta-learner)

Saved artifacts:
- `models/best_model.joblib`
- `models/metrics.json`

Metrics tracked:
- ROC-AUC
- PR-AUC
- F1

---

## 3) Run Streamlit Dashboard

```bash
streamlit run streamlit_app.py
```

Dashboard modules:
- Overall funnel with step conversion and drop-off
- Segment-wise leakage comparison
- Largest leakage stage detection
- Interactive conversion scoring with recommendation bands

---

## Advanced ML concepts implemented

- Mixed-feature preprocessing with `ColumnTransformer`
- Category encoding + numeric scaling pipeline
- Model comparison (baseline vs advanced)
- Stacked ensemble for non-linear interactions
- Artifact persistence (`joblib`) + metrics tracking (`json`)

---

## Recommendation framework (non-fluffy)

Each recommendation should follow:
1. **Observed metric** (exact numbers)
2. **Hypothesis** (what causes friction)
3. **Action** (specific product/UX experiment)
4. **Expected impact + validation** (A/B test KPI)

Example:
- Observed: Mobile checkout drop-off = 61%, desktop = 37%
- Hypothesis: Mobile payment form friction and slower page load
- Action: Reduce form fields + enable wallet autofill
- Impact target: -12% relative drop in mobile checkout abandonment

---

## Next iterations

- Replace synthetic dataset with GA4/BigQuery or Olist event logs
- Add model explainability (SHAP)
- Add experiment simulation and uplift tracking
- Deploy Streamlit to Streamlit Community Cloud or container platform

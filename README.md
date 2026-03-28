# User Journey Funnel Analysis (Portfolio Project)

This project is designed to look like **real product analytics work**, not generic dashboarding.

## 1) Problem Statement
Users are not completing the intended journey (signup or purchase). The goal is to identify where users drop off, why they drop off, and what product changes are most likely to improve conversion.

---

## 2) What Makes This Project Recruiter-Grade

Most student projects stop at:
- “Here are conversion rates by step.”

This project goes further:
- **Event-level funnel construction** from sequential user events.
- **Drop-off quantification** at each stage.
- **Segmentation analysis** (device, location, traffic source).
- **Evidence-based recommendations** tied directly to measured leakage.

---

## 3) Dataset Requirements (Non-Negotiable)

To avoid a “fake funnel,” your data must include:
- `user_id` (or stable pseudo-user id)
- `event_name` (e.g., visit, signup, add_to_cart, begin_checkout, purchase)
- `event_timestamp`
- Segment fields (at least one of):
  - `device_type`
  - `geo` (country/state/city)
  - `traffic_source` / `utm_source`

### Suggested Data Sources
- **Google Analytics sample datasets in BigQuery** (best for event-level journey work)
- **Olist e-commerce dataset (Kaggle)** (good for commerce funnel proxies)
- Any public clickstream/product-analytics dataset with sequenced events

---

## 4) Funnel Definition

Define one explicit funnel, e.g.:

1. `visit`
2. `signup`
3. `add_to_cart`
4. `purchase`

### Core Metrics
- Step conversion: users reaching step N / users reaching step N-1
- Overall conversion: users reaching final step / users at step 1
- Step drop-off: 1 - step conversion
- Largest leakage point: step with max drop-off

---

## 5) Segmentation (Where You Differentiate)

Run the same funnel by:
- Device (mobile/desktop/tablet)
- Geography
- Traffic source

### Example of strong finding
> Mobile users have materially higher drop-off at payment than desktop, indicating a likely mobile checkout UX issue.

This is much stronger than just saying “users drop at checkout.”

---

## 6) Recommendation Quality Bar

Avoid vague suggestions like:
- “Improve UX”
- “Reduce steps”

Instead, tie each recommendation to specific evidence:

- **Observed:** Payment-step drop-off is 62% on mobile vs 38% on desktop.
- **Hypothesis:** Mobile payment form friction (input length/autofill/latency).
- **Action:** Simplify mobile payment fields, enable wallet/autofill, reduce validation friction.
- **Expected impact:** Reduce mobile payment drop-off by X–Y% (tracked via A/B test).

Use this four-part format for every recommendation.

---

## 7) Suggested Deliverables

- `notebooks/01_data_prep.ipynb`
- `notebooks/02_funnel_analysis.ipynb`
- `notebooks/03_segment_analysis.ipynb`
- `sql/funnel_metrics.sql`
- `dashboard/` screenshots (funnel + segmented leakage)
- `insights.md` with quantified recommendations

---

## 8) Interview-Ready Narrative

Use this structure when presenting:
1. Business problem and KPI impact
2. Funnel design and data model
3. Biggest leakage stage
4. Segment-level diagnosis
5. Prioritized recommendations with measurable expected impact
6. How you would validate via experiment

If you can defend each recommendation with numbers, the project reads like real analyst work done at a product company.

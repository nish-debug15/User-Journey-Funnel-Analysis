# 🔥 User Journey Funnel Analysis — End-to-End Data Analytics Project

> **"What companies love but students don't do"** — a full-stack funnel analysis with EDA, segmentation, and ML-powered purchase prediction.

---

## 📌 Project Overview

This project analyzes a **50,000-user e-commerce funnel** to uncover where and why users drop off across the journey:

```
Visit → Sign Up → Add to Cart → Purchase
```

It goes beyond simple drop-off counting to **segment by device, location, traffic source, and time**, identify the **biggest leakage points**, and build **ML models that predict purchase likelihood** — ending with **actionable fix recommendations**.

---

## 📊 Key Findings (TL;DR)

| Metric | Value |
|--------|-------|
| Total Visitors | 50,000 |
| Overall Signup Rate | 51.5% |
| Overall Cart Rate | 23.9% |
| **Overall Purchase Rate** | **9.7%** |
| Mobile Purchase Rate | 5.2% |
| Desktop Purchase Rate | 17.2% |
| **Mobile–Desktop Gap** | **12.0 percentage points** 🚨 |
| Best Traffic Source | Email (16.1% purchase rate) |
| Worst Traffic Source | Social Media (5.5% purchase rate) |
| Best ML Model AUC | 0.9393 (Gradient Boosting) |
| Total Simulated Revenue | ₹44.2 Lakhs |
| Avg Order Value | ₹912 |

---

## 🗂️ Project Structure

```
funnel_project/
│
├── data/
│   └── ecommerce_funnel_data.csv   # 50K users, 13 features
│
├── outputs/
│   ├── 01_funnel_overview.png       # Overall funnel + step conversion
│   ├── 02_device_segmentation.png   # Mobile / Desktop / Tablet breakdown
│   ├── 03_traffic_source.png        # Heatmap + purchase rate by source
│   ├── 04_location_analysis.png     # City-wise funnel + revenue
│   ├── 05_temporal_analysis.png     # Monthly trends + day-of-week patterns
│   ├── 06_order_value.png           # AOV distribution + device/source breakdown
│   ├── 07_ml_results.png            # ROC curves + feature importance + model comparison
│   └── 08_leakage_insights.png      # Gap analysis + cart abandonment + revenue segments
│
├── analysis.py                      # Full EDA + ML script
├── generate_data.py                 # Dataset generation script
└── README.md
```

---

## 🔍 Deep Dive: Funnel Stages

### Stage-by-Stage Drop-Off

| Stage | Users | Conversion (Overall) | Step Conversion |
|-------|-------|----------------------|-----------------|
| Visit | 50,000 | 100% | — |
| Sign Up | 25,755 | 51.5% | 51.5% |
| Add to Cart | 11,934 | 23.9% | 46.3% |
| Purchase | 4,849 | 9.7% | 40.6% |

**Biggest drop-off:** Visit → Sign-Up (48.5% of users leave here).  
This is the **#1 leakage point** — fixing the onboarding/sign-up flow has the highest leverage.

---

## 📱 Device Segmentation — The Biggest Story

Mobile users convert at **less than a third** the rate of desktop users:

| Device | Purchase Rate | Cart Abandonment |
|--------|--------------|-----------------|
| Desktop | 17.2% | ~55% |
| Tablet | ~10.4% | ~62% |
| Mobile | 5.2% | ~72% |

**Why it matters:** 55% of the traffic is mobile, but it generates a disproportionately low share of revenue.

### Fix Recommendations for Mobile:
- Simplify the payment form (reduce fields, auto-fill where possible)
- Enable one-tap checkout (Google Pay / UPI for India)
- Move primary CTA above the fold on mobile viewports
- Reduce sign-up friction — allow guest checkout
- A/B test a bottom-anchored sticky CTA button

---

## 🚦 Traffic Source Analysis

| Traffic Source | Purchase Rate | Notes |
|----------------|--------------|-------|
| Email | 16.1% | 🏆 Best — high intent, pre-warmed audience |
| Direct | ~14.8% | High intent, brand-aware |
| Organic Search | ~13.5% | Strong, SEO investment pays off |
| Referral | ~10.2% | Moderate |
| Paid Ads | ~9.0% | Below average — check landing page quality |
| Social Media | 5.5% | 🚨 Worst — low intent, high scroll behavior |

### Fix Recommendations for Traffic Sources:
- **Email:** Scale email capture + automated drip campaigns. This is your highest-ROI channel.
- **Paid Ads:** Landing pages need alignment with ad creative. Current ROAS likely poor.
- **Social Media:** Use retargeting ads, not cold acquisition. Social users need more nurturing.

---

## 📍 Location Insights

- **Mumbai & Delhi** generate the most absolute revenue (high traffic volume)
- **Bangalore** has a slightly higher purchase conversion rate relative to its volume — tech-savvy, higher purchasing power
- **Ahmedabad & Kolkata** are underperforming — potential for localized campaigns or regional payment options

---

## 📅 Temporal Patterns

- **Month:** Conversions peak in **Oct–Dec** (festive season effect — Diwali, Christmas)
- **Day of Week:** **Weekdays outperform weekends** for purchase conversion, suggesting this is a considered-purchase product category
- **Actionable:** Schedule email campaigns on Tuesday–Thursday; run weekend promotions to capture weekend traffic that doesn't convert organically

---

## 🤖 ML: Purchase Prediction

### Objective
Predict whether a visitor will **complete a purchase** (binary classification).

### Features Used
- Device type
- Location (city)
- Traffic source
- Session duration
- Whether user signed up
- Whether user added to cart
- Month of visit

### Model Performance

| Model | Test AUC | CV AUC (5-fold) |
|-------|----------|-----------------|
| Logistic Regression | 0.9370 | 0.9404 |
| Random Forest | 0.9378 | 0.9413 |
| **Gradient Boosting** | **0.9393** | **0.9416** |

All three models achieve **AUC > 0.93**, indicating excellent discrimination between buyers and non-buyers.

### Feature Importance (Random Forest)
1. `added_to_cart` — strongest signal by far
2. `signed_up`
3. `session_duration_sec`
4. `traffic_source`
5. `device`
6. `month`
7. `location`

**Insight:** Cart addition is the most predictive event. Intervening at the cart stage (exit-intent popups, email reminders, urgency nudges) has the highest ML-backed ROI.

---

## 💡 Top 5 Fix Recommendations (Prioritized by Impact)

| # | Fix | Target Stage | Expected Impact |
|---|-----|-------------|-----------------|
| 1 | Redesign mobile checkout — reduce payment steps, enable UPI one-tap | Add to Cart → Purchase | +3–5pp mobile CVR |
| 2 | Email capture popup + automated cart abandonment drip (3-email sequence) | Cart → Purchase | +2–4pp overall CVR |
| 3 | Simplify sign-up — allow social login (Google/Apple) + guest checkout option | Visit → Sign-Up | +4–6pp signup rate |
| 4 | Audit paid ads landing pages — ensure ad-to-page message match | Visit → Sign-Up | Improve paid ads CVR from 9% toward 13%+ |
| 5 | Invest in email list growth — it's 3x better than Social Media at converting | All stages | Scale best-performing channel |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.12 | Core language |
| Pandas & NumPy | Data manipulation |
| Matplotlib & Seaborn | Visualization |
| Scikit-learn | ML models (LR, RF, GB) |
| Plotly (optional) | Interactive charts |

---

## 🚀 How to Run

```bash
# 1. Clone / download the project
# 2. Install dependencies
pip install pandas numpy matplotlib seaborn scikit-learn plotly

# 3. Generate dataset
python generate_data.py

# 4. Run full analysis
python analysis.py

# 5. Outputs will be saved to outputs/ directory
```

---

## 📈 Dataset Description

Synthetically generated dataset modeled on realistic Indian e-commerce behavior (Flipkart/Meesho/Myntra patterns):

| Column | Type | Description |
|--------|------|-------------|
| user_id | str | Unique user identifier |
| visit_date | date | Date of visit |
| device | categorical | Mobile / Desktop / Tablet |
| location | categorical | Indian city |
| traffic_source | categorical | How user arrived |
| visited | int (1) | Always 1 — baseline |
| signed_up | int (0/1) | Completed registration |
| added_to_cart | int (0/1) | Added ≥1 item to cart |
| purchased | int (0/1) | Completed purchase |
| order_value | float | ₹ value (0 if no purchase) |
| session_duration_sec | int | Time on site (seconds) |
| month | int | Month number (1–12) |
| day_of_week | str | Day name |

Conversion probabilities are **device × traffic source dependent**, creating realistic segmentation patterns that reflect actual product analytics data.

---

## 🎯 What Makes This Portfolio-Worthy

1. **Real business framing** — not just "analyze this dataset", but a clear problem statement (drop-offs) with actionable output
2. **Segmentation depth** — three independent dimensions (device, source, location) with interaction effects
3. **ML layer** — 3 models, cross-validation, feature importance, all tied back to business interpretation
4. **Leakage identification** — quantified the mobile gap (12pp) and named the specific fix
5. **Indian market context** — UPI, festive season, city-tier analysis — shows real-world domain awareness

---

## 👤 Author

Built as an end-to-end portfolio project demonstrating product analytics, funnel analysis, and predictive modeling skills.

---

*Dataset is synthetically generated for portfolio purposes. Patterns and conversion rates are modeled on publicly available Indian e-commerce benchmarks.*

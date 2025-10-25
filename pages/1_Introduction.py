# pages/1_Introduction.py
# Narrative: define the problem (why this study) + what the app will show + quick data facts (France)

import streamlit as st
import pandas as pd
from utils.io import load_data, load_metadata, add_labels, basic_quality

st.title("Intro — Why this study? (France)")

st.caption("Scope: 🇫🇷 France · Monthly · Not seasonally adjusted (HICP/IPCH) · One national series (no `geo` column)")

# ---- Narrative: the problem we want to answer
st.markdown("""
## Our narrative question (plain words, France)

**What really happened to prices in France over time, and which everyday categories pushed them up or down?**  
We want to:
- See **when prices peaked** in France and **where they stand now** (overall, “headline” CP00).
- Understand **which categories** (CP01..CP12 — e.g., food, housing/energy, transport) are **above** the headline
  (so they **push** inflation) or **below** it (so they **soften** it).
- Check **stability vs. volatility**: do some categories swing wildly or stay steady?
- See if **seasonality changed since 2020** (did some months become “hotter” than before?).

**Why this matters (France)**  
A clear, simple view helps students, households, and decision-makers in **France** understand **where price pressure comes from**,
instead of only watching one big number.
""")

# ---- Data at a glance (friendly facts, France)
df_raw = load_data()
meta = load_metadata()
info = basic_quality(df_raw)

start = info["start"].date() if info["start"] is not None else None
end   = info["end"].date() if info["end"] is not None else None
n_rows = info["rows"]

unique_months = df_raw["date"].dt.to_period("M").nunique() if "date" in df_raw else 0
n_all_cats = df_raw["expenditure_1999"].nunique() if "expenditure_1999" in df_raw else 0
n_divisions = (
    df_raw["expenditure_1999"].astype(str).str.match(r"^CP\d{2}$", na=False).sum()
    if "expenditure_1999" in df_raw else 0
)

st.markdown("## Data at a glance — France")
c1, c2, c3 = st.columns(3)
c1.metric("Rows", f"{n_rows:,}")
c2.metric("Period", f"{start} → {end}")
c3.metric("Distinct months", f"{unique_months}")

c4, c5 = st.columns(2)
c4.metric("All categories (codes)", f"{n_all_cats}")
c5.metric("Top divisions present (CP01..CP12)", f"{n_divisions}")

st.info("Note: This file contains a **single national series for France** (no geographical breakdown).")

with st.expander("Small preview of the data (labels added)"):
    st.dataframe(add_labels(df_raw.head(10), meta), use_container_width=True)

# ---- How we will answer the question (roadmap of the app, France)
st.markdown("""
## How this dashboard answers the question (France)

- **Overview**: the **headline** (CP00) for **France** with **year-over-year (YoY)** and **month-over-month (MoM)** trends.
- **Categories**: compare **selected categories** (France) to the headline and see who is **above/below** it (last 12 months).
- **Volatility**: rank categories by **how much they move** (YoY variability) and how **persistent** they are.
- **Seasonality**: compare **average MoM** before 2020 vs. after 2020, month by month (France).

> Read each page top-to-bottom: a short **description above** the chart, then a **one-line conclusion** below it.
""")

# pages/5_Seasonality.py  — narrative + conclusion + sidebar selector

import streamlit as st
import plotly.express as px
import pandas as pd
from utils.io import load_metadata
from utils.prep import prepare_data, top_categories, compute_rates, seasonality_profiles

st.title("Seasonality — Before vs After 2020")

df = prepare_data()
cat_yoy = compute_rates(top_categories(df))
prof = seasonality_profiles(cat_yoy, pre=(2016, 2019), post=(2020, 2025))

meta = load_metadata()
prof = prof.merge(meta, how="left", on="expenditure_1999")  # adds expenditure_label

labels = sorted(prof["expenditure_label"].dropna().unique().tolist())
with st.sidebar:
    chosen_label = st.selectbox("Pick a category", labels)

chosen_codes = meta.loc[meta["expenditure_label"] == chosen_label, "expenditure_1999"].unique().tolist()
p = prof[prof["expenditure_1999"].isin(chosen_codes)].copy().sort_values("month")

# ---- Narrative (above chart)
st.markdown(f"""
**What this chart shows — in simple words**

Bars compare the **average month-over-month (%)** before 2020 and after 2020,  
for **{chosen_label}**, month by month (Jan..Dec).  
If the **post-2020** bar is higher, that month tended to rise **faster** after 2020.
""")

plot_df = p.melt(
    id_vars=["expenditure_label","month"],
    value_vars=["mom_pre","mom_post"],
    var_name="period", value_name="avg_mom"
)

fig = px.bar(
    plot_df, x="month", y="avg_mom", color="period",
    barmode="group",
    title=f"Average MoM (%) — {chosen_label} (pre-2020 vs post-2020)",
    labels={"avg_mom":"Avg MoM (%)","month":"Month","period":"Period"}
)
st.plotly_chart(fig, use_container_width=True)
st.caption("Help: Positive = prices went up versus the previous month. Compare the two bars for each month.")

# ---- Conclusion (below chart)
delta = p.assign(delta=p["mom_post"] - p["mom_pre"])
if not delta["delta"].dropna().empty:
    best_month = int(delta.loc[delta["delta"].idxmax(), "month"])
    worst_month = int(delta.loc[delta["delta"].idxmin(), "month"])
    st.success(f"""
**Conclusion**  
After 2020, seasonality changed most in **month {best_month}** (stronger increases)  
and least / opposite in **month {worst_month}**.  
This helps spot when this category tends to move more in the year.
""")
else:
    st.info("No clear seasonality difference detected for this category.")

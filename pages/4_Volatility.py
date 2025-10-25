# pages/4_Volatility.py  — narrative + conclusion + sidebar (no controls needed, but consistent)

import streamlit as st
import plotly.express as px
from utils.io import load_metadata, add_labels
from utils.prep import prepare_data, top_categories, volatility_persistence, compute_rates

st.title("Volatility — Which categories move the most?")

df = prepare_data()
cat_yoy = compute_rates(top_categories(df))
scores = volatility_persistence(cat_yoy)

meta = load_metadata()
scores = add_labels(scores, meta).rename(columns={"expenditure_label":"category"})

# ---- Narrative (above chart)
st.markdown("""
**What this chart shows — in simple words**

Each dot is a **category**.  
- **Up** means **more volatile** (YoY varies a lot).  
- **Right** means **more persistent** (fewer flips between positive/negative).
""")

# Chart
fig = px.scatter(
    scores, x="persistence", y="vol",
    hover_name="category",
    title="Volatility (std of YoY) vs Persistence",
    labels={"persistence":"Persistence (0–1)","vol":"Volatility (std YoY)"}
)
st.plotly_chart(fig, use_container_width=True)
st.caption("Help: Hover to see the category name. Top-right are both volatile and persistent (long stretches in one direction).")

# ---- Conclusion (below chart)
top3_vol = scores.sort_values("vol", ascending=False).head(3)
bot3_vol = scores.sort_values("vol", ascending=True).head(3)
st.success(f"""
**Conclusion**  
Most volatile categories: **{', '.join(top3_vol['category'].fillna(top3_vol.get('expenditure_1999','')).tolist())}**.  
Most stable categories: **{', '.join(bot3_vol['category'].fillna(bot3_vol.get('expenditure_1999','')).tolist())}**.
""")

# Table
st.dataframe(scores[["category","vol","persistence"]].round(3), use_container_width=True)

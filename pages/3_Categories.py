# pages/3_Categories.py  — labels only + narrative + small multiples + sidebar

import streamlit as st
import plotly.express as px
import pandas as pd
from utils.io import load_metadata, add_labels
from utils.prep import prepare_data, top_categories, headline, last12_gap_vs_headline

st.title("Categories — Compare with the headline")

# Fallback labels for CP00..CP12 (used if metadata misses some)
FALLBACK = {
    "CP00":"All items",
    "CP01":"Food and non-alcoholic beverages",
    "CP02":"Alcoholic beverages, tobacco and narcotics",
    "CP03":"Clothing and footwear",
    "CP04":"Housing, water, electricity, gas and other fuels",
    "CP05":"Furnishings, household equipment and routine household maintenance",
    "CP06":"Health",
    "CP07":"Transport",
    "CP08":"Communication",
    "CP09":"Recreation and culture",
    "CP10":"Education",
    "CP11":"Restaurants and hotels",
    "CP12":"Miscellaneous goods and services",
}

df = prepare_data()
cats = top_categories(df)
head = headline(df)

# Build mapping: metadata + fallbacks
meta = load_metadata()  # columns: expenditure_1999, expenditure_label
fallback_df = pd.DataFrame(list(FALLBACK.items()),
                           columns=["expenditure_1999","expenditure_label"])
mapping = pd.concat([meta, fallback_df], ignore_index=True)\
            .drop_duplicates(subset=["expenditure_1999"], keep="first")

# Attach human labels to categories
cats = add_labels(cats, mapping)  # adds 'expenditure_label'
if "expenditure_label" not in cats.columns:
    st.error("No category labels available. Check metadata file.")
    st.stop()

# Sidebar selector with labels only
label_options = sorted(cats["expenditure_label"].dropna().unique().tolist())
code_to_label = dict(mapping[["expenditure_1999","expenditure_label"]].dropna().values)
default_labels = [code_to_label[c] for c in ["CP01","CP04","CP07"]
                  if c in code_to_label and code_to_label[c] in label_options]

with st.sidebar:
    picked_labels = st.multiselect("Pick categories", options=label_options, default=default_labels)

if picked_labels:
    picked_codes = mapping.loc[mapping["expenditure_label"].isin(picked_labels),
                               "expenditure_1999"].unique().tolist()
    g = cats[cats["expenditure_1999"].isin(picked_codes)].copy().dropna(subset=["yoy"])

    # ---- Narrative (above combined chart)
    st.markdown(f"""
**What this chart shows — in simple words**

Each line is the **year-over-year (%)** change for a **selected category**.  
The **headline** (all items) is plotted to compare if a category is **above** (pushing prices) or **below** (softening).
""")

    # Combined chart (selected categories + headline)
    g["series"] = g["expenditure_label"]
    head_label = code_to_label.get("CP00", "All items")
    h = head[["date","yoy"]].dropna().copy()
    h["series"] = head_label

    plot_df = pd.concat(
        [g[["date","yoy","series"]], h],
        ignore_index=True
    )
    fig = px.line(
        plot_df, x="date", y="yoy", color="series",
        title="Selected categories vs headline — Year-over-year (%)",
        labels={"yoy":"YoY (%)","date":"Date","series":"Series"}
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Help: Click labels in the legend to hide/show lines. This helps focus on one or two series at a time.")

    # ---- Conclusion (below combined chart) using last-12-months gap for picked categories only
    gap_all = last12_gap_vs_headline(cats, head)                         # all categories
    gap_sel = gap_all[gap_all["expenditure_1999"].isin(picked_codes)]    # only selected
    gap_sel = gap_sel.merge(mapping, on="expenditure_1999", how="left")
    if not gap_sel.empty:
        top_above = gap_sel.sort_values("diff", ascending=False).head(1)
        top_below = gap_sel.sort_values("diff", ascending=True).head(1)
        above_name = top_above["expenditure_label"].iloc[0]
        above_gap  = top_above["diff"].iloc[0]
        below_name = top_below["expenditure_label"].iloc[0]
        below_gap  = top_below["diff"].iloc[0]
        st.success(f"""
**Conclusion (combined chart)**  
Over the **last 12 months**, **{above_name}** stood **above** the headline by **{above_gap:.2f} pp**,  
while **{below_name}** sat **below** the headline by **{below_gap:.2f} pp** among your selected categories.
""")

    # ---- Small multiples (facets) for selected categories only
    st.markdown("### Small multiples — one panel per category")
    st.markdown("This view separates each selected category to make its trend easier to read.")
    facet_df = g.rename(columns={"expenditure_label":"category"}).copy()
    fig_facets = px.line(
        facet_df, x="date", y="yoy",
        facet_col="category", facet_col_wrap=3, height=700,
        labels={"yoy":"YoY (%)","date":"Date","category":"Category"},
        title="Year-over-year (%) per selected category"
    )
    st.plotly_chart(fig_facets, use_container_width=True)
    st.caption("Help: Read panels left-to-right, then top-to-bottom. Look for peaks or long periods above 0%.")
    med_tbl = facet_df.groupby("category")["yoy"].median().sort_values(ascending=False)
    st.info(f"**Conclusion (small multiples)**  • Median YoY is highest for **{med_tbl.index[0]}** at **{med_tbl.iloc[0]:.2f}%** among the selected categories.")
else:
    st.info("Pick at least one category on the left to see the charts.")

# pages/6_Conclusions.py
# Narrative summary focused on 🇫🇷 France

import streamlit as st
import pandas as pd
from utils.io import load_metadata
from utils.prep import (
    prepare_data, headline, top_categories,
    last12_gap_vs_headline, volatility_persistence, seasonality_profiles
)

# Fallback labels for CP00..CP12 (used if metadata misses some labels)
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

st.title("Conclusions — How we answered the question (France)")
st.caption("Scope: 🇫🇷 France · Monthly · Not seasonally adjusted (HICP/IPCH) · One national series (no `geo`)")

df = prepare_data()
head = headline(df).dropna(subset=["yoy"])
cats = top_categories(df)
meta = load_metadata()

# Safe mapping (metadata + fallback)
fallback_df = pd.DataFrame(list(FALLBACK.items()), columns=["expenditure_1999","expenditure_label"])
mapping = pd.concat([meta, fallback_df], ignore_index=True)\
            .drop_duplicates(subset=["expenditure_1999"], keep="first")

if head.empty or cats.empty:
    st.info("Not enough data to compute a French summary. Please check the other pages first.")
else:
    # ---- 1) Headline story (France)
    peak_yoy = head["yoy"].max()
    peak_date = head.loc[head["yoy"].idxmax(), "date"].date()
    latest_yoy = head["yoy"].iloc[-1]
    avg12 = head["yoy"].tail(12).mean()

    st.markdown("## 1) Headline (CP00) — What happened overall in France?")
    st.markdown(f"""
- **Peak YoY (France)**: **{peak_yoy:.2f}%** in **{peak_date}**  
- **Latest YoY (France)**: **{latest_yoy:.2f}%**  
- **Average (last 12 months, France)**: **{avg12:.2f}%**  
**Reading**: we can locate the high point for France and see how much prices cooled (or not) since then.
""")

    # ---- 2) Category drivers (last 12 months gap vs headline, France)
    gap = last12_gap_vs_headline(cats, head)  # columns: expenditure_1999, diff
    gap = gap.merge(mapping, on="expenditure_1999", how="left")

    top_above = gap.sort_values("diff", ascending=False).head(3)
    top_below = gap.sort_values("diff", ascending=True).head(3)

    st.markdown("## 2) Which French categories drove/softened prices (last 12 months)?")
    st.markdown(f"""
**Above the headline (pushing, France)**: {", ".join(top_above["expenditure_label"].fillna(top_above["expenditure_1999"]).tolist())}  
**Below the headline (softening, France)**: {", ".join(top_below["expenditure_label"].fillna(top_below["expenditure_1999"]).tolist())}
""")

    # ---- 3) Volatility & persistence (France)
    scores = volatility_persistence(cats)  # columns: expenditure_1999, vol, n, sc, persistence
    scores = scores.merge(mapping, on="expenditure_1999", how="left")

    most_volatile = scores.sort_values("vol", ascending=False).head(3)
    most_stable  = scores.sort_values("vol", ascending=True).head(3)

    st.markdown("## 3) Stability vs. volatility — which French categories move the most?")
    st.markdown(f"""
**Most volatile (France)**: {", ".join(most_volatile["expenditure_label"].fillna(most_volatile["expenditure_1999"]).tolist())}  
**Most stable (France)**: {", ".join(most_stable["expenditure_label"].fillna(most_stable["expenditure_1999"]).tolist())}  
**Reading**: volatile categories swing more; stable ones move gently and change trend less often.
""")

    # ---- 4) Seasonality change (pre-2020 vs post-2020, France)
    prof = seasonality_profiles(cats, pre=(2016, 2019), post=(2020, 2025))  # exp_1999, month, mom_pre, mom_post
    if not prof.empty:
        prof = prof.merge(mapping, on="expenditure_1999", how="left")
        # average change in seasonality (post - pre) by category
        delta = (prof.assign(delta=prof["mom_post"] - prof["mom_pre"])
                      .groupby(["expenditure_1999","expenditure_label"], dropna=False)["delta"]
                      .mean().reset_index().sort_values("delta", ascending=False))

        if not delta.empty:
            most_increase = delta.head(1)
            most_decrease = delta.tail(1)

            inc_name = most_increase["expenditure_label"].fillna(most_increase["expenditure_1999"]).iloc[0]
            inc_val  = most_increase["delta"].iloc[0]
            dec_name = most_decrease["expenditure_label"].fillna(most_decrease["expenditure_1999"]).iloc[0]
            dec_val  = most_decrease["delta"].iloc[0]

            st.markdown("## 4) Seasonality — did monthly patterns change in France after 2020?")
            st.markdown(f"""
**Biggest post-2020 rise in seasonal intensity (France)**: **{inc_name}** (avg MoM post–pre = **{inc_val:.2f} pp**)  
**Biggest post-2020 drop (France)**: **{dec_name}** (avg MoM post–pre = **{dec_val:.2f} pp**)  
This shows **which French categories became more “seasonal”** after 2020 and which became calmer.
""")
        else:
            st.markdown("## 4) Seasonality — no clear change detected overall for France.")
    else:
        st.markdown("## 4) Seasonality — not enough data to compare pre/post 2020 for France.")

    # ---- Final stitched answer (France)
    st.markdown("---")
    st.markdown("## Final answer to our narrative question (France)")
    st.success(f"""
Putting the pieces together for **France**:
- The headline peak was **{peak_yoy:.2f}%** ({peak_date}); the latest reading is **{latest_yoy:.2f}%**; the 12-month average is **{avg12:.2f}%**.
- Over the last year, **top drivers above the headline** were: **{", ".join(top_above["expenditure_label"].fillna(top_above["expenditure_1999"]).tolist())}**;  
  **softening categories** were: **{", ".join(top_below["expenditure_label"].fillna(top_below["expenditure_1999"]).tolist())}**.
- The landscape was led by **volatile** groups like **{", ".join(most_volatile["expenditure_label"].fillna(most_volatile["expenditure_1999"]).tolist())}**,  
  while **{", ".join(most_stable["expenditure_label"].fillna(most_stable["expenditure_1999"]).tolist())}** stayed relatively stable.
- Seasonality **shifted the most** for **{inc_name if 'inc_name' in locals() else '—'}**, and decreased for **{dec_name if 'dec_name' in locals() else '—'}**.

**So for France**, we can say **when** prices peaked, **who** pushed them, **how** steady categories were,
and **whether the calendar pattern changed after 2020**. That is how we answered the question.
""")

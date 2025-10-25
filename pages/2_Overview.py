# pages/2_Overview.py  — narrative added (above/below charts) + sidebar controls

import streamlit as st
import plotly.express as px
import pandas as pd
from utils.prep import prepare_data, headline

st.title("Overview — Headline (CP00)")

df = prepare_data()
head = headline(df).dropna(subset=["yoy"])

if head.empty:
    st.warning("No CP00 (headline) series found.")
else:
    # Sidebar period
    dmin = head["date"].min().to_pydatetime()
    dmax = head["date"].max().to_pydatetime()
    with st.sidebar:
        start, end = st.slider(
            "Select period",
            min_value=dmin, max_value=dmax,
            value=(dmin, dmax),
            format="YYYY-MM-DD",
        )

    start_ts, end_ts = pd.Timestamp(start), pd.Timestamp(end)
    h = head[(head["date"] >= start_ts) & (head["date"] <= end_ts)].copy()

    if h.empty:
        st.info("No data in this range.")
    else:
        # ---- Narrative (above the chart)
        latest_yoy = h["yoy"].iloc[-1]
        peak_yoy = h["yoy"].max()
        peak_date = h.loc[h["yoy"].idxmax(), "date"].date()
        avg12 = h["yoy"].tail(12).mean()
        st.markdown(f"""
**What this chart shows — in simple words**

This line shows the **headline price change** (CP00), measured as **year-over-year (%)**.
You selected **{start_ts.date()} → {end_ts.date()}**.
We can already see the **peak** in this period (**{peak_yoy:.2f}%** in **{peak_date}**) and the **latest level** (**{latest_yoy:.2f}%**).
""")

        # ---- Main chart (YoY)
        fig = px.line(
            h, x="date", y="yoy",
            title="Headline inflation — Year-over-year (%)",
            labels={"yoy":"YoY (%)", "date":"Date"}
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Help: Hover points to read exact values. The higher the line, the faster prices are increasing versus last year.")

        # ---- Conclusion (below chart)
        st.success(f"""
**Conclusion (YoY)**  
Over this period, headline inflation **peaked at {peak_yoy:.2f}%**, the latest reading is **{latest_yoy:.2f}%**,  
and the **12-month average** is **{avg12:.2f}%**. This gives a clear sense of where prices stood and how they moved.
""")

        # ---- Secondary chart (MoM)
        st.markdown("### Monthly change (MoM, %)")
        st.markdown("""
This line shows the **month-over-month (%)** change.  
Small positive values mean prices increased a bit versus the previous month; negative values mean they fell.
""")
        st.line_chart(h.set_index("date")["mom"])
        st.caption("Help: MoM is more 'noisy' than YoY; look for clusters of positives/negatives.")
        pos_last12 = (h["mom"].tail(12) > 0).sum()
        st.info(f"**Conclusion (MoM)**  • In the last 12 months of the selected range, **{pos_last12}** months were positive (price increases), the others were flat/negative.")

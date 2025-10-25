import streamlit as st

st.set_page_config(page_title="HICP Dashboard — France", page_icon="💶", layout="wide")

st.title("💶 HICP Dashboard — Simple Price Story (France)")
st.caption("Scope: 🇫🇷 France · Monthly · Not seasonally adjusted (HICP/IPCH) · One national series")

st.image("data/maxresdefault.jpg", caption="Stonks", use_container_width=True)

st.markdown("""
### What this app answers
- When did prices **peak**, and where are they **now** (France)?
- Which **everyday categories** pushed prices **up** or **down** in France?
- Are some categories **volatile** or more **stable**?
- Did **seasonality** change **after 2020**?

### How to navigate
Use the **sidebar → Pages** to open:
- **0_Data_Quality** — columns, missing values, duplicates
- **1_Introduction** — our narrative question & data at a glance
- **2_Overview** — headline (CP00) with year-over-year / month-over-month
- **3_Categories** — compare categories (CP01..CP12) to the headline
- **4_Volatility** — which categories move the most
- **5_Seasonality** — before 2020 vs after 2020
- **6_Conclusions** — stitched summary of the key findings

*Tip:* If the sidebar is hidden, click the **››** icon in the top-left.
""")

st.info("Note: This dataset contains a **single national series for France** (no `geo` column). All results refer to France.")

st.markdown(
    "Data source: Eurostat via data.gouv.fr · **Scope: France (HICP/IPCH)** · Files: `data/DS_IPCH_M_data.csv`, `data/DS_IPCH_M_metadata.csv`"
)
st.link_button("data.gouv.fr", "https://www.data.gouv.fr/datasets/indice-des-prix-a-la-consommation-harmonises-mensuels/")

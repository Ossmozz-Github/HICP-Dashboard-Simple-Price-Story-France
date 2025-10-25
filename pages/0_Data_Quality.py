import streamlit as st
import pandas as pd
from utils.io import load_data

st.title("Data Quality — Missing • Duplicates • Types")

df = load_data()

st.subheader("Columns & dtypes")
st.dataframe(pd.DataFrame({"column": df.columns, "dtype": df.dtypes.astype(str)}), use_container_width=True)

st.subheader("Missing values")
miss = (
    df.isna().sum().to_frame("missing")
      .assign(missing_pct=(df.isna().mean()*100).round(2))
      .reset_index().rename(columns={"index":"column"})
)
st.dataframe(miss, use_container_width=True)

st.subheader("Duplicates")
st.write(f"Total duplicate rows: **{int(df.duplicated().sum())}**")

if "date" in df.columns:
    st.subheader("Date coverage")
    cov = pd.DataFrame({
        "start": [df["date"].min()],
        "end": [df["date"].max()],
        "unique_months": [df["date"].dt.to_period("M").nunique()]
    })
    st.dataframe(cov, use_container_width=True)

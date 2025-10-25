import pandas as pd
import streamlit as st

@st.cache_data(show_spinner=False)
def load_data(path: str = "data/DS_IPCH_M_data.csv") -> pd.DataFrame:
    df = pd.read_csv(path, sep=";")
    df.columns = df.columns.str.lower().str.strip()
    df = df.rename(columns={
        "time_period": "date",
        "obs_value": "value",
        "freq": "frequency",
        "idx_type": "index_type",
        "seasonal_adjust": "seasonal_adjustment",
    })
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"].astype(str).str.replace(",", ".", regex=False), errors="coerce")
    return df

@st.cache_data(show_spinner=False)
def load_metadata(path: str = "data/DS_IPCH_M_metadata.csv") -> pd.DataFrame:
    meta = pd.read_csv(path, sep=";")
    meta.columns = meta.columns.str.lower().str.strip()
    exp_map = meta.loc[meta["cod_var"]=="EXPENDITURE_1999", ["cod_mod","lib_mod"]].drop_duplicates()
    exp_map.columns = ["expenditure_1999","expenditure_label"]
    return exp_map

def add_labels(df: pd.DataFrame, exp_map: pd.DataFrame) -> pd.DataFrame:
    if "expenditure_1999" in df.columns:
        return df.merge(exp_map, on="expenditure_1999", how="left")
    return df

def basic_quality(df: pd.DataFrame):
    return {
        "rows": len(df),
        "start": df["date"].min() if "date" in df else None,
        "end": df["date"].max() if "date" in df else None,
        "missing_any": int(df.isna().sum().sum()),
    }

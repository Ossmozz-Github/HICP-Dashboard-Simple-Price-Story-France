import numpy as np
import pandas as pd
import streamlit as st

def _basic_filter(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "frequency" in out.columns:
        out = out[out["frequency"] == "M"]
    if "seasonal_adjustment" in out.columns:
        out = out[out["seasonal_adjustment"] == "N"]
    if "index_type" in out.columns:
        out = out[out["index_type"] == "HICP"]
    return out.sort_values("date")

@st.cache_data(show_spinner=False)
def prepare_data(path: str = "data/DS_IPCH_M_data.csv") -> pd.DataFrame:
    from utils.io import load_data
    df = load_data(path)
    df = df.dropna(subset=["date","value"])
    df = _basic_filter(df)
    return df

def headline(df: pd.DataFrame) -> pd.DataFrame:
    head = df[df["expenditure_1999"] == "CP00"].copy()
    head["mom"] = head["value"].pct_change() * 100
    head["yoy"] = head["value"].pct_change(12) * 100
    return head

def top_categories(df: pd.DataFrame) -> pd.DataFrame:
    mask = df["expenditure_1999"].astype(str).str.match(r"^CP\d{2}$")  # CP01..CP12
    out = df[mask].copy()
    out["mom"] = out.groupby("expenditure_1999")["value"].pct_change() * 100
    out["yoy"] = out.groupby("expenditure_1999")["value"].pct_change(12) * 100
    return out

def compute_rates(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "expenditure_1999" in out.columns:
        out["mom"] = out.groupby("expenditure_1999")["value"].pct_change() * 100
        out["yoy"] = out.groupby("expenditure_1999")["value"].pct_change(12) * 100
    return out

def last12_gap_vs_headline(cat_yoy: pd.DataFrame, head: pd.DataFrame) -> pd.DataFrame:
    last_date = cat_yoy["date"].max()
    start = last_date - pd.DateOffset(months=11)
    c12 = cat_yoy[cat_yoy["date"] >= start].copy()
    h12 = head[head["date"] >= start].copy()
    g_cat = c12.groupby("expenditure_1999")["yoy"].mean()
    g_head = h12["yoy"].mean()
    diff = (g_cat - g_head).sort_values(ascending=False).rename("diff").to_frame().reset_index()
    return diff

def volatility_persistence(cat_yoy: pd.DataFrame) -> pd.DataFrame:
    def sign_changes(s: pd.Series) -> int:
        s = np.sign(s.dropna())
        return int((s.shift() != s).sum() - 1 if len(s) > 1 else 0)
    agg = cat_yoy.groupby("expenditure_1999").agg(
        vol=("yoy", lambda x: x.std(skipna=True)),
        n=("yoy","count"),
        sc=("yoy", sign_changes)
    ).reset_index()
    agg["persistence"] = 1 - agg["sc"] / agg["n"].clip(lower=1)
    return agg.sort_values("vol", ascending=False)

def seasonality_profiles(cat_yoy: pd.DataFrame, pre=(2016, 2019), post=(2020, 2025)) -> pd.DataFrame:
    t = cat_yoy.copy()
    t["year"] = t["date"].dt.year
    t["month"] = t["date"].dt.month
    p1 = (t[t["year"].between(pre[0], pre[1])]
          .groupby(["expenditure_1999","month"])["mom"]
          .mean().reset_index().rename(columns={"mom":"mom_pre"}))
    p2 = (t[t["year"].between(post[0], post[1])]
          .groupby(["expenditure_1999","month"])["mom"]
          .mean().reset_index().rename(columns={"mom":"mom_post"}))
    return p1.merge(p2, on=["expenditure_1999","month"], how="outer")

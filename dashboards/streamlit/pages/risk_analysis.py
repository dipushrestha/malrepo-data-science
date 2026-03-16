"""Risk Analysis page for Streamlit dashboard."""
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

st.set_page_config(page_title="Risk Analysis", page_icon="⚠️")
st.title("⚠️ Risk Analysis")

st.markdown("Deep-dive into high-risk accounts and transaction patterns.")


@st.cache_data
def load_data():
    path = Path("data/processed/features.parquet")
    if path.exists():
        return pd.read_parquet(path)
    np.random.seed(42)
    n = 500
    return pd.DataFrame({
        "account_id": np.random.randint(1000, 9999, n),
        "transaction_amount": np.random.lognormal(3, 1, n).round(2),
        "account_balance": np.random.uniform(100, 50000, n).round(2),
        "is_fraud": np.random.choice([0, 1], n, p=[0.95, 0.05]),
    })


df = load_data()

# ── Filters ─────────────────────────────────────────────────────────
st.sidebar.header("Filters")
min_amount = st.sidebar.slider("Min Transaction Amount", 0, 10000, 0)
fraud_only = st.sidebar.checkbox("Show Fraud Only", False)

filtered = df[df["transaction_amount"] >= min_amount]
if fraud_only:
    filtered = filtered[filtered["is_fraud"] == 1]

st.metric("Filtered Transactions", f"{len(filtered):,}")

# ── Account Risk Table ──────────────────────────────────────────────
if "account_id" in filtered.columns:
    st.subheader("Account Risk Summary")
    account_risk = filtered.groupby("account_id").agg(
        txn_count=("is_fraud", "count"),
        fraud_count=("is_fraud", "sum"),
        total_volume=("transaction_amount", "sum"),
    )
    account_risk["fraud_rate"] = account_risk["fraud_count"] / account_risk["txn_count"]
    account_risk = account_risk.sort_values("fraud_rate", ascending=False)
    st.dataframe(account_risk.head(20), use_container_width=True)

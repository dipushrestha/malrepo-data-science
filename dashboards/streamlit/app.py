"""FinAnalytics Streamlit Dashboard."""
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

st.set_page_config(
    page_title="FinAnalytics Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 FinAnalytics — Fraud Detection Dashboard")
st.markdown("Real-time transaction monitoring and fraud analytics.")


@st.cache_data
def load_data():
    """Load processed transaction data."""
    path = Path("data/processed/features.parquet")
    if path.exists():
        return pd.read_parquet(path)
    # Generate sample data for demo
    np.random.seed(42)
    n = 1000
    return pd.DataFrame({
        "transaction_amount": np.random.lognormal(3, 1, n).round(2),
        "account_balance": np.random.uniform(100, 50000, n).round(2),
        "merchant_category": np.random.choice(
            ["retail", "food", "travel", "online", "atm"], n
        ),
        "is_fraud": np.random.choice([0, 1], n, p=[0.95, 0.05]),
        "hour_of_day": np.random.randint(0, 24, n),
        "day_of_week": np.random.randint(0, 7, n),
    })


df = load_data()

# ── KPI Row ─────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Transactions", f"{len(df):,}")
with col2:
    st.metric("Total Volume", f"${df['transaction_amount'].sum():,.0f}")
with col3:
    fraud_rate = df["is_fraud"].mean() * 100
    st.metric("Fraud Rate", f"{fraud_rate:.2f}%")
with col4:
    avg_amount = df["transaction_amount"].mean()
    st.metric("Avg Transaction", f"${avg_amount:.2f}")

st.divider()

# ── Charts ──────────────────────────────────────────────────────────
left, right = st.columns(2)

with left:
    st.subheader("Fraud by Merchant Category")
    if "merchant_category" in df.columns:
        fraud_by_cat = df.groupby("merchant_category")["is_fraud"].mean().sort_values()
        st.bar_chart(fraud_by_cat)

with right:
    st.subheader("Transaction Amount Distribution")
    st.histogram_chart = st.bar_chart(
        pd.cut(df["transaction_amount"], bins=20).value_counts().sort_index()
    )

# ── Hourly Pattern ──────────────────────────────────────────────────
st.subheader("Hourly Fraud Pattern")
if "hour_of_day" in df.columns:
    hourly = df.groupby("hour_of_day").agg(
        total=("is_fraud", "count"),
        fraud=("is_fraud", "sum"),
    )
    hourly["fraud_rate"] = hourly["fraud"] / hourly["total"]
    st.line_chart(hourly["fraud_rate"])

# ── Data Table ──────────────────────────────────────────────────────
st.subheader("Recent Transactions")
st.dataframe(df.head(50), use_container_width=True)

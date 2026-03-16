"""FinAnalytics Dash Dashboard."""
from pathlib import Path

import numpy as np
import pandas as pd

try:
    import dash
    from dash import dcc, html, dash_table
    import plotly.express as px
    import plotly.graph_objects as go
except ImportError:
    raise ImportError("Install dash and plotly: pip install dash plotly")


def load_data():
    path = Path("data/processed/features.parquet")
    if path.exists():
        return pd.read_parquet(path)
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
    })


df = load_data()

app = dash.Dash(__name__, title="FinAnalytics Dashboard")

app.layout = html.Div([
    html.H1("FinAnalytics — Fraud Detection Dashboard"),

    html.Div([
        html.Div([
            html.H3(f"{len(df):,}"),
            html.P("Total Transactions"),
        ], className="metric-card"),
        html.Div([
            html.H3(f"{df['is_fraud'].mean()*100:.2f}%"),
            html.P("Fraud Rate"),
        ], className="metric-card"),
    ], style={"display": "flex", "gap": "20px"}),

    html.Div([
        dcc.Graph(
            figure=px.histogram(
                df, x="transaction_amount", color="is_fraud",
                title="Transaction Amount Distribution",
                nbins=50, barmode="overlay",
            )
        ),
        dcc.Graph(
            figure=px.bar(
                df.groupby("merchant_category")["is_fraud"].mean().reset_index(),
                x="merchant_category", y="is_fraud",
                title="Fraud Rate by Merchant Category",
            )
        ),
    ]),

    html.H3("Recent Transactions"),
    dash_table.DataTable(
        data=df.head(50).to_dict("records"),
        columns=[{"name": c, "id": c} for c in df.columns[:8]],
        page_size=20,
        style_table={"overflowX": "auto"},
    ),
])


if __name__ == "__main__":
    app.run(debug=True, port=8050)

"""Reusable layout components for Dash dashboard."""
try:
    from dash import html, dcc
except ImportError:
    pass


def metric_card(title: str, value: str):
    return html.Div([
        html.H3(value, style={"margin": "0"}),
        html.P(title, style={"margin": "0", "color": "#666"}),
    ], style={
        "padding": "20px",
        "border": "1px solid #ddd",
        "borderRadius": "8px",
        "textAlign": "center",
        "minWidth": "150px",
    })


def section_header(title: str):
    return html.H2(title, style={"marginTop": "30px", "marginBottom": "10px"})

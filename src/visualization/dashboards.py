import plotly.express as px
import plotly.graph_objects as go

def create_stock_chart(df, symbol):
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'])])
    fig.update_layout(title=f'{symbol} Stock Price')
    return fig

def create_volatility_heatmap(correlation_matrix):
    fig = px.imshow(correlation_matrix, text_auto=True)
    return fig

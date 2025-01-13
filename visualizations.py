import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

def create_time_series(df, metric, title):
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df['date'],
            y=df[metric],
            name=metric.capitalize()
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title=metric.capitalize(),
        hovermode='x unified',
        showlegend=False,
        height=400
    )
    return fig

def create_earnings_breakdown(df):
    fig = go.Figure()

    # Daily earnings
    fig.add_trace(
        go.Bar(
            x=df['date'],
            y=df['earnings'],
            name='Daily Earnings'
        )
    )

    # Add trend line
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['earnings'].rolling(window=7).mean(),
            name='7-day Moving Average',
            line=dict(color='red', width=2)
        )
    )

    fig.update_layout(
        title='Daily Earnings with Trend',
        xaxis_title="Date",
        yaxis_title="Earnings ($)",
        height=400,
        hovermode='x unified'
    )
    return fig

def create_efficiency_metrics(df):
    fig = go.Figure()

    # Calculate metrics
    df['earnings_per_hour'] = df['earnings'] / df['hours']
    df['earnings_per_mile'] = df['earnings'] / df['miles']

    # Add bars for earnings per hour
    fig.add_trace(
        go.Bar(
            x=df['date'],
            y=df['earnings_per_hour'],
            name='Earnings per Hour',
            marker_color='blue'
        )
    )

    # Add bars for earnings per mile on secondary y-axis
    fig.add_trace(
        go.Bar(
            x=df['date'],
            y=df['earnings_per_mile'],
            name='Earnings per Mile',
            marker_color='green',
            yaxis='y2'
        )
    )

    fig.update_layout(
        title='Efficiency Metrics Over Time',
        xaxis_title="Date",
        yaxis_title="Earnings per Hour ($)",
        yaxis2=dict(
            title="Earnings per Mile ($)",
            overlaying='y',
            side='right'
        ),
        height=400,
        hovermode='x unified',
        barmode='group'
    )
    return fig

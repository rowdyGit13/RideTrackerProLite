import pandas as pd

def calculate_statistics(df):
    if df.empty:
        return {
            'total_earnings': 0,
            'total_hours': 0,
            'total_miles': 0,
            'avg_hourly_rate': 0,
            'avg_miles_per_hour': 0,
            'earnings_per_mile': 0
        }
    
    stats = {
        'total_earnings': df['earnings'].sum(),
        'total_hours': df['hours'].sum(),
        'total_miles': df['miles'].sum(),
        'avg_hourly_rate': df['earnings'].sum() / df['hours'].sum(),
        'avg_miles_per_hour': df['miles'].sum() / df['hours'].sum(),
        'earnings_per_mile': df['earnings'].sum() / df['miles'].sum()
    }
    return stats

def format_currency(value):
    return f"${value:,.2f}"

def format_number(value):
    return f"{value:,.2f}"

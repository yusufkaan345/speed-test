from dash import html, dcc

def create_layout():
    return html.Div([
        html.H1("Speedtest Dashboard", style={'textAlign': 'center'}),
        dcc.Dropdown(
            id='time-period-dropdown',
            options=[
                {'label': 'Günlük', 'value': 'daily'},
                {'label': 'Haftalık', 'value': 'weekly'},
            ],
            value='daily',  # Varsayılan olarak günlük seçilsin
            style={'width': '50%', 'margin': '0 auto'}
        ),
        dcc.Interval(
            id='interval-component',
            interval=300*1000,  # 5 dk da bir
            n_intervals=0
        ),
        dcc.Graph(id='speed-graph')
    ])
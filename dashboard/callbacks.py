import json
from datetime import datetime, timedelta
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from dash import html, dcc

def load_results(output_file):
    try:
        with open(output_file, 'r') as f:
            data = json.load(f)
            if not data:
                raise ValueError("JSON file is empty")
            return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return []

def register_callbacks(app, output_file):
    @app.callback(
        Output('speed-graph', 'figure'),
        [Input('time-period-dropdown', 'value'), Input('interval-component', 'n_intervals')]
    )
    def update_graph(time_period, n_intervals):
        results = load_results(output_file)
        if not results:
            return {}

        if time_period == 'daily':
            # Günlük verileri alma (son 5 ölçüm)
            daily_data = results[-5:]
            timestamps = [datetime.strptime(result['timestamp'], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S") for result in daily_data]
            download_speeds = [result['download'] / 1_000_000 for result in daily_data]
            upload_speeds = [result['upload'] / 1_000_000 for result in daily_data]
            pings = [result['ping'] for result in daily_data]

            title = 'Last 5 Measurements'
        elif time_period == 'weekly':
            # Haftalık verileri gruplama
            weekly_data = group_weekly_data(results)
            timestamps = [key.strftime("%Y-%m-%d") for key in weekly_data.keys()]
            download_speeds = [value['download'] / 1_000_000 for value in weekly_data.values()]
            upload_speeds = [value['upload'] / 1_000_000 for value in weekly_data.values()]
            pings = [value['ping'] for value in weekly_data.values()]

            title = 'Weekly Averages'

        figure = {
            'data': [
                go.Scatter(x=timestamps, y=download_speeds, mode='lines+markers', name='Download Speed (Mbps)'),
                go.Scatter(x=timestamps, y=upload_speeds, mode='lines+markers', name='Upload Speed (Mbps)'),
                go.Scatter(x=timestamps, y=pings, mode='lines+markers', name='Ping (ms)')
            ],
            'layout': {
                'title': title,
                'xaxis': {'title': 'Timestamp'},
                'yaxis': {'title': 'Speed (Mbps) / Ping (ms)'}
            }
        }
        return figure

def group_weekly_data(data):
    """
    Verileri haftalık olarak gruplar ve günlük ortalamaları hesaplar.
    """
    grouped_data = {}
    today = datetime.now().date()

    # Son 7 günü hesapla
    start_date = today - timedelta(days=7)

    for result in data:
        timestamp = datetime.strptime(result['timestamp'], "%Y-%m-%d %H:%M:%S")
        result_date = timestamp.date()

        # Sadece son 7 günün verileri
        if start_date <= result_date <= today:
            if result_date not in grouped_data:
                grouped_data[result_date] = {'download': 0, 'upload': 0, 'ping': 0, 'count': 0}

            grouped_data[result_date]['download'] += result['download']
            grouped_data[result_date]['upload'] += result['upload']
            grouped_data[result_date]['ping'] += result['ping']
            grouped_data[result_date]['count'] += 1

    # Ortalamaları hesapla
    for key, value in grouped_data.items():
        value['download'] /= value['count']
        value['upload'] /= value['count']
        value['ping'] /= value['count']
        del value['count']

    return grouped_data
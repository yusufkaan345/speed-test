from dash import Dash
from dashboard.layouts import create_layout
from dashboard.callbacks import register_callbacks

def create_app():
    app = Dash(__name__)
    output_file = 'speedtest_results.json'

    app.layout = create_layout()
    register_callbacks(app, output_file)
    
    return app.server  # WSGI uygulamasını döndür

def start_dashboard():
    app = Dash(__name__)
    output_file = 'speedtest_results.json'

    app.layout = create_layout()
    register_callbacks(app, output_file)

    app.run_server(debug=False, host='0.0.0.0', port=8050)

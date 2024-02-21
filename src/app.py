from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP
from layout import create_layout

app = Dash(__name__, external_stylesheets=[BOOTSTRAP],
               suppress_callback_exceptions=True)
server = app.server

app.title = 'Deep Generative Models for Pharmaceutical Process Design - Survey'
app.layout = create_layout(app)

if __name__ == '__main__':
    app.run_server(debug=True)

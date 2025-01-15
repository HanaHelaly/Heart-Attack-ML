from dash import Dash
import dash_bootstrap_components as dbc
# Intiliazing Dash app
app = Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.UNITED, dbc.icons.BOOTSTRAP])
server = app.server

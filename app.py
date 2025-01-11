from dash import Dash
import dash_bootstrap_components as dbc

# meta_tags are required for the app layout to be mobile responsive
app = Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.UNITED, dbc.icons.BOOTSTRAP])
server = app.server

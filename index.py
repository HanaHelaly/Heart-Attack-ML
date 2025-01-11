import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
# Connect to main app.py file
from app import app
from dash_iconify import DashIconify
from app import server

# Connect to your app pages
from pages import Homepage, page2, page3

heart_icon = html.Img(src=app.get_asset_url('heart.png'),
                      style={'height': '34px', 'margin-right': 10,'margin-bottom':8})
home_icon = DashIconify(icon="fa:home", style={'margin-right': 18,'font-size':25})
world_icon = DashIconify(icon="fa6-solid:earth-americas", style={'margin-right': 18,'font-size':25})
prediction_icon = DashIconify(icon="material-symbols:stethoscope-rounded", style={'margin-right': 18,'font-size':25})

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    dbc.NavbarSimple(
        [
            dbc.NavItem(dbc.NavLink([home_icon],style={"color":"#1a1a1c"}, href="/pages/homepage")),
            dbc.NavItem(dbc.NavLink([world_icon], style={"color":"#1a1a1c"},href="/pages/page2")),
            dbc.NavItem(dbc.NavLink([prediction_icon],style={"color":"#1a1a1c"}, href="/pages/page3"))
        ],
    brand=html.Div([heart_icon,"HeartAnalyzer: Insights & Prediction Tool"],style={"font-weight":"bold","color":'#1a1a1c','font-size':30}),
    color='#F3E6E4',
    brand_href="#",
    dark=True,
),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pages/homepage':
        return Homepage.layout
    if pathname == '/pages/page2':
        return page2.layout
    if pathname == '/pages/page3':
        return page3.layout
    else:
        return Homepage.layout


if __name__ == '__main__':
    app.run_server(port='8050',debug=False)
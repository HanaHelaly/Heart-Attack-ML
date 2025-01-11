import dash
from dash import html, dcc, Dash, Input, Output, State
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import pathlib
from app import app
import plotly.graph_objects as go

#data frame for geographical distributions
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

df1 = pd.read_csv(DATA_PATH.joinpath("cardiovascular_deaths.csv"))

years = df1['Year'].unique()
marks = {str(year): str(year) for year in years if year % 5 == 0 or year == 2019}

# Create the layout
layout = dbc.Container(
    [
        dbc.Row(
            [
                html.H2("Global Cardiovascular Disease Mortality Rates", className='mb-5',
                        style={'color': '#1a1a1c', 'font-weight': 'bold',
                               'padding-top': '50px', 'text-align': 'center', 'font-size': '30px'})
            ]
        ),

        dbc.Row(
            [
                dbc.Col(
                    dcc.Slider(
                        id="year_slider",
                        min=df1['Year'].min(),
                        max=2019,
                        step=None,
                        value=2019,
                        marks=marks
                    ),
                    width=6, align='center'
                )
            ], justify='center', style={'margin-bottom': '0px'}
        ),

        dbc.Row(
            [
                dbc.Col(
                    html.Div(dcc.Graph(id="map_holder"), style={'position': 'relative'})
                )
            ]
        ),
    ]
)


# Define the callback
@app.callback(
    Output('map_holder', 'figure'),
    [Input('year_slider', 'value')]
)
def update_graph(selected_year):
    # Filter data for the selected year
    filtered_data = df1[df1['Year'] == selected_year]

    if filtered_data.empty:
        fig = px.scatter_geo()
    else:
        fig = px.scatter_geo(filtered_data, locations="Code",
                             color="Deaths - Cardiovascular diseases - Sex: Both - Age: All Ages (Number)",
                             hover_name="Entity",
                             size="Deaths - Cardiovascular diseases - Sex: Both - Age: All Ages (Number)",
                             projection="natural earth",
                             labels={"Deaths - Cardiovascular diseases - Sex: Both - Age: All Ages (Number)": "Deaths"})

        fig.update_layout(legend=dict(x=0.8))

    return fig

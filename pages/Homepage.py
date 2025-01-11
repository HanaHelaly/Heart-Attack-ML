import pathlib
import dash
from dash import html, dcc, Dash, Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from app import app


# read icons from asstes
download_icon = DashIconify(icon="lets-icons:arrow-drop-down-big", style={'margin-right': 5})
blood_icon = html.Img(src=app.get_asset_url('blood-sample.png'),
                      style={'height': '48px', 'margin-right': 10})
ecg_icon = html.Img(src=app.get_asset_url('ecg.png'),
                           style={'height': '48px', 'margin-right': 10})
stress_icon = html.Img(src=app.get_asset_url('treadmill.png'),
                           style={'height': '48px', 'margin-right': 10})
blood_pressure_icon = html.Img(src=app.get_asset_url('blood-pressure.png'),
                           style={'height': '48px', 'margin-right': 10})
imaging_icon = html.Img(src=app.get_asset_url('diagnose.png'),
                           style={'height': '48px', 'margin-right': 10})
heart_image = html.Img(src=app.get_asset_url('heart-image.png'),
                       style={'height': '310px', 'width': 'auto', 'margin-left': '50px','margin-top': '330px'})



layout = dbc.Container([
    dbc.Row([
    html.Br(),

    dbc.Col([
        dbc.Row([
            html.H5("Welcome to HeartAnalyzer: Your personalized tool for predicting heart attack risks. Based on historical patient data, we aim to give you valuable insights into heart health and help with early detection",
                    className='mb-5',
                    style={'color': '#1a1a1c', 'padding-top': '100px', 'text-align': 'justify'}),
            dbc.Col([
            dbc.Button([download_icon, "Read More"], outline=True, color='secondary',
                       id="proj_des_button",className='mb-2', size=3)],width={'size': 4}),
            html.Div(id="proj_des")
        ],
            className='float-left mb-4'),
        dbc.Row([
        dbc.Col([
            html.P("To perform the heart attack prediction test, you would need the following types of tests:"),
            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        [
                            html.P(
                                "Cholesterol levels and fasting blood sugar levels to assess cardiovascular risk."
                                , style={'text-align': 'justify', 'color':'#272727'}),
                        ],
                        title=html.Div([

                            html.Span(blood_icon),
                            html.Div([
                                html.P("Blood Tests",
                                       style={'color':'#272727', 'font-size':16})])

                        ], style={'display': 'inline-flex', 'align-items': 'center'})
                    ),

                    dbc.AccordionItem(
                        [
                            html.P("Measures heart electrical activity and detects abnormalities such as ST-T wave changes or left ventricular hypertrophy.",
                                style={'text-align': 'justify', 'color':'#272727'}),
                        ],
                         title = html.Div([

                            html.Span(ecg_icon),
                            html.Div([
                                html.P("ECG (Electrocardiogram)",
                                       style={'color': '#272727', 'font-size': 16})])

                        ], style={'display': 'inline-flex', 'align-items': 'center'})
                    ),
                    dbc.AccordionItem(
                        [
                            html.P(
                                "Monitors max heart rate, exercise-induced chest pain, and ST segment depression during exercise."
                                , style={'text-align': 'justify', 'color':'#272727'}),
                        ],
                        title = html.Div([

                        html.Span(stress_icon),
                        html.Div([
                            html.P("Cardiovascular Stress Test",
                                   style={'color': '#272727', 'font-size': 16})])

                    ], style={'display': 'inline-flex', 'align-items': 'center'})

                    ),
                    dbc.AccordionItem(
                        [
                            html.P(
                                "Resting blood pressure to assess heart health and risk of cardiovascular diseases."
                                , style={'text-align': 'justify', 'color':'#272727'}),
                        ],
                        title = html.Div([

                        html.Span(blood_pressure_icon),
                        html.Div([
                            html.P("Blood Pressure Measurement",
                                   style={'color': '#272727', 'font-size': 16})])

                         ], style={'display': 'inline-flex', 'align-items': 'center'})
                    ),
                    dbc.AccordionItem(
                        [
                            html.P(
                                "Checks for blockages or abnormalities in coronary arteries and identifies blood disorders that affect heart health.",
                                style={'text-align': 'justify', 'color':'#272727'}),
                        ],
                        title = html.Div([

                        html.Span(imaging_icon),
                        html.Div([
                            html.P("Imaging and Diagnostic Tests",
                                   style={'color': '#272727', 'font-size': 16})])

                        ], style={'display': 'inline-flex', 'align-items': 'center'})
                    ),

                ],style={'margin-top': '20px'}
            )

            ],className='float-left')
            ])
            ], width={'size': 7}),

        dbc.Col([
        html.Span(heart_image)
        ])
        ])
    ])


@app.callback(
    Output("proj_des", "children"),
    Input("proj_des_button", "n_clicks")
)
def show_text(n_clicks):
    if n_clicks==None:
        return None
    if n_clicks % 2 != 0:
        dp = html.P('HeartAnalyzer is designed to provide both data-driven insights and heart attack predictions based on key medical attributes. By utilizing advanced machine learning models, this tool helps healthcare providers assess heart attack risk by analyzing factors like age, cholesterol levels, blood pressure, and more',
                    className="text-monospace float-none mt-3",
                    style={'color': '#272727', 'text-align': 'justify'})
        return dp
    else:
        return None


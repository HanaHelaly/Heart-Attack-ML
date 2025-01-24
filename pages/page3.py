# Import necessary libraries
import pathlib
from dash import html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
import joblib
import xgboost
from app import app
import shap
import plotly.graph_objects as go
import numpy as np

# Path to the project directory
PATH = pathlib.Path(__file__).parent

# Path to the models folder
MODEL_PATH = PATH.joinpath("../models").resolve()
# Load model and preprocessing transformers
model = joblib.load(MODEL_PATH.joinpath("xgb_model.joblib"))

fitted_column_transformer = joblib.load(MODEL_PATH.joinpath("xgb_preprocessor.joblib"))

# Define feature names
cols = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']

# Define layout for the app
layout = dbc.Container([
    html.Div(id="input-container", children=[
    html.H2("Predict Your Heart Health Risk Now", style={'textAlign': 'left', 'margin-bottom': '40px', 'margin-top': '40px'}),

    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Label('Gender:'),
                dcc.Dropdown(
                    options=[{'label': 'Male', 'value': 1}, {'label': 'Female', 'value': 0}],
                    id='gender', value=1
                ),
            ],style={'margin-bottom': '15px'}),
            html.Div([
                dbc.Label('Age:', style={'margin-right': '285px', 'display': 'inline-block'}),
                dcc.Input(id='age', type='number', value=50, min=0),
            ],style={'margin-bottom': '15px'}),
            html.Div([
                dbc.Label('Resting blood pressure (mm Hg):', style={'margin-right': '85px', 'display': 'inline-block'}),
                dcc.Input(id='trestbps', type='number', value=150, min=0),
            ],style={'margin-bottom': '15px'}),
            html.Div([
                dbc.Label('Serum cholesterol level (mg/dl):', style={'margin-right': '95px', 'display': 'inline-block'}),
                dcc.Input(id='chol', type='number', value=240, min=0),
            ],style={'margin-bottom': '15px'}),
            html.Div([
                dbc.Label('Maximum heart rate achieved (bpm):', style={'margin-right': '60px', 'display': 'inline-block'}),
                dcc.Input(id='thalach', type='number', value=150, min=0),
            ],style={'margin-bottom': '15px'}),
            html.Div([
                dbc.Label('ST segment change during exercise (mm):', style={'margin-right': '30px', 'display': 'inline-block'}),
                dcc.Input(id='oldpeak', type='number', value=2.5, step=0.1),
            ],style={'margin-bottom': '15px'}),
        ], width=6),

        dbc.Col([
            html.Div([
                dbc.Label('Chest pain type:'),
                dcc.Dropdown(
                    options=[
                        {'label': 'Typical angina', 'value': 0},
                        {'label': 'Atypical angina', 'value': 1},
                        {'label': 'Non-anginal pain', 'value': 2},
                        {'label': 'Asymptomatic', 'value': 3}
                    ],
                    id='cp', value=0
                ),
            ]),
            html.Div([
                dbc.Label('Fasting blood sugar > 120 mg/dl:'),
                dcc.Dropdown(
                    options=[{'label': 'Yes', 'value': 1}, {'label': 'No', 'value': 0}],
                    id='fbs', value=0
                ),
            ]),
            html.Div([
                dbc.Label('ECG test results:'),
                dcc.Dropdown(
                    options=[
                        {'label': 'Normal', 'value': 0},
                        {'label': 'ST-T wave abnormality', 'value': 1},
                        {'label': 'Left ventricular hypertrophy', 'value': 2}
                    ],
                    id='restecg', value=0
                ),
            ]),
            html.Div([
                dbc.Label('Exercise-induced angina:'),
                dcc.Dropdown(
                    options=[{'label': 'Yes', 'value': 1}, {'label': 'No', 'value': 0}],
                    id='exang', value=0
                ),
            ]),
            html.Div([
                dbc.Label('ST slope during peak exercise:'),
                dcc.Dropdown(
                    options=[
                        {'label': 'Upsloping', 'value': 0},
                        {'label': 'Flat', 'value': 1},
                        {'label': 'Downsloping', 'value': 2}
                    ],
                    id='slope', value=1
                ),
            ]),
            html.Div([
                dbc.Label('Number of major vessels (0–3):'),
                dcc.Dropdown(
                    options=[{'label': str(i), 'value': i} for i in range(4)],
                    id='ca', value=0
                ),
            ]),
            html.Div([
                dbc.Label('Blood disorder condition:'),
                dcc.Dropdown(
                    options=[
                        {'label': 'Normal', 'value': 0},
                        {'label': 'Fixed defect', 'value': 1},
                        {'label': 'Reversible defect', 'value': 2}
                    ],
                    id='thal', value=0
                ),
            ]),
        ], width=6),
    dbc.Row(dbc.Col([
        html.Div([
            dbc.Button(id="button", outline=True,color='secondary', size="lg", children="Submit")
        ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'height': '10vh', 'margin-bottom': '30px'})
    ], width=12))
    ]),

    ]),
    dbc.Row([
            dbc.Col([
                dcc.Graph(id='shap_graph')  # Initially hidden, shown after submit
            ])
        ], style={'margin-top': '20px'}),
    dbc.Row(html.Div(id="output_prediction", style={'margin-top': '20px','textAlign': 'center'})),
    # Add Reset Button
    dbc.Row(dbc.Col([
        html.Div([
            dbc.Button(id="reset_button", outline=True, color='secondary', size="lg", children="Reset", className="me-3")
        ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'height': '10vh', 'margin-bottom': '30px'})
    ], width=12)),
    dbc.Row([
        dbc.Col([
            html.Div(id="alerts")
        ])
    ])
    ])


# Define callback function

@app.callback(
    [Output("input-container", "style"),  # Hide the input form
     Output("output_prediction", "children"),  # Show the prediction result
     Output('shap_graph', 'figure')],  # SHAP figure output
    [Input("button", "n_clicks")],
    [State("age", "value"),
     State("trestbps", "value"),
     State("chol", "value"),
     State("thalach", "value"),
     State("oldpeak", "value"),
     State("gender", "value"),
     State("cp", "value"),
     State("fbs", "value"),
     State("restecg", "value"),
     State("exang", "value"),
     State("slope", "value"),
     State("ca", "value"),
     State("thal", "value")]
)
def predict_and_explain(n_clicks, age, trestbps, chol, thalach, oldpeak, gender, cp, fbs, restecg, exang, slope, ca, thal):
    if n_clicks is None:
        return {"display": "block"}, None, {}  # Show inputs if no clicks and return empty figure for SHAP plot

    # User input values
    feature_values = {
        'age': int(age) if age else 0,
        'trestbps': int(trestbps) if trestbps else 150,
        'chol': int(chol) if chol else 240,
        'thalach': int(thalach) if thalach else 125,
        'oldpeak': float(oldpeak) if oldpeak else 2.5,
        'sex': int(gender) if gender else 1,
        'cp': int(cp) if cp else 0,
        'fbs': int(fbs) if fbs else 0,
        'restecg': int(restecg) if restecg else 0,
        'exang': int(exang) if exang else 0,
        'slope': int(slope) if slope else 1,
        'ca': int(ca) if ca else 0,
        'thal': int(thal) if thal else 0
    }

    # Prepare the features and make the prediction
    sample = pd.DataFrame([feature_values], columns=cols)
    transformed_features = pd.DataFrame(fitted_column_transformer.transform(sample))
    # Model prediction
    probability = model.predict_proba(transformed_features)[:, 1]
    print(probability)
    prediction = (probability >= 0.57).astype(int)

    # Define the alert message based on the prediction
    if prediction == 0:
        alert_color = "success"
        alert_message = " Low risk of a heart attack"
        alert_icon = "bi bi-check-circle-fill"
    else:
        alert_color = "danger"
        alert_message = "High risk of a heart attack"
        alert_icon = "bi bi-x-octagon-fill me-2"

    alert = dbc.Alert([html.I(className=alert_icon), alert_message], color=alert_color, className="d-flex align-items-center")

    # masker = shap.maskers.Independent(transformed_features)
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(transformed_features)
    #Extract the feature names and their corresponding SHAP values
    feature_names = transformed_features.columns
    shap_contributions = shap_values[1]  
    # Convert shap_contributions to a list or numpy array to avoid issues with single values
    shap_contributions = list(shap_contributions) if isinstance(shap_contributions, np.ndarray) else [shap_contributions]
    sorted_indices = sorted(range(len(shap_contributions)), key=lambda k: abs(shap_contributions[k]), reverse=True)
    sorted_shap_contributions = [shap_contributions[i] for i in sorted_indices]
    sorted_feature_names = [feature_names[i] for i in sorted_indices]

    trace = go.Bar(
        x=sorted_feature_names,
        y=sorted_shap_contributions,  # Sorted SHAP contributions
        marker=dict(color=sorted_shap_contributions, colorscale="RdBu"),
        text=sorted_shap_contributions,
        hoverinfo="text"
    )

    fig_layout = go.Layout(
        title="Breaking Down Your Heart Disease Risk Prediction",
        title_font=dict(size=20,color='#1a1a1c'),  # Title font color
        plot_bgcolor='#fff8f8',
        # paper_bgcolor='#f3e8e8',  # Background of the whole figure
        xaxis=dict(
            title="Features",
            title_font=dict(size=16, color='#a84d4d'),  # Axis title font color
            tickfont=dict(size=12, color='#a84d4d')  # Tick font color
        ),
        yaxis=dict(
            title="SHAP Value (Feature Contribution)",
            title_font=dict(size=16, color='#a84d4d'),  # Axis title font color
            tickfont=dict(size=12, color='#a84d4d')  # Tick font color
        ),
        showlegend=False,
        width=1200,
        # height=700,
        margin=dict(l=300, r=50, t=50, b=100),
        bargap=0.2
    )

    # Create the Plotly figure
    fig = go.Figure(data=[trace], layout=fig_layout)

    # Return the SHAP plot and prediction output
    return {"display": "none"}, html.Div([alert]), fig

# Define callback for resetting the page
@app.callback(
    Output('url', 'href'),  
    [Input("reset_button", "n_clicks")],
    [State('url', 'pathname')] 
)
def refresh_page(n_clicks, current_url):
    if n_clicks is None:
        return None  
    return current_url

from doctest import OutputChecker
import dash, json, math
import pandas as pd, plotly.express as px, plotly.graph_objs as go
import dash_bootstrap_components as dbc
from pathlib import Path
from dash import Dash, dcc, html, Input, Output
from cmath import nan
from flask import redirect

#dash.register_page(__name__)

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])
# add suppress_callback_exceptions=True when done - to hide error messages


DATA_PATH = Path(__file__).parent.joinpath('data')
genre_list = ['Action','Adventure','Animation','Comedy','Crime','Documentary','Drama','Family','Fantasy','History','Horror','Music','Mystery','Science-Fiction','Romance','Thriller','TV Movie','War','Western']


def preferences():
    return


app.layout = dbc.Container(
    [
        html.H1("NetPix"),
        html.Br(),
        html.H2(children=["Helping you pick the best flicks"]),
        html.Br(),
        html.Br(),
        html.H3(children=["What are your preferences?"]),

        html.Br(),
        html.Br(),

        dbc.Row([

            dcc.Dropdown(
                    id='genre-dropdown',
                    options=[{'label': x, 'value': x} for x in genre_list],
                    placeholder='Select your ideal genres (we recommend picking no more than 5)',
                    multi=True

                    ),

        ]),

        html.Br(),
        html.Br(),

        dbc.Row([
            

            dcc.Slider(min=0, max=360, step=5,
                value=150,
                tooltip={"placement": "bottom", "always_visible": True}, 
                id='runtime-slider'
                ),

            html.Div(id='slider-output-container')

        ]),

        html.Div(style={'text-align': 'center'}, children=[
            html.Button('Confirm', id='confirm-button', n_clicks=0),
        ])
        
    ],

    fluid=True,
)


@app.callback(
    Output('slider-output-container', 'children'),
    Input('runtime-slider', 'value')
)

def update_runtime(value):
    hours = value//60
    minutes= value - (hours*60)

    if hours == 0:
        if minutes == 1:
            time = f"Max: {minutes} minute"
        else:
            time = f"Max: {minutes} minutes"
    elif hours == 1:
        if minutes ==1:
            time = f"Max: {hours} hour and {minutes} minute"
        else:
            time = f"Max: {hours} hour and {minutes} minutes"
    else:
        if minutes == 1:
            time = f"Max: {hours} hours and {minutes} minute"
        else:
            time = f"Max: {hours} hours and {minutes} minutes"

    return time


if __name__ == '__main__':
    app.run_server(debug=True, port=8888)


# Copied from the Dash tutorial documentation at https://dash.plotly.com/layout on 24/05/2021
# Import section modified 10/10/2021 to comply with changes in the Dash library.

# Run this app with `python dash_app.py` and visit http://127.0.0.1:8050/ in your web browser.

from doctest import OutputChecker
import dash, create_charts
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from pathlib import Path
from dash import Dash, dcc, html, Input, Output

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])


DATA_PATH = Path(__file__).parent.joinpath('data')


viz_bubble_chart = create_charts.results_bubble()[0]
viz_polar_chart = create_charts.comparisons_polar()
df_User = create_charts.results_bubble()[1]

app.layout = dbc.Container(
    [
        html.H1("NetPix"),
        html.Br(),
        html.H3(children=["Here's a list of movies that match your criteria"]),

        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='dropdown',
                    options=[df_User['Titles']],

                ),
            ]),

            dbc.Col([
                dcc.Graph(
                id='bubble-chart',
                figure=viz_bubble_chart
                )
                
            
            ])

        ]),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                id = 'polar-chart',
                figure=viz_polar_chart
                )
            
            ])

        ]),
        

        
    ],
    fluid=True,
)

@app.callback(
    Output(component_id='polar-chart', component_property='figure'),
    Input(component_id='dropdown', component_property='value')
)

def update_output(input):
    return

if __name__ == '__main__':
    app.run_server(debug=True, port=8888)


# Copied from the Dash tutorial documentation at https://dash.plotly.com/layout on 24/05/2021
# Import section modified 10/10/2021 to comply with changes in the Dash library.

# Run this app with `python dash_app.py` and visit http://127.0.0.1:8050/ in your web browser.

import dash, create_charts
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from pathlib import Path
from dash import dcc
from dash import html

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])


DATA_PATH = Path(__file__).parent.joinpath('data')


viz_bubble_chart = create_charts.results_bubble()
viz_chloro_medals = create_charts.choropleth_medal_dist()

app.layout = dbc.Container(
    [
        html.H1("NetPix"),
        html.Br(),
        html.H3(children=["Here's a list of movies that match your criteria"]),

        dcc.Graph(
            id='bubble-chart',
            figure=viz_bubble_chart
        ),

        dcc.Graph(
            id = 'chloro_medals',
            figure=viz_chloro_medals
        )
    ],
    fluid=True,
)

if __name__ == '__main__':
    app.run_server(debug=True, port=8888)


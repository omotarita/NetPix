from doctest import OutputChecker
from click import style
import dash
import pandas as pd, plotly.graph_objs as go, dash_bootstrap_components as dbc
from pathlib import Path
from dash import Dash, dcc, html, Input, Output, State
from cmath import nan

external_stylesheets = [Path(__file__).parent.parent.joinpath('static/assets', 'custom.css'), dbc.themes.BOOTSTRAP]
MY_SAVED_PREFS_FILEPATH = Path(__file__).parent.parent.parent.joinpath('data', 'my_saved_prefs.csv')
MY_BLENDS_FILEPATH = Path(__file__).parent.parent.parent.joinpath('data', 'my_blends.csv')


genre_list = ['Action','Adventure','Animation','Comedy','Crime','Documentary','Drama','Family','Fantasy','History','Horror','Music','Mystery','Science-Fiction','Romance','Thriller','TV Movie','War','Western']
df = pd.read_csv(MY_SAVED_PREFS_FILEPATH)
df2 = pd.read_csv(MY_BLENDS_FILEPATH)
saved_preference_list = df['tag'].to_list()
blend_list = df2['tag'].to_list()
i = 0
while i<len(blend_list):
    saved_preference_list.insert(len(saved_preference_list), blend_list[i])
    i=i+1


layout = html.Div(style={'background-color': '#141414'}, children=[
    dbc.Container([

            dcc.Store(id='hidden-store', storage_type='memory'),
            dcc.Store(id='preference-store', storage_type='memory'),
            dcc.Store(id='saved-pref-store', storage_type='memory'),
            dbc.Row([
                html.Div(style={'text-align': 'center'}, children=[
                    html.Br(),
                    html.Img(id='logo', width=300, src="assets/images/logo.png"),
                    ]) 
                ]),
            html.Br(),
            html.Br(),
            html.Br(),
            dbc.Row([
                html.Div(style={'text-align': 'center'}, children=[
                    html.H3(children=["What are your preferences?"], style={'color': '#FFFFFF', 'font-family': 'Helvetica Neue', 'font-size': '26px' , 'opacity': '0.7'}),
                ])
            ]),
            html.Br(),
            dbc.Row([
                dcc.Dropdown(
                        id='genre-dropdown',
                        options=[{'label': x, 'value': x} for x in genre_list],
                        placeholder='Select your preferred genres (we recommend picking at least 3)',
                        multi=True
                        ),
                ]),
            html.Br(),
            html.Br(),
            dbc.Row([
                dcc.Slider(min=0, marks=None, max=360, step=5,
                    value=150,
                    tooltip={"placement": "bottom", "always_visible": True}, 
                    id='runtime-slider'
                    ),
                html.Div(id='slider-output-container')
                ]),
            html.Br(),
            dbc.Row([
                dbc.Col(width=6, children=[
                    html.H5(children=["Reuse Saved Preferences?"], style={'color': '#FFFFFF', 'font-family': 'Helvetica Neue', 'font-size': '26px' , 'opacity': '0.7'}),
                    dcc.Dropdown(
                        id='saved-pref-dropdown',
                        options=[{'label': x, 'value': x} for x in saved_preference_list],
                        placeholder='Select...',
                        multi=False
                    ),
                ]),
                dbc.Col(width=6, children=[
                    html.H5(children=["Save Your Preferences?"], style={'color': '#FFFFFF', 'font-family': 'Helvetica Neue', 'font-size': '26px' , 'opacity': '0.7'}),
                    dbc.Row([
                        dbc.Col(width=4, children=[
                            dcc.Input(id="tag-input", type="text", placeholder="Tag", style={'marginRight':'10px'}),
                            dcc.Input(id="username-input", type="text", placeholder="Username"),
                        ]),
                        dbc.Col(width=2, children=[
                            html.Button('Save', id='save-prefs'),
                            html.Div(id='save-success-output-container')
                        ]),

                    ]),
                    dbc.Row([

                    ]), 
                ]),
            ]),
            html.Br(),
            html.Br(),
            html.H3(children=["Here's a list of movies that match your preferences"]),
            html.Br(),
            dbc.Row([
                dbc.Col(width=4, children=[
                    dcc.Dropdown(
                        id='movie-dropdown',
                        placeholder='Pick a movie'
                        ),
                    html.Div(id='description-box', style={'text-align': 'center'}, children=[
                        html.Br(),
                        html.H2(id='header', children={}),
                        html.A(id='match', style={'font-size': '18px', 'color': '#d3d3d3'}, children={}),
                        html.Br(),
                        html.A(id='text', style={'font-size': '16.5px'}, children={}),
                        html.Br(),
                        html.Br(),
                        html.Img(id='poster', width=450, src="https://www.colorhexa.com/141414.png")
                        ])       
                    ]),
                dbc.Col(width=8, children=[
                    dbc.Row([
                        dcc.Graph(
                            id='bubble-chart',
                            figure={}
                            )
                        ]),
                    html.Br(),
                    dbc.Row([
                        dcc.Graph(
                            id = 'polar-chart',
                            figure={}
                            )
                        ])
                    ])
            ]),
        ],
    fluid=True,
    ),
])

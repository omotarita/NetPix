from doctest import OutputChecker
import dash, json, math, numpy
import pandas as pd, plotly.express as px, plotly.graph_objs as go
import dash_bootstrap_components as dbc
from pathlib import Path
from dash import Dash, dcc, html, Input, Output, State
from cmath import nan
from flask import redirect

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])


DATA_PATH = Path(__file__).parent.joinpath('data')
MOVIE_DATA_FILEPATH = Path(__file__).parent.joinpath('data', 'updated_complete_data.csv')
genre_list = ['Action','Adventure','Animation','Comedy','Crime','Documentary','Drama','Family','Fantasy','History','Horror','Music','Mystery','Science-Fiction','Romance','Thriller','TV Movie','War','Western']


#viz_bubble_chart = results_bubble()[0]
#viz_polar_chart = comparisons_polar(input)


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
                    placeholder='Select your preferred genres (we recommend picking at least 3)',
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

        html.H3(children=["Here's a list of movies that match your preferences"]),


        dbc.Row([
            dbc.Col(width=4, children=[
                dcc.Dropdown(
                    id='movie-dropdown',
                    #doesn't look like dropdown is showing all the options/nor even the right options. change df_User to df from results_bubble and check again
                    options={},
                    #options=[{'label': x, 'value': x} for x in {}],
                    value='Happy Feet',
                    placeholder='Pick a movie'

                ),
                
            ]),

            dbc.Col(width=8, children=[
                dcc.Graph(
                id='bubble-chart',
                figure={}
                )
                
            
            ])

        ]),

        dbc.Row([

            dbc.Col([
                html.Div(id='description-box', style={'text-align': 'center'}, children=[
                    html.H2(id='header', children={}),
                    html.A(id='text', children={}),
                    html.Br(),
                    html.Br(),
                    html.Img(id='poster', width=500, src="https://cdn.vox-cdn.com/thumbor/Yq1Vd39jCBGpTUKHUhEx5FfxvmM=/39x0:3111x2048/1200x800/filters:focal(39x0:3111x2048)/cdn.vox-cdn.com/uploads/chorus_image/image/49901753/netflixlogo.0.0.png")

                ])
            ]),

            dbc.Col([
                dcc.Graph(
                id = 'polar-chart',
                figure={}
                )
            
            ])

        ]),
        

        
    ],
    fluid=True,
)

@app.callback(
    [Output('slider-output-container', 'children'), Output('bubble-chart', 'figure'), Output('movie-dropdown', 'options')],
    [Input('runtime-slider', 'value'), Input('genre-dropdown', 'value')]
)
def update_user(time_value, genre_value):
    """
    Takes input from user's preferences and adapts the dataset accordingly to show user's results

    :parameter data: user's input, the movie dataset (updated_complete_data.csv)
    :type: DataFrame
    :return: DataFrame
    """

    df_movies = pd.read_csv(MOVIE_DATA_FILEPATH)

    #These lines of code should be made interactive
    #genre_prefs_User = ["Adventure", "Comedy", "Family", "Drama"]
    genre_prefs_User = genre_value

    hours = time_value//60
    minutes= time_value - (hours*60)

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

    genre_adherence = []
    hover_text = []
    match = []
    newline = '\n'
    n = 0

    while n < len(df_movies):
        genre_scoresheet = [0,0,0,0]

        if df_movies['Genre 1'].iloc[n] in (genre_prefs_User):
            genre_scoresheet[0] = 1
        else:
            pass

        if df_movies['Genre 2'].iloc[n] in (genre_prefs_User):
            genre_scoresheet[1] = 1
        else:
            pass
        
        if df_movies['Genre 3'].iloc[n] in (genre_prefs_User):
            genre_scoresheet[2] = 1
        else:
            pass

        if df_movies['Genre 4'].iloc[n] in (genre_prefs_User):
            genre_scoresheet[3] = 1
        else:
            pass
    
        genre_score = sum(genre_scoresheet)

        # Match formula adapted from Netflix's own percent match score and formulae developed for a thesis 
        # titled 'Learning about Media Users from Movie Rating Data' (More information on these available 
        # at: https://help.netflix.com/en/node/9898 and https://dspace.mit.edu/bitstream/handle/1721.1/129200/1227275102-MIT.pdf?sequence=1&isAllowed=y)

        match_score = ((df_movies['Average Vote (/10)'].iloc[n]*((genre_score ** 0.7)/(len(genre_prefs_User) ** 0.7)) / (10*(1 ** 0.7))) ** 0.3) * 100
        # 0.7 represents the weighting of genre adherence towards a user's match score for a particular movie. 
        # 0.3 represents the weighting of the movie's average vote

        match.insert(n, math.trunc(match_score))
        genre_adherence.insert(n, (genre_score ** 0.7)/(len(genre_prefs_User) ** 0.7))
        
        if df_movies['Tagline'].iloc[n] == nan:
            hover_text.insert(n, f"{df_movies['Title'].iloc[n]}{chr(10)}{match[n]}% match!{newline}Average Vote:{df_movies['Average Vote (/10)'].iloc[n]}{newline}Popularity:{df_movies['Popularity'].iloc[n]}{newline}Runtime:{df_movies['Runtime (minutes)'].iloc[n]}")
        else:
            hover_text.insert(n, f"{df_movies['Title'].iloc[n]}{chr(10)}{df_movies['Tagline'].iloc[n]}{newline}{match[n]}% match!{newline}Average Vote:{df_movies['Average Vote (/10)'].iloc[n]}{newline}Popularity:{df_movies['Popularity'].iloc[n]}{newline}Runtime:{df_movies['Runtime (minutes)'].iloc[n]}")

        n +=1

    df_movies['Genre Preference Adherence'] = genre_adherence
    df_movies['Hover Description'] = hover_text
    df_movies['Percent Match Score'] = match
  
    df_User = df_movies[(df_movies['Runtime (minutes)'] < time_value) & (df_movies['Popularity'] > 3) & (df_movies['Percent Match Score'] > 55)]
    df_User = df_User.sample(frac = 1)[0:int(0.2*len(df_User))]
    #df_User = df_User[0:int(0.2*len(df_User))]
    df_User = remove_outliers(df_User)

    viz = results_bubble(df_User)[0]

    movie_options = df_User['Title']
    movie_options.tolist()
    
    return time, viz, movie_options

@app.callback(
    [Output('polar-chart', 'figure'), Output('header', 'children'), Output('text', 'children'), Output('poster', 'src')],
    Input('movie-dropdown', 'value')
)
def update_selection(input):
    viz = comparisons_polar(input)[0]
    title = movie_box(input)[0]
    overview = movie_box(input)[1]
    poster = str(movie_box(input)[2])
    return viz, title, overview, poster



def remove_outliers(df):
    '''
    Function to remove outliers from dataset to improve the clarity of the eventual data visualisation
    '''

    stdPopularity = df['Popularity'].std()
    meanPopularity = df['Popularity'].mean()
    stdAvgVote = df['Average Vote (/10)'].std()
    meanAvgVote = df['Average Vote (/10)'].mean()

    maxPop = meanPopularity+(1.5*stdPopularity)
    minPop = meanPopularity-(1.5*stdPopularity)
    maxVote = meanAvgVote+(1.5*stdAvgVote)
    minVote = meanAvgVote-(1.5*stdAvgVote)

    df = df[(df['Average Vote (/10)'] > minVote) & (df['Average Vote (/10)'] < maxVote)]
    df = df[(df['Popularity'] > minPop) & (df['Popularity'] < maxPop)]

    return df

def results_bubble(df_User):
    """
    Takes the movie dataset prepared in COMP0035 and creates a bubble chart by using the Plotly Graph Objects Scatter function and making the 
    marker size variable

    :parameter data: the movie dataset (updated_complete_data.csv)
    :type data: DataFrame
    :return: None
    """

    # Adapted from code published in the Plotly documentation (Available from: https://plotly.com/python/bubble-charts/)
    size = 3.5 ** (df_User['Percent Match Score']/10)

    viz = go.Figure(data=[go.Scatter(
                          x=df_User['Popularity'],
                          y=df_User['Average Vote (/10)'],
                          mode='markers',
                          hovertext=df_User['Hover Description'],
                          hoverinfo= 'text',

                          marker=dict(
                            size=size,
                            sizemode="area",
                            sizeref=2.*(max(size)/2)/(60.**2),
                            sizemin = 10,
                            color=df_User['Genre Preference Adherence'],
                            colorscale=[(0,"#e50914"), (1,"#b20710")],
                            #opacity=0.5,
                            line=dict(width=2,
                                        color='antiquewhite')                            
                            
                          )
    )])

    return viz, df_User

def comparisons_polar(selection):
    #movie_selection = user()[1]
    #movie_selection = selection

    df_User = update_user()[2]

    selection_index = df_User.index[df_User['Title']==selection].tolist()[0]
    selection_matchp = df_User.loc[selection_index,'Percent Match Score']

    #df_Similar = df_User[(df_User['Percent Match Score'] > (selection_matchp-3)) & (df_User['Percent Match Score'] < (selection_matchp+3))][0:2]
    #df_Similar should be gotten from results_bubble but using the genres of the selection as the input  
    df_Similar = df_User[(df_User['Percent Match Score'] > (selection_matchp-3)) & (df_User['Percent Match Score'] < (selection_matchp+3))].sample(frac = 1)
    df_Similar = df_Similar[0:2]
    df_Optimal = df_User.sort_values(by='Percent Match Score', ascending=False)[0:1]
    #df_Optimal = df_User.sort_values(by='Percent Match Score', ascending=False).sample(frac = 1)
    #df_Optimal = df_Optimal[0:1]


    cols = ['Title', 'Popularity', 'Average Vote (/10)', 'Genre Preference Adherence']
    s1 = [selection, df_User.loc[selection_index,'Popularity'], df_User.loc[selection_index,'Average Vote (/10)']*10, (df_User.loc[selection_index,'Genre Preference Adherence'])*100]
    s2 = [df_Similar.iloc[0]['Title'], df_Similar.iloc[0]['Popularity'], df_Similar.iloc[0]['Average Vote (/10)']*10, (df_Similar.iloc[0]['Genre Preference Adherence'])*100]
    s3 = [df_Similar.iloc[1]['Title'], df_Similar.iloc[1]['Popularity'], df_Similar.iloc[1]['Average Vote (/10)']*10, (df_Similar.iloc[1]['Genre Preference Adherence'])*100]
    s4 = [df_Optimal.iloc[0]['Title'], df_Optimal.iloc[0]['Popularity'], df_Optimal.iloc[0]['Average Vote (/10)']*10, (df_Optimal.iloc[0]['Genre Preference Adherence'])*100]
    s5 = ['Average', df_User['Popularity'].mean(), df_User['Average Vote (/10)'].mean()*10, (df_User['Genre Preference Adherence'].mean())*100]

    comparisons = [s1, s2, s3, s4, s5]
    df_Comparisons = pd.DataFrame(comparisons, columns=cols)

    # Adapted from code published in the Plotly documentation (Available from: https://plotly.com/python/wind-rose-charts/) 
    viz = go.Figure()

    viz.add_trace(go.Barpolar(
        r=df_Comparisons['Popularity'],
        name='Popularity',
        marker_color='#e50914'
    ))
    viz.add_trace(go.Barpolar(
        r=df_Comparisons['Average Vote (/10)'],
        name='Average Vote (/10)',
        marker_color='#b20710'
    ))
    viz.add_trace(go.Barpolar(
        r=df_Comparisons['Genre Preference Adherence'],
        name='Genre Preference Adherence',
        marker_color='#000000'
    ))

    viz.update_traces(text=df_Comparisons['Title'])
    viz.update_layout(
        title='See how your chosen movie compares to similar options',
        font_size=16,
        legend_font_size=16,
        #polar_radialaxis_ticksuffix='%',
        polar_angularaxis_rotation=90,

    )

    #remove hover details, remove wind details, remove all numbers tbh

    return viz, selection_index

def movie_box(selection):
    title = selection
    selection_index = df_User.index[df_User['Title']==selection].tolist()[0]
    overview = df_User.loc[selection_index,'Overview']
    poster_link = f"https://image.tmdb.org/t/p/w500{df_User.loc[selection_index,'Poster Path']}"

    print(poster_link)

    return title, overview, poster_link


if __name__ == '__main__':
    app.run_server(debug=True, port=8888)


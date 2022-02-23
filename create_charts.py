# Helper functions for creating the charts in the activities
from flask import redirect
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from pathlib import Path
import json
from pathlib import Path


MOVIE_DATA_FILEPATH = Path(__file__).parent.joinpath('data', 'updated_complete_data.csv')


def results_bubble():
    """
    Takes the movie dataset prepared in COMP0035 and creates a bubble chart by using the plotly express scatter function and making the 
    mark size variable

    :parameter data: the movie data set (updated_complete_data.csv)
    :type data: DataFrame
    :return: None
    """
    
    df_movies = pd.read_csv(MOVIE_DATA_FILEPATH)

    #These two lines of code should be made interactive
    genre_prefs_User = ["Adventure", "Comedy", "Family", "Romance"]
    runtime_prefs_User = 130

    df_User = df_movies[(df_movies['Runtime (minutes)'] < runtime_prefs_User) & (df_movies['Popularity'] > 3)]

    g1_col = df_User['Genre 1']
    g2_col = df_User['Genre 2']
    title_col = df_User['Title']
    tag_col = df_User['Tagline']
    vote_col = df_User['Average Vote (/10)']
    pop_col = df_movies['Popularity']
    run_col = df_User['Runtime (minutes)']


    genre_adherence = []
    hover_text = []
    newline = '\n'



    n = 0

    while n < len(df_User):
        hover_text.insert(n, f"{title_col.iloc[n]}{chr(10)}{tag_col.iloc[n]}{newline}Average Vote:{vote_col.iloc[n]}{newline}Popularity:{pop_col.iloc[n]}{newline}Runtime:{run_col.iloc[n]}")

        if g1_col.iloc[n] in (genre_prefs_User):
            if g2_col.iloc[n] in (genre_prefs_User):
                genre_score = 2
            else:
                genre_score = 1
        elif g2_col.iloc[n] in (genre_prefs_User):
            genre_score = 1
        else:
            genre_score = 0
        
        genre_adherence.insert(n, genre_score)
        n +=1

    df_User['Genre Preference Adherence'] = genre_adherence
    adherence_col = df_User['Genre Preference Adherence']
    df_User['Hover Description'] = hover_text
    hover_col = df_User['Hover Description']

    #genre_colors = {'Action': ,'Adventure': ,'Animation': ,'Comedy': ,'Crime': ,'Documentary': ,'Drama': ,'Family': , 'Fantasy': ,'History': ,'Horror': ,'Music': ,'Mystery': ,'Science-Fiction': ,'Romance': ,'Thriller': ,'TV Movie': ,'War': ,'Western': }

    df_User = df_User.sort_values(by='Popularity', ascending=False)
    df_User = df_User[0:100]
    #df_User = df_User.sort_values(by='Genre Preference Adherence', ascending=False)
    #df_User[~df_User['Genre Preference Adherence'] < 1]

    
    #Adapted from code written by __ for thisPointer (Available from: https://thispointer.com/python-pandas-how-to-drop-rows-in-dataframe-by-conditions-on-column-values/) 
    # and code published on DelftStack (Available from: https://www.delftstack.com/howto/python-pandas/pandas-get-index-of-row/)
    genre_columns = ["Genre 1", "Genre 2"]
    #ind_list = list(df_User.index.values)
    #ind_list = []
    #genre_adherence = []
    #i = 0

    #df_User([df_User["Genre 1"].isin(genre_prefs_User)] | [df_User["Genre 2"].isin(genre_prefs_User)])


    #swap runtime to genre-adherence later

    df_User['Runtime (minutes)'] = df_User['Runtime (minutes)'].astype(str)
    df_User['Runtime (minutes)'] = df_User['Runtime (minutes)'].astype(float)
    df_User['Runtime (minutes)'] = pd.to_numeric(df_User['Runtime (minutes)'], downcast='float')
    df_User['Runtime (minutes)'] = df_User['Runtime (minutes)'].astype(int)

    print(df_User)

    # px line charts https://plotly.com/python/line-charts/
    # Styling figures with px https://plotly.com/python/styling-plotly-express/

    # Adapted from code published in the Plotly documentation (Available from: https://plotly.com/python/bubble-charts/)

    size = 4 ** df_User['Genre Preference Adherence']
    text = df_User['Title'], df_User['Tagline'], df_User['Average Vote (/10)'], df_User['Popularity'], df_User['Runtime (minutes)']

    viz = go.Figure(data=[go.Scatter(
                          x=vote_col,
                          y=pop_col,
                          mode='markers',
                          hovertext=hover_col,
                          hoverinfo= 'text',
                          
                          #labels={'Average Vote (/10)': 'Average Vote (/10)', 'Popularity': 'Popularity'},

                          #hover_name=df_User['Title'],
                          #hover_data=["Title", "Tagline", "Average Vote (/10)", "Popularity", "Runtime (minutes)"],
                          #template="simple_white",

                          marker=dict(
                            size=size,
                            sizemode="area",
                            sizeref=2.*(max(size)/2)/(60.**2),
                            sizemin = 10,
                            color='darkred',
                            opacity=0.5,
                            line=dict(width=2,
                                        color='antiquewhite')
                            #title='Have the number of events changed over time?',
                            
                            
                          )#colour should correspond with genre 1
    )])

    return viz


def choropleth_medal_dist():
    #How many medals did each country win in the 2012 London Summer Olympics?

 
    return

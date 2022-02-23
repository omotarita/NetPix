# Helper functions for creating the charts in the activities
from flask import redirect
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from pathlib import Path
import json
import math
from pathlib import Path


MOVIE_DATA_FILEPATH = Path(__file__).parent.joinpath('data', 'updated_complete_data.csv')

def user():
    """
    Takes input from user's preferences and adapts the dataset accordingly to show user's results

    :parameter data: user's input, the movie dataset (updated_complete_data.csv)
    :type: DataFrame
    :return: DataFrame
    """

    df_movies = pd.read_csv(MOVIE_DATA_FILEPATH)

    #These lines of code should be made interactive
    genre_prefs_User = ["Adventure", "Comedy", "Family", "Drama"]
    runtime_prefs_User = 130

    movie_selection = 'The Life Aquatic with Steve Zissou'

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
        
        hover_text.insert(n, f"{df_movies['Title'].iloc[n]}{chr(10)}{df_movies['Tagline'].iloc[n]}{newline}{match[n]}% match!{newline}Average Vote:{df_movies['Average Vote (/10)'].iloc[n]}{newline}Popularity:{df_movies['Popularity'].iloc[n]}{newline}Runtime:{df_movies['Runtime (minutes)'].iloc[n]}")

        n +=1

    df_movies['Genre Preference Adherence'] = genre_adherence
    #adherence_col = df_movies['Genre Preference Adherence']
    df_movies['Hover Description'] = hover_text
    #hover_col = df_movies['Hover Description']
    df_movies['Percent Match Score'] = match
    #print(len(match))
    #match_col = 

    
    df_User = df_movies[(df_movies['Runtime (minutes)'] < runtime_prefs_User) & (df_movies['Popularity'] > 3)]
    
    return df_User, movie_selection

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


    #remove certain values from dataframe
    df = df[(df['Average Vote (/10)'] > minVote) & (df['Average Vote (/10)'] < maxVote)]
    df = df[(df['Popularity'] > minPop) & (df['Popularity'] < maxPop)]


    #remove rows with empty 
    #df = df.dropna(axis=0, how='any')

    return df

def results_bubble():
    """
    Takes the movie dataset prepared in COMP0035 and creates a bubble chart by using the Plotly Graph Objects Scatter function and making the 
    marker size variable

    :parameter data: the movie dataset (updated_complete_data.csv)
    :type data: DataFrame
    :return: None
    """

    df_User = user()[0]
    
    #genre_colors = {'Action': ,'Adventure': ,'Animation': ,'Comedy': ,'Crime': ,'Documentary': ,'Drama': ,'Family': , 'Fantasy': ,'History': ,'Horror': ,'Music': ,'Mystery': ,'Science-Fiction': ,'Romance': ,'Thriller': ,'TV Movie': ,'War': ,'Western': }

    # Considering only the top 25% of matches
    #df_User = df_User.sort_values(by='Percent Match Score', ascending=False)
    df_User = df_User[df_User['Percent Match Score'] > 55]

    df_User = df_User.sample(frac = 1)
    df_User = df_User[0:int(0.2*len(df_User))]

    #df_User = df_User.sort_values(by='Genre Preference Adherence', ascending=False)
    #df_User[~df_User['Genre Preference Adherence'] < 1]

    # Then removing any outliers
    df_User = remove_outliers(df_User)

    print(df_User)


    # Adapted from code published in the Plotly documentation (Available from: https://plotly.com/python/bubble-charts/)

    size = 3.5 ** (df_User['Percent Match Score']/10)
    #text = df_User['Title'], df_User['Tagline'], df_User['Average Vote (/10)'], df_User['Popularity'], df_User['Runtime (minutes)']

    viz = go.Figure(data=[go.Scatter(
                          x=df_User['Popularity'],
                          y=df_User['Average Vote (/10)'],
                          mode='markers',
                          hovertext=df_User['Hover Description'],
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
                            color=df_User['Genre Preference Adherence'],
                            colorscale=[(0,"#e50914"), (1,"#b20710")],
                            #opacity=0.5,
                            line=dict(width=2,
                                        color='antiquewhite')                            
                            
                          )
    )])

    return viz, df_User


def choropleth_medal_dist():
    #How many medals did each country win in the 2012 London Summer Olympics?

    movie_selection = user()[1]
    df_User = results_bubble()[0]

    selection_index = df_User.index[df_User['Title']==movie_selection

    comparisons = []

    # Movie Selection Popularity Avg Vote Genre Preference Adherence
    # Similar Match Popularity Avg Vote GPA
    # Similar Match Popularity Avg Vote GPA
    # Better Match POpylarity Avg Vote GPA
    # Better Match POpularity Avg Vote GPA
    # Avg AvgPopularity Avg(Avg Vote) AvgGPA

    x=df_User['Popularity'],
    y=df_User['Average Vote (/10)'],
    color=df_User['Genre Preference Adherence'],

    ]





 
    return

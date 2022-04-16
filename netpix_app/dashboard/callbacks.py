import dash, math
from dash import Dash, dcc, html, Input, Output, State
from pathlib import Path
import pandas as pd, plotly.graph_objs as go, dash_bootstrap_components as dbc

#external_stylesheets = [Path(__file__).parent.parent.joinpath('static/assets', 'custom.css'), dbc.themes.BOOTSTRAP]

DATA_PATH = Path(__file__).parent.joinpath('data')
MOVIE_DATA_FILEPATH = Path(__file__).parent.parent.parent.joinpath('data', 'updated_complete_data.csv')

def register_callbacks(dash_app):
    '''Function to register all the callbacks for my Dash app'''
    @dash_app.callback(
        [Output('hidden-store', 'hidden'), Output('slider-output-container', 'children'), Output('bubble-chart', 'figure'), Output('movie-dropdown', 'options')],
        [Input('runtime-slider', 'value'), Input('genre-dropdown', 'value')]
    )
    def update_user(time_value, genre_value):
        """
        Takes input from user's preferences and calls on the generate_dataset function to adapt the dataframe accordingly to show user's results.
        Also produces a string verifying to the user the amount of time they've chosen

        :parameter data: user's input, the movie dataset (updated_complete_data.csv)
        :type: int, list
        :return: DataFrame, str, fig, list
        """
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

        df_User = generate_dataframe(genre_prefs_User, time_value)
        bubble = results_bubble(df_User)

        movie_options = df_User['Title'].tolist()

        test_options = [{'label': i,'value': i} for i in df_User['Title'].tolist()]

        df_User = df_User.to_json()

        return df_User, time, bubble, test_options

    @dash_app.callback(
        [Output('polar-chart', 'figure'), Output('header', 'children'), Output('match', 'children'), Output('text', 'children'), Output('poster', 'src')],
        Input('movie-dropdown', 'value'),
        State('hidden-store', 'hidden')
    )
    def update_selection(input, data):
        """
        Takes input from user's movie selection and calls on the relevant helper functions to generate a polar bar chart comparing it with
        other alternative options and to gather the data required to update its description box

        :parameter data: user's input, data
        :type: str, DataFrame
        :return: Figure, str, str, str
        """
        df_User = pd.read_json(data)

        fig = comparisons_polar(input, df_User)
        title = movie_box(input, df_User)[0]
        match = f"{str(movie_box(input, df_User)[1])}% match"
        overview = movie_box(input, df_User)[2]
        poster = str(movie_box(input, df_User)[3])

        return fig, title, match, overview, poster

    def generate_dataframe(pref_genres, pref_time):
        '''
        Takes the input of user's genre and time preferences and finds movies that match these from the complete movie dataset prepared 
        in COMP0035 (see data/updated_complete_dataset.csv). Creates and returns a new dataframe containing these matches, the degree to which they are a match
        (Percent Match Score), their adherence to the user's given genre preferences (Genre Preference Adherence) and a small amount of
        contextual information on the movie, to be used, if needed, in future data visualisations (Hover Text)

        :parameter data: pref_genres, pref_time
        :type data: list, int
        :return: DataFrame
        '''

        df_movies = pd.read_csv(MOVIE_DATA_FILEPATH)
        genre_adherence = []
        hover_text = []
        match = []
        newline = '\n'
        n = 0

        while n < len(df_movies):
            genre_scoresheet = [0,0,0,0]
            if df_movies['Genre 1'].iloc[n] in (pref_genres):
                genre_scoresheet[0] = 1
            else:
                pass
            if df_movies['Genre 2'].iloc[n] in (pref_genres):
                genre_scoresheet[1] = 1
            else:
                pass
            if df_movies['Genre 3'].iloc[n] in (pref_genres):
                genre_scoresheet[2] = 1
            else:
                pass
            if df_movies['Genre 4'].iloc[n] in (pref_genres):
                genre_scoresheet[3] = 1
            else:
                pass
        
            genre_score = sum(genre_scoresheet)

            # Match formula adapted from Netflix's own percent match score and formulae developed for a thesis 
            # titled 'Learning about Media Users from Movie Rating Data' (More information on these available 
            # at: https://help.netflix.com/en/node/9898 and https://dspace.mit.edu/bitstream/handle/1721.1/129200/1227275102-MIT.pdf?sequence=1&isAllowed=y)
            match_score = ((df_movies['Average Vote (/10)'].iloc[n]*((genre_score ** 0.7)/(len(pref_genres) ** 0.7)) / (10*(1 ** 0.7))) ** 0.3) * 100

            match.insert(n, math.trunc(match_score))
            genre_adherence.insert(n, (genre_score ** 0.7)/(len(pref_genres) ** 0.7))
            
            if type(df_movies['Tagline'].iloc[n]) != str :
                hover_text.insert(n, f"{df_movies['Title'].iloc[n]}{chr(10)}{match[n]}% match!{chr(10)}Average Vote:{df_movies['Average Vote (/10)'].iloc[n]}{chr(10)}Popularity:{df_movies['Popularity'].iloc[n]}{chr(10)}Runtime:{df_movies['Runtime (minutes)'].iloc[n]}")
            else:
                hover_text.insert(n, f"{df_movies['Title'].iloc[n]}{chr(10)}{df_movies['Tagline'].iloc[n]}{chr(10)}{match[n]}% match!{chr(10)}Average Vote:{df_movies['Average Vote (/10)'].iloc[n]}{chr(10)}Popularity:{df_movies['Popularity'].iloc[n]}{chr(10)}Runtime:{df_movies['Runtime (minutes)'].iloc[n]}")

            n +=1

        df_movies['Genre Preference Adherence'] = genre_adherence
        df_movies['Hover Description'] = hover_text
        df_movies['Percent Match Score'] = match
    
        df_User = df_movies[(df_movies['Runtime (minutes)'] < pref_time) & (df_movies['Popularity'] > 3) & (df_movies['Percent Match Score'] > 55)]
        df_User = df_User.sample(frac = 1)[0:int(0.2*len(df_User))]
        df_User = remove_outliers(df_User)

        return df_User

    def remove_outliers(df):
        '''
        Function to remove outliers from dataset to improve the clarity of the eventual data visualisation

        :parameter data: df
        :type data: DataFrame
        :return: DataFrame
        '''

        sdevPopularity = df['Popularity'].std()
        meanPopularity = df['Popularity'].mean()
        sdevVote = df['Average Vote (/10)'].std()
        meanVote = df['Average Vote (/10)'].mean()

        maxPop = meanPopularity+(1.5*sdevPopularity)
        minPop = meanPopularity-(1.5*sdevPopularity)
        maxVote = meanVote+(1.5*sdevVote)
        minVote = meanVote-(1.5*sdevVote)

        df = df[(df['Average Vote (/10)'] > minVote) & (df['Average Vote (/10)'] < maxVote)]
        df = df[(df['Popularity'] > minPop) & (df['Popularity'] < maxPop)]
        return df

    def results_bubble(df):
        """
        Takes the movie dataset prepared in generate_dataframe() and creates a bubble chart by using the Plotly Graph Objects Scatter function and making the 
        marker size variable

        :parameter data: df
        :type data: DataFrame
        :return: Figure
        """

        # Adapted from code published in the Plotly documentation (Available from: https://plotly.com/python/bubble-charts/)
        size = 3.5 ** (df['Percent Match Score']/10)

        fig = go.Figure(data=[go.Scatter(
                            x=df['Popularity'],
                            y=df['Average Vote (/10)'],
                            mode='markers',
                            hovertext=df['Hover Description'],
                            hoverinfo= 'text',

                            marker=dict(
                                size=size,
                                sizemode="area",
                                sizeref=2.*(max(size)/2)/(60.**2),
                                sizemin = 10,
                                color=df['Genre Preference Adherence'],
                                colorscale=[(0,"#e50914"), (1,"#430206")],
                                colorbar={"title": 'Genre Preference Match'},
                                showscale=True,
                                opacity=1,
                                line=dict(width=2,
                                            color='antiquewhite')                            
                                
                            )
        )])

        fig.update_layout(
            title="Look for the biggest bubbles; their size corresponds to how close of an overall match they are",
            font_size=9,
            title_x=0.5,
            xaxis_title="Popularity",
            yaxis_title="Average Vote (/10)",
            legend_title="Legend Title",
            font=dict(
                family="Helvetica Neue",
                size=14,
                color="white"
                ),
            template = 'plotly_dark',
            paper_bgcolor='#141414',
            plot_bgcolor='#141414'
        )

        return fig 

    def comparisons_polar(selection, df):
        '''
        Takes the movie dataset prepared in generate_dataframe() and creates a stacked polar bar chart by using the Plotly Graph Objects Polar Bar function

        :parameter data: df
        :type data: str, DataFrame
        :return: Figure 
        '''
        selection_index = df.index[df['Title']==selection].tolist()[0]
        selection_matchp = df.loc[selection_index,'Percent Match Score']

        df_Similar = df[(df['Percent Match Score'] > (selection_matchp-3)) & (df['Percent Match Score'] < (selection_matchp+3))].sample(frac = 1)
        df_Similar = df_Similar[0:2]
        df_Optimal = df.sort_values(by='Percent Match Score', ascending=False)[0:1]

        cols = ['Title', 'Popularity', 'Average Vote (/10)', 'Genre Preference Adherence']
        s1 = [selection, df.loc[selection_index,'Popularity'], df.loc[selection_index,'Average Vote (/10)']*10, (df.loc[selection_index,'Genre Preference Adherence'])*100]
        s2 = [df_Similar.iloc[0]['Title'], df_Similar.iloc[0]['Popularity'], df_Similar.iloc[0]['Average Vote (/10)']*10, (df_Similar.iloc[0]['Genre Preference Adherence'])*100]
        s3 = [df_Similar.iloc[1]['Title'], df_Similar.iloc[1]['Popularity'], df_Similar.iloc[1]['Average Vote (/10)']*10, (df_Similar.iloc[1]['Genre Preference Adherence'])*100]
        s4 = [df_Optimal.iloc[0]['Title'], df_Optimal.iloc[0]['Popularity'], df_Optimal.iloc[0]['Average Vote (/10)']*10, (df_Optimal.iloc[0]['Genre Preference Adherence'])*100]
        s5 = ['Average', df['Popularity'].mean(), df['Average Vote (/10)'].mean()*10, (df['Genre Preference Adherence'].mean())*100]
        
        comparisons = [s1, s2, s3, s4, s5]
        df_Comparisons = pd.DataFrame(comparisons, columns=cols)

        # Adapted from code published in the Plotly documentation (Available from: https://plotly.com/python/wind-rose-charts/) 
        fig = go.Figure()
        fig.add_trace(go.Barpolar(
            r=df_Comparisons['Popularity'],
            theta=df_Comparisons['Title'],
            name='Popularity',
            marker_color='#e50914'
        ))
        fig.add_trace(go.Barpolar(
            r=df_Comparisons['Average Vote (/10)'],
            theta=df_Comparisons['Title'],
            name='Average Vote (/10)',
            marker_color='#b20710'
        ))
        fig.add_trace(go.Barpolar(
            r=df_Comparisons['Genre Preference Adherence'],
            theta=df_Comparisons['Title'],
            name='Genre Preference Match',
            marker_color='#550307'
        ))
        fig.update_traces(text=df_Comparisons['Title'])
        fig.update_layout(
            template = 'plotly_dark',
            paper_bgcolor='#141414',
            plot_bgcolor='#141414',
            title="This is how your current selection compares to some of your other recommendations",
            font_size=13,
            title_x=0.5,
            legend_font_size=11,
            polar_angularaxis_rotation=60,
            hovermode=None
        )
        fig.update_polars(angularaxis_showgrid=False)
        fig.update_polars(angularaxis_showline=False)
        fig.update_polars(radialaxis_showgrid=False)
        fig.update_polars(radialaxis_showline=False)
        fig.update_polars(radialaxis_showticklabels=False)

        return fig

    def movie_box(selection, df):
        '''
        Generates a description box for each movie, containing its title, a brief overview of its plot and its poster

        :parameter data: selection, df
        :type data: str, DataFrame
        :return: str, str, str
        '''
        title = selection
        selection_index = df.index[df['Title']==selection].tolist()[0]
        match_score = df.loc[selection_index,'Percent Match Score']
        overview = df.loc[selection_index,'Overview']
        poster_link = f"https://image.tmdb.org/t/p/w500{df.loc[selection_index,'Poster Path']}"

        return title, match_score, overview, poster_link

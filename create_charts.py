# Helper functions for creating the charts in the activities
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from pathlib import Path
import json
from pathlib import Path


MOVIE_DATA_FILEPATH = Path(__file__).parent.joinpath('data', 'updated_complete_data.csv')


def line_chart_sports():
    """
    Creates a line chart showing change in the number of sports in the summer and winter paralympics over time
    An example for exercise 1.

    TODO: Add checkbox to choose Winter, Summer or both (Lab 4 - interactivity)

    :return: Plotly Express line chart
    """
    cols = ['REF', 'TYPE', 'YEAR', 'LOCATION', 'EVENTS', 'SPORTS', 'COUNTRIES', 'MALE', 'FEMALE', 'PARTICIPANTS']
    df_events = pd.read_csv(EVENT_DATA_FILEPATH, usecols=cols)

    # px line charts https://plotly.com/python/line-charts/
    # Styling figures with px https://plotly.com/python/styling-plotly-express/
    line_events = px.line(df_events,
                          x='YEAR',
                          y='EVENTS',
                          color='TYPE',
                          text='YEAR',
                          title='Have the number of events changed over time?',
                          labels={'YEAR': '', 'EVENTS': 'Number of events', 'TYPE': ''},
                          template="simple_white"
                          )

    # Add an annotation https://plotly.com/python/text-and-annotations/
    line_events.add_annotation(
        text='Event in multiple locations, Stoke Mandeville and New York',
        x='1984',
        y=975,
        showarrow=True,
        arrowhead=2
    )

    # Remove the x-axis labels and tick lines
    line_events.update_xaxes(showticklabels=False, ticklen=0)

    return line_events


def choropleth_medal_dist():
    #How many medals did each country win in the 2012 London Summer Olympics?

    cols = ['Rank','Country','NPC','Total','Event','Year']
    df_medals = pd.read_csv(MEDALS_DATA_FILEPATH, usecols=cols)
    df_medals_event = df_medals[(df_medals['Event'] == 'London') & (df_medals['Year'] == '2012')]


    fig = px.choropleth_mapbox(df_medals_event,
                           geojson=df_geojson,
                           locations='NPC',
                           featureidkey="properties.ISO_A3",
                           color='Total')
    fig.show()

    return

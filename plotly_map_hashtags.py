"""CSC110 Project: Plotly Map: Key Phrases

Module Description
==================
The module plotly_map_hashtags:
    - appends dictionary processed from module keywords_plotly_data_points using
    hashtags_to_data_points to dictionary of hashtag and map
    - create a dash application of the dictionary and display it

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of Faizah Sayyid, Tina Zhang,
Poorvi Sharma, and Courtney Amm (students at the University of Toronto St. George campus).
All forms of distribution of this code, whether as given or with any changes, are expressly
prohibited.

This file is Copyright (c) 2020 Faizah Sayyid, Tina Zhang, Poorvi Sharma, and Courtney Amm.
"""
from typing import Dict, Any
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from keywords_plotly_data_points import hashtags_to_data_points
from rehydrate_and_filter_tweets import json_to_tweets

# TYPE IN THE PATH TO THE DOWNLOADED DATASET HERE:
DATA_SET_PROCESSED = ''
# TYPE IN THE NUMBER OF HASHTAGS YOU WANT THE MAP TO DISPLAY, AROUND 5 IS RECOMMENDED:
NUM_HASHTAGS = 5

TWEETS = json_to_tweets(DATA_SET_PROCESSED)
DATA = hashtags_to_data_points(TWEETS, NUM_HASHTAGS)
KEYS = list(DATA.keys())


def hashtag_to_map_dictionary() -> Dict[str, Any]:
    """Returns a dictionary of key phrase corresponding to the map"""
    animations = {}
    for value in KEYS:
        # filter out the hashtags that have empty dates, locations, or occurrences
        if DATA[value][0] != [] and DATA[value][1] != [] and DATA[value][2] != []:
            animations[value] = px.choropleth(locations=DATA[value][1],
                                              color=DATA[value][2],
                                              animation_frame=DATA[value][0],
                                              color_continuous_scale="Inferno",
                                              locationmode='USA-states',
                                              scope="usa",
                                              range_color=(0, max(DATA[value][2])),
                                              height=600
                                              )
        else:
            animations[value] = px.choropleth(color_continuous_scale="Inferno",
                                              locationmode='USA-states',
                                              scope="usa",
                                              title="Empty",
                                              height=600
                                              )
    return animations


# create an empty dash application and make the hashtag to map dictionary
APP = dash.Dash(__name__)
ANIMATIONS = hashtag_to_map_dictionary()

# configure the layout of the applications, add dropdowns
APP.layout = html.Div([
    html.P("Select a keyword:"),
    dcc.Dropdown(
        id='selection',
        options=[{'label': x, 'value': x} for x in ANIMATIONS],
        value=KEYS[0],
        placeholder="Select a key phrase"
    ),
    dcc.Graph(id="graph"),
    html.Div(id='dd-output-container')
])


@APP.callback(
    Output("graph", "figure"),
    [Input("selection", "value")])
def update_graph(input_data: str) -> Any:
    """Return and displays the map correspondent to the input from the dropdown.
    Displays an empty map if there's no input
    """
    if input_data is None:
        return px.choropleth(title="Awaiting Input...")
    else:
        return ANIMATIONS[input_data]


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['dash',
                          'dash_core_components',
                          'dash_html_components',
                          'dash.dependencies',
                          'plotly.express',
                          'keywords_plotly_data_points',
                          'rehydrate_and_filter_tweets'
                          ],  # the names (strs) of imported modules
        'allowed-io': ['update_graph',
                       'key_phrases_to_data_points',
                       'hashtag_to_map_dictionary'],
        # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
    APP.run_server(host='127.0.0.1', port=5050, debug=True)

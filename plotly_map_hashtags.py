"""CSC110 Project: Plotly Map: Key Phrases

Module Description
==================
This module contains the functions for finding all keywords in a list of tweets, and sorting them
based on the number of time they occur.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of Faizah Sayyid, Tina Zhang,
Poorvi Sharma, and Courtney Amm (students at the University of Toronto St. George campus).
All forms of distribution of this code, whether as given or with any changes, are expressly
prohibited.

This file is Copyright (c) 2020 Faizah Sayyid, Tina Zhang, Poorvi Sharma, and Courtney Amm.
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import keywords_plotly_data_points as sk
from rehydrate_and_filter_tweets import json_to_tweets

tweets = json_to_tweets()
data = sk.hashtags_to_data_points(tweets, 100)
keys = list(data.keys())


animations = {}
for value in keys:
    if data[value][0] != [] and data[value][1] != [] and data[value][2] != []:
        animations[value] = px.choropleth(locations=data[value][1],
                                          color=data[value][2],
                                          animation_frame=[str(date) for date in data[value][0]],
                                          color_continuous_scale="Inferno",
                                          locationmode='USA-states',
                                          scope="usa",
                                          range_color=(0, max(data[value][2])),
                                          height=600
                                          )
    else:
        animations[value] = px.choropleth(color_continuous_scale="Inferno",
                                          locationmode='USA-states',
                                          scope="usa",
                                          title="Empty",
                                          height=600
                                          )

app = dash.Dash(__name__)

app.layout = html.Div([
    html.P("Select a keyword:"),
    dcc.Dropdown(
        id='selection',
        options=[{'label': x, 'value': x} for x in animations],
        value=keys[1],
        placeholder="Select a key phrase"
    ),
    dcc.Graph(id="graph"),
    html.Div(id='dd-output-container')
])


@app.callback(
    Output("graph", "figure"),
    [Input("selection", "value")])
def update_graph(input_data):
    if input_data == None:
        px.choropleth(color_continuous_scale="Inferno",
                      locationmode='USA-states',
                      title="Empty",
                      scope="usa",
                      height=600)
    else:
        return animations[input_data]


if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=5050, debug=True)

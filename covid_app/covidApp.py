#!/usr/bin/env python
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output
import numpy as np
import json
from urllib.request import urlopen
from COVIDAppUtils import draw_plot
from decouple import config
from flask import Flask

# Path where covid cases timeseries is stored
COVID_CASES_PATH = config('COVID_CASES_PATH')
# Path where covid deaths timeseries is stored
COVID_DEATHS_PATH = config('COVID_DEATHS_PATH')
# path where the U.S. counties JSON file is stored
JSON_PATH = config('JSON_PATH')
HOST = config('HOST')
PORT = config('PORT')
DEBUG = config('DEBUG')


my_server = Flask(__name__)
my_app = Dash(__name__,server=my_server,
           external_stylesheets=[dbc.themes.DARKLY])



# Retrieve US counties JSON for visualization
with urlopen(JSON_PATH) as response:
    JSON = json.load(response)

df = pd.read_csv(COVID_CASES_PATH)
df_deaths = pd.read_csv(COVID_DEATHS_PATH)

# Data cleaning and wrangling
df.dropna(inplace=True)
df_deaths.dropna(inplace=True)
df_deaths.drop('Population', axis=1, inplace=True)

# FIPS is a county unique ID used in the JSON

df['FIPS'] = df['FIPS'].astype(int)
df['FIPS'] = df['FIPS'].apply('{0:0>5}'.format)

# Get day of first US covid case
first_date = df.columns[11:][0]

# Here I am assigning each date in the time series a raw day number
# i.e. 1/20/2020 -> day 1
# 1/21/2020 -> day 2 .... etc

columns = list(df.columns.values[11:])
columns_2 = np.arange(0, len(columns)).astype(str)
columns = df.columns.values
columns[11:] = columns_2
df.columns = columns
d_columns = list(df_deaths.columns.values[11:])
d_columns_2 = np.arange(0, len(d_columns)).astype(str)
d_columns = df_deaths.columns.values
d_columns[11:] = d_columns_2
df_deaths.columns = d_columns
ints_cols_2 = [int(x) for x in columns_2]

# -----------------------------------------------------------------------------------
# App layout

my_app.layout = html.Div(id="Base", children=[
    html.H1("Covid-19 Data Explorer By Week", style={'text-align': 'center'}),
    html.H3("Drag the slider to see weekly Covid-19 cases", style={'text-align': 'center'}),

    dcc.Slider(
        id='my-slider',
        min=0,
        max=651,
        step=7,
        value=1,
        #marks={i: f"{int(i / 7)}".format(int(i / 7)) for i in range(0, max(ints_cols_2), 7)}
        # For now just hardcose limit on tick marks.
        marks={i: f"{int(i / 7)}".format(int(i / 7)) for i in range(0, 651, 7)}

    ),

    html.Div(id="container2", className='seven columns div-for-charts bg-grey', children=[
        dcc.Graph(id="choropleth",
                  style={'display': 'inline-block', 'width': '45%', 'height': '80%', "margin-top": "10px",
                         "margin-left": "60px"}),
        html.Div(id="container1", className='four columns div-user-controls', children=[
            dcc.Graph(id="covid_cases_timeseries",
                      style={'display': 'inline-block', 'width': '50%', 'height': '35%', "margin-top": "10px"}),
            html.Div(id="graph2", children=[
                dcc.Graph(id="covid_deaths_timeseries",
                          style={'display': 'inline-block', 'width': '50%', 'height': '35%', }),
            ])
        ])

    ], style={'display': 'inline-block', 'width': '100%', 'height': '90vh', 'columnCount': 2,
              "verticalAlign": "top"})
])


# Connect the Plotly graphs with Dash Components
@my_app.callback(
    Output(component_id='choropleth', component_property='figure'),
    Output(component_id='covid_deaths_timeseries', component_property='figure'),
    Output(component_id='covid_cases_timeseries', component_property='figure'),
    Input(component_id='my-slider', component_property='value')
)
# Update function
def update_graph(option_select_day):
    return draw_plot(option_select_day, df, df_deaths, JSON)



 
if __name__ == "__main__":
    my_app.run_server()
    



import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output
import pdb
import numpy as np

import json
from urllib.request import urlopen
import datetime as DT

def map_day(day):
    """
    Map date format days to a raw day with day 0 being first reported US case
    :param day: String
    :return: Int
    """
    first_day = DT.datetime(2020, 1, 21)
    return (first_day + DT.timedelta(days=day)).strftime("%m/%d/%Y")


def draw_plot(option_select_day, df_cases, df_deaths, JSON):
    """
    This function takes input from the app interface and creates an updated covid
    plot for option_select_day (the day that the slider is currently selecting)
    :param option_select_day: Int
    :param df: pandas dataframe
    :param df_deaths: pandas dataframe
    :param JSON:
    :return:list[plotly express figures]
    """

    # Data cleaning and wrangling
    dff = df_cases.copy()
    dff_deaths = df_deaths.copy()

    # The timeseries data from John Hopkins gives total cases for each day
    # use np.diff to get new cases for each day only
    daily_cases = np.diff(dff.iloc[:, 11:option_select_day + 11]).sum(axis=0)
    daily_cases = np.insert(daily_cases, 0, 0)
    daily_deaths = np.diff(dff_deaths.iloc[:, 11:option_select_day + 11]).sum(axis=0)
    daily_deaths = np.insert(daily_deaths, 0, 0)

    # Clean state and FIPS county data
    top_states = dff.sort_values(by=f"{option_select_day}")
    top_states = top_states.loc[0:20, ['Province_State', f"{option_select_day}"]]
    dff_2 = dff.loc[:, ['FIPS', str(option_select_day), 'Admin2']]
    current_day = str(option_select_day)
    #df_3 = df.copy()
    #df_3 = df_3.iloc[:, 11:option_select_day + 11]

    # array with all raw days up the the slider_select_day

    xs = np.arange(0, option_select_day)
    # Plotly Express
    fig1 = px.choropleth(
        geojson=JSON,
        locations=dff_2['FIPS'],
        range_color=(0, 15000),
        scope="usa",
        color=dff[f'{current_day}'],
        color_continuous_scale="YlOrRd",
        hover_name=dff_2["Admin2"],
        hover_data={'FIPS': dff_2['FIPS'].values,
                    'Cases': dff_2[f'{option_select_day}']},
        title=f"New Daily Covid Cases: {map_day(option_select_day)}",
        template="plotly_dark"
    )
    fig1.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)'))
    fig2 = px.bar(x=xs, y=daily_cases, title="Daily Confirmed Cases", template="plotly_dark")
    fig3 = px.bar(x=xs, y=daily_deaths, title="Daily Deaths", template="plotly_dark")

    fig2.update_layout(
        xaxis_title="Days Since First US Case",
        yaxis_title="Cases",
    )

    fig3.update_layout(
        xaxis_title="Days Since First US Case",
        yaxis_title="Deaths",
    )

    # Adding markers to timeseries to indicate significant events during the pandemic
    # e.g. Vaccine mandate was announced approximately 596 days since the first covid case was reported
    # in the United States

    if 672 in xs: # if the current timeseries includes this raw day number
        fig2.add_vline(x=672, line_color="red", annotation_text="First US Omicron Case", annotation_position="top left")
        fig3.add_vline(x=672, line_color="red", annotation_text="First US Omicron Case", annotation_position="top left")

    if 596 in xs:
        fig2.add_vline(x=596, line_color="red", annotation_text="Vaccine Mandate", annotation_position="top left")
        fig3.add_vline(x=596, line_color="red", annotation_text="Vaccine Mandate", annotation_position="top left")


    if 407 in xs:
        fig2.add_vline(x=407, line_color="red", annotation_text="First Vaccine Receives EUA",
                       annotation_position="top left")
        fig3.add_vline(x=407, line_color="red", annotation_text="First Vaccine Receives EUA",
                       annotation_position="top left")
    if 407 in xs:
        fig2.add_vline(x=407, line_color="red", annotation_text="First Vaccine Receives EUA",
                       annotation_position="top left")
        fig3.add_vline(x=407, line_color="red", annotation_text="First Vaccine Receives EUA",
                       annotation_position="top left")


    return [fig1, fig2, fig3]

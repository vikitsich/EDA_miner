from dash import Dash
from dash.dependencies import Input, Output, Event, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import plotly.graph_objs as go

import dash_callback_chain as chainvis

import peakutils
from utils import mapping, load_df, cleanup, r
from apis import twitter_connect

import pandas as pd
import base64
import datetime
import io
import atexit
import uuid
import redis

from app import app



layout = html.Div(children=[
    html.Div(children=[
        dcc.Tabs(id="graphs", value='regression', children=[
            dcc.Tab(label='Exploratory analyis', value='exploration',
                    id="exploration"),
            dcc.Tab(label='Key performance indicators', value='kpi',
                    id="kpi"),
            dcc.Tab(label='3D graphs', value='graphs3d',
                    id="graphs3d"),
            dcc.Tab(label='Network graphs', value='networks',
                    id="networks"),
        ]),
    ]),
    html.Div(id="visuals-content"),
])


@app.callback(Output('visuals-content', 'children'),
              [Input('graphs', 'value')],
              [State("user_id", "children")])
def low_level_tabs_visualization(tab, user_id):

    df = load_df(r, user_id)

    if tab == 'exploration':
        return html.Div(children=[
            html.Button("Data exploration", id="r2d2"),

            html.H4("X variable:"),
            dcc.Dropdown(
                options=[
                    {'label': col, 'value': col}
                    for col in df.columns],
                multi=False,
                id="xvar_eda",
                value=df.columns[-1],
            ),
            html.H4("Variables:"),
            dcc.Dropdown(
                options=[
                    {'label': col, 'value': col}
                    for col in df.columns],
                multi=False,
                id="yvar_eda",
                value=df.columns[-1],
            ),
            dcc.Graph(id="graph2d"),


        ])
    elif tab == 'kpi':

        return html.Div(children=[
            html.H4("X variable:"),
            dcc.Dropdown(
                options=[
                    {'label': col, 'value': col}
                    for col in df.columns],
                multi=False,
                id="xvar_kpi",
                value=df.columns[-1],
            ),
            html.H4("Variables:"),
            dcc.Dropdown(
                options=[
                    {'label': col, 'value': col}
                    for col in df.columns],
                multi=True,
                id="yvar_kpi",
                value=df.columns[-1],
            ),
            dcc.Graph(id="baseline_graph"),])

    elif tab == "graphs3d":
        return html.Div(children=[
            html.Button("mpl3d or mpld3 ??!!", id="d33d"),
        ])
    elif tab == "networks":
        return html.Div(children=[
            html.Button("networkx is awesome", id="nx"),
        ])


@app.callback(
    Output("graph2d", "figure"),
    [Input("xvar_eda", "value"),
     Input("yvar_eda", "value")],
    [State("user_id", "children")])
def plot_graph2d(xvars, yvars, user_id):
    df = load_df(r, user_id)


    traces = [
        go.Scatter(
            x=df[xvars],
            y=df[yvars],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
        ),
    ]

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': xvars},
            yaxis={'title': yvars},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
            )

    }



@app.callback(
    Output("baseline_graph", "figure"),
    [Input("xvar_kpi", "value"),
     Input("yvar_kpi", "value")],
    [State("user_id", "children")])
def plot_baseline_graph(xvars, yvars, user_id):

    df = load_df(r, user_id)

    if not isinstance(yvars, list):
        yvars = [yvars]

    print(yvars)

    traces = [
        go.Scatter(
            x=df[xvars],
            y=peakutils.baseline(df[yvars[0]]),
            mode='lines',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': (0,100,255)}
            },
            name="Baseline",
        )] + [
        go.Scatter(
            x=df[xvars],
            y=df[yvar],
            mode='lines+markers',
            opacity=0.7,
            marker={
                'size': 8,
                'line': {'width': 0.5, 'color': 'rgb(210, 40, 180)'},
                'color': 'rgb(180, 35, 180)'
            },
            name="Volume"
        )
        for yvar in yvars]

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': xvars},
            yaxis={'title': yvars},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
            )

    }

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
from utils import load_df, r, create_dropdown
from apps.view_tabs.Exploration import simple_scatter

import plotly.graph_objs as go
import peakutils


def KPI_Options(df):

    options = [
        {'label': col, 'value': col}
        for col in df.columns
    ]

    return html.Div(children=[

        *create_dropdown("X variables", options,
                         multi=False, id="xvars"),
        *create_dropdown("Y variable", options,
                         multi=True, id="yvars"),

        dcc.Graph(id="graph"),
    ])



def baseline_graph(df, xvars, yvars, **kwargs):

    return [
        go.Scatter(
            x=df[xvars],
            y=peakutils.baseline(df[yvar]),
            mode='lines',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': (0,100,255)}
            },
            name=f"Baseline for {' '.join(yvar.split()[:2])}",
        ) for yvar in yvars] + [
            # one scatter for each y variable
            simple_scatter(df, xvars, yvar,
                           mode='lines+markers',
                           marker={
                               'size': 8,
                               'line': {
                                   'width': 0.5,
                                   'color': 'rgb(210, 40, 180)'
                                },
                               'color': 'rgb(180, 35, 180)'
                           },
                           name=yvar)[0]
            for yvar in yvars
        ]

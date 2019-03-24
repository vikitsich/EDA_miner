from dash.dependencies import Input, Output, Event, State
import dash_core_components as dcc
import dash_html_components as html

from app import app
from utils import load_df, r, create_dropdown

import plotly.graph_objs as go


def Network_Options(df):

    options = [
        {'label': col, 'value': col}
        for col in df.columns
    ]

    return html.Div(children=[
        html.Button("networkx is awesome", id="nx"),

        *create_dropdown("X variables", options,
                         multi=False, id="xvars"),
        *create_dropdown("Y variable", options,
                         multi=False, id="yvars"),

        dcc.Graph(id="graph"),
    ])

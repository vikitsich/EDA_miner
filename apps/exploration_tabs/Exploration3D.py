"""
    This module will be used to plot 3D graphs.

    You can write code in this module, but keep in
    mind that it may be moved later on to lower-level
    modules. Also, there is a chance that this will be
    moved entirely into another tab.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
from utils import load_df, r, create_dropdown

import plotly.graph_objs as go
import peakutils

def Exploration3D_Options(options, results):

    options = [
        {'label': col, 'value': col}
        for col in df.columns
    ]

    return html.Div(children=[
        html.Button("mpl3d or mpld3 ??!!", id="d33d"),

        *create_dropdown("X variables", options,
                         multi=False, id="xvars"),
        *create_dropdown("Y variable", options,
                         multi=False, id="yvars"),


        dcc.Graph(id="graph"),
    ])

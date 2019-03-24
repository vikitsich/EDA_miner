from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
from utils import load_df, r, create_dropdown

import plotly.graph_objs as go


def Exploration_Options(df):

    options = [
        {'label': col, 'value': col}
        for col in df.columns
    ]

    return html.Div(children=[

        *create_dropdown("X variables", options,
                         multi=False, id="xvars"),
        *create_dropdown("Y variable", options,
                         multi=False, id="yvars"),

        dcc.Graph(id="graph"),
    ])



def simple_scatter(df, xvars, yvars, **kwargs):

    options = dict(
        mode='markers',
        opacity=0.7,
        marker={
            'size': 15,
            'line': {'width': 0.5, 'color': 'white'}
        },
    )

    options.update(kwargs)

    return [
        go.Scatter(
            x=df[xvars],
            y=df[yvars],
            **options
        ),
    ]

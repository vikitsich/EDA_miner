from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
from utils import load_df, r, create_dropdown

import plotly.graph_objs as go


def Network_Options(options, results):

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

        dcc.Graph(id="graph_network"),
    ])


@app.callback(Output("graph_network", "children"),
              [Input("xvars", "value")])
def plot_graph_network(xvars):
    traces = [{'values': [[10,90],[5, 95],[15,85],[20,80]][3],
               'type': 'pie',},]

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

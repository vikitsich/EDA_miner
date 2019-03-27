from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
from utils import load_df, r, create_dropdown
from apps.data_tabs.View import get_data

import plotly.graph_objs as go



def Exploration_Options(options, results):

    return html.Div(children=[

        *create_dropdown("Available datasets:", options,
                         multi=False, id="dataset_choice_2d"),

        html.Div(id="variable_choices_2d"),

        dcc.Graph(id="graph_2d"),
    ])


@app.callback(Output("variable_choices_2d", "children"),
              [Input("dataset_choice_2d", "value")],
              [State("user_id", "children")])
def render_variable_choices_2d(dataset_choice, user_id):

    data = get_data(dataset_choice, user_id)

    options = [{'label': "No dataset selected yet", 'value': "no_data"}]
    if data is not None:
        options=[{'label': col, 'value': col} for col in data.columns]

    return [
        *create_dropdown("X variable", options,
                         multi=False, id="xvars_2d"),
        *create_dropdown("Y variable", options,
                         multi=False, id="yvars_2d"),
    ]


@app.callback(
    Output("graph_2d", "figure"),
    [Input("xvars_2d", "value"),
     Input("yvars_2d", "value")],
    [State("user_id", "children"),
     State('viz_tabs', 'value'), # can probably be removed
     State('dataset_choice_2d', 'value')])
def plot_graph_2d(xvars, yvars, user_id, viz_tab, dataset_choice):

    df = get_data(dataset_choice, user_id)

    if any(x is None for x in [xvars, yvars, df]):
        return {}

    # simple scatter
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

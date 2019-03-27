from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from utils import mapping, load_df, cleanup, r, encode_image
from server import app
from utils import load_df, r, create_dropdown
from apps.data_tabs.View import get_data

import plotly.graph_objs as go
import peakutils
import numpy as np


SideBar_KPIs = [
        html.H4('Key Performance Indicators', id = 'kpis'),
        html.Ul([
            html.Button('Built Your KPIs', id = 'custom_kpis'),
            html.Button('Baseline Modeling', id = 'baseline_modelling'),
            html.Button('Built Your Report', id = 'custom-report')
        ]),
        html.Div(id="SideBar-kpis"),
    ]


def KPI_Options(options, results):

    return html.Div(children=[

        *create_dropdown("Available datasets:", options,
                         multi=False, id="dataset_choice_kpi"),

        html.Div(id="variable_choices_kpi"),

        dcc.Graph(id="graph_kpi"),
    ])

@app.callback(Output("variable_choices_kpi", "children"),
              [Input("dataset_choice_kpi", "value")],
              [State("user_id", "children")])
def render_variable_choices_kpi(dataset_choice, user_id):

    data = get_data(dataset_choice, user_id)

    options = [{'label': "No dataset selected yet", 'value': "no_data"}]
    if data is not None:
        options=[{'label': col, 'value': col} for col in data.columns]

    return [
        *create_dropdown("X variables", options,
                         multi=False, id="xvars"),
        *create_dropdown("Choose The Variable For The Baseline Calculation", options,
                         multi=False, id="yvars"),
        *create_dropdown("Choose The Variable For The Bar Chart", options,
                         multi=False, id="secondary_yvars"),

        dcc.Graph(id="graph"),
    ])


def hard_cast_to_float(x):
    try:
        ret = np.float32(x)
    except:
        ret = 0

    return ret


@app.callback(
    Output("graph_kpi", "figure"),
    [Input("xvars_kpi", "value"),
     Input("yvars_kpi", "value"),
     Input("secondary_yvars_kpi", "value")],
    [State("user_id", "children"),
     State('viz_tabs', 'value'), # can probably be removed
     State('dataset_choice_kpi', 'value')])
def plot_graph_kpi(xvars, yvars, secondary_yvars,
                   user_id, viz_tab, dataset_choice):

    df = get_data(dataset_choice, user_id)

    if any(x is None for x in [xvars, yvars, secondary_yvars, df]):
        return {}

    # baseline graph
    traces = [
        go.Scatter(
            x=df[xvars],
            y=peakutils.baseline(df[yvar].apply(hard_cast_to_float)),
            mode='lines',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': (0,100,255)}
            },
            name=f"Baseline for {' '.join(yvar.split()[:2])}",
        ) for yvar in yvars] + [
        # one scatter for each y variable
        go.Scatter(x=df[xvars],
                   y=df[yvar].apply(hard_cast_to_float),
                   mode='lines+markers',
                   marker={
                       'size': 8,
                       'line': {
                           'width': 0.5,
                           'color': 'rgb(210, 40, 180)'
                        },
                       'color': 'rgb(180, 35, 180)'
                   },
                   name=yvar
            ) for yvar in yvars] + [
        go.Bar(
            x=df[xvars],
            y=df[secondary_yvars].apply(hard_cast_to_float),
        )
        ]

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': xvars},
            yaxis={'title': yvars},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
        )
    }

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from utils import mapping, load_df, cleanup, r, encode_image
from server import app
from utils import load_df, r, create_dropdown
from apps.exploration_tabs.Exploration import simple_scatter

import plotly.graph_objs as go
import peakutils


SideBar_KPIs = [
        html.Br(),
        html.H4('Key Performance Indicators', id = 'kpis'),
        html.Ul([
            html.Button('Built Your KPIs', id = 'custom_kpis'),
            html.Button('Baseline Modeling', id = 'baseline_modelling'),
            html.Button('Built Your Report', id = 'custom-report')
        ]),
        html.Div(id="SideBar-kpis"),
    ]



def KPI_Options(df):

    options = [
        {'label': col, 'value': col}
        for col in df.columns
    ]

    return html.Div(children=[

        *create_dropdown("X variables", options,
                         multi=False, id="xvars"),
        *create_dropdown("Choose The Variable For The Baseline Calculation", options,
                         multi=False, id="yvars"),
        *create_dropdown("Choose The Variable For The Bar Chart", options,
                         multi=False, id="secondary_yvars"),

        dcc.Graph(id="graph"),
    ])
'''
@app.callback(Output('SideBar-kpis', 'children'),
              [Input('SideBar-kpis', 'value')])
'''
def baseline_graph(df, xvars, yvars, secondary_yvars, **kwargs):

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

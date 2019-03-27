from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
from utils import load_df, r
from apps.exploration_tabs import Exploration, KPIs
from apps.exploration_tabs import Exploration_Options, KPI_Options
from apps.exploration_tabs import Exploration3D_Options, Network_Options
from apps.data_tabs.View import get_available_choices

import plotly.graph_objs as go
import peakutils



layout = html.Div(children=[
    html.Div(children=[
        dcc.Tabs(id="viz_tabs", value='exploration', children=[
            dcc.Tab(label='Exploratory analysis', value='exploration',
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
              [Input('viz_tabs', 'value')],
              [State("user_id", "children")])
def tab_subpages(tab, user_id):

    options, results = get_available_choices(r, user_id)

    #
    if all(v is None for k,v in results.items()):
        return html.H4("No data currently uploaded")

    # each view should handle on its own how chaning
    # the dataset it handled
    if tab == 'exploration':
        return Exploration_Options(options, results)

    elif tab == 'kpi':
        return KPI_Options(options, results)

    elif tab == "graphs3d":
        return Exploration3D_Options(options, results)

    elif tab == "networks":
        return Network_Options(options, results)




@app.callback(
    Output("graph", "figure"),
    [Input("xvars", "value"),
     Input("yvars", "value")],
    [State("user_id", "children"),
     State('viz_tabs', 'value')])
def plot_graph(xvars, yvars, user_id, viz_tab):



    if any(x is None for x in [xvars, yvars, df]):
        return {}

    if viz_tab == "exploration":
        traces = Exploration.simple_scatter(df, xvars, yvars)

    elif viz_tab == "kpi":
        if not isinstance(yvars, list):
            yvars = [yvars]
        traces = KPIs.baseline_graph(df, xvars, yvars)

    else:
        # simple pie chart
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

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import dash_table
import dash_callback_chain as chainvis

from server import app
from utils import load_df, r
from apps.data_tabs import APIs
from apps.data_tabs import Upload_Options, View_Options, API_Options



layout = html.Div(children=[
    html.Div(children=[
        dcc.Tabs(id="data_tabs", value='upload_data', children=[
            dcc.Tab(label='Upload Data', value='upload_data',
                    id="upload_data"),
            dcc.Tab(label='Connect to API', value='api_data',
                    id="api_data"),
            dcc.Tab(label='View Data', value='view_data',
                    id="view_data"),
        ]),
    ]),
    html.Div(id="data-content"),
])


@app.callback(Output('data-content', 'children'),
              [Input('data_tabs', 'value')],
              [State("user_id", "children")])
def tab_subpages(tab, user_id):
    """
        This is the second level of data tabs, that gets
        called when one of the first-level tabs is selected.
        Here you can either upload your data, connect to an
        API, or view already uploaded data.

        Input comes from current module, output comes from
        the modules in data_tabs (loaded in __init__)
    """

    if tab == 'upload_data':
        return Upload_Options

    elif tab == "view_data":
        df = load_df(r, user_id)
        return View_Options(df)

    elif tab == "api_data":
        return API_Options

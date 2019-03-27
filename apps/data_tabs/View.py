from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import dash_table

import pandas as pd
import datetime
import pickle

from server import app
from utils import r, load_df, pretty_print_tweets



def get_available_choices(redisConn, user_id):

    results = {
        "twitter_api": redisConn.get(f"{user_id}_twitter_api_handle"),
        "gsheets_api": redisConn.get(f"{user_id}_gsheets_api_data"),
        "user_data": redisConn.get(f"{user_id}_user_dataframe"),
    }
    options=[
        {'label': k, 'value': k}
        for k,v in results.items() if v is not None
    ]
    if len(options) < 1:
        options = [{'label': "No uploaded data yet", 'value': "no_data"}]

    return options, results

def get_data(api_data_choice, user_id):
    if api_data_choice == "gsheets_api":
        df = r.get(f"{user_id}_gsheets_api_data")
        df = pickle.loads(df)

    # uploaded data
    elif api_data_choice == "user_data":
        df =  load_df(r, user_id)

    else:
        df = None

    return df


def View_Options(user_id):

    options, results = get_available_choices(r, user_id)
    available_choices = dcc.Dropdown(options=options, id="api_data_choice")

    return [
        html.Br(),

        available_choices,
        html.Div(id="table_view", children=[
            dash_table.DataTable(id='table'),
        ]),
    ]


@app.callback(Output("table_view", "children"),
              [Input("api_data_choice", "value")],
              [State("user_id", "children")])
def render_table(api_data_choice, user_id):

    if api_data_choice == "twitter_api":
        api = r.get(f"{user_id}_twitter_api_handle")

        return pretty_print_tweets(api, 5)

    df = get_data(api_data_choice, user_id)

    if df is None:
        return [html.H4("Nothing to display")]


    df = df[df.columns[:10]]

    # if not, return this table
    return [
        html.Br(),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict("rows"),
            style_table={
                'maxHeight': '400',
                'overflowY': 'scroll'
            },
            sorting=True,
            editable=True,
            pagination_mode='fe',
            pagination_settings={
                "displayed_pages": 1,
                "current_page": 0,
                "page_size": 10,
            },
            navigation="page",
            # n_fixed_rows=1,
            style_cell={
                'width': '150px',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'maxWidth': 0,
                'paddingLeft': '15px',
                # 'paddingRight': '15px',
            },
            style_cell_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(218, 218, 218)'
                },
                {
                    'if': {'row_index': 'even'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                },
            ],
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'rgb(230,230,230)',
                "fontWeight": "bold",
            },
        ),
    ]

from dash import Dash
from dash.dependencies import Input, Output, Event, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import dash_callback_chain as chainvis

from utils import mapping, load_df, cleanup, parse_contents, r
from apis import twitter_connect

import pandas as pd
import base64
import datetime
import io
import atexit
import uuid
import redis

from app import app



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
    html.Div(id="data-content", children=[
        dash_table.DataTable(
                id='table',
            ),
        ], style={"display":"inline"}),
])


@app.callback(Output('data-content', 'children'),
              [Input('data_tabs', 'value')],
              [State("user_id", "children")])
def data_tab_subpages(tab, user_id):
    """
        This is the second level of data tabs, that gets
        called when one of the first-level tabs is selected.
        Here you can either upload your data or view already
        uploaded data.
    """

    if tab == 'upload_data':
        return [
            dcc.Upload(
                id='upload_data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]), style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=True
            ),
            html.Div(id='output-data-upload'),
        ]

    elif tab == "view_data":
        df = load_df(r, user_id)

        if df is not None:
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

        else:
            # if you don't have any tables stored in
            #  memory prompt the user to upload one
            return [
                html.Div(id="data-content", children=[
                    html.H3("Upload data first"),
                ], style={"display":"inline"}),
            ]

    elif tab == "api_data":

        return html.Div(children=[
            html.H4("Connect to an API from the list:"),
            html.Button("twitter", value="twitter",
                        id="twitter_button", n_clicks=0),
            html.Button("Google Docs", value="google_docs",
                        id="api_choice"),
            html.Button("Google Sheets", value="google_sheets",
                        id="api_choice"),
            html.Div([], id="api_login_form"),
            html.Div([], id="api_interface"),
            html.Div(["false"], id="connected", style={"display":"none"}),
        ])


# TODO: same as above
# Generally, the inconsistency rises from the fact
# that the guide was meant for multiple-file uploads
@app.callback(Output('output-data-upload', 'children'),
              [Input('upload_data', 'contents'),],
              [State('upload_data', 'filename'),
               State('upload_data', 'last_modified'),
               State("user_id", "children")])
def update_output(list_of_contents, list_of_names,
                  list_of_dates, user_id):

    if list_of_contents is not None:
        response = [parse_contents(c, n, d, user_id) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]

        return response



@app.callback(Output('api_login_form', 'children'),
              [Input('twitter_button', 'n_clicks')],
              [State("user_id", "children"),
               State("connected", "children")])
def api_connect(n_clicks, user_id, children):

    if n_clicks % 2 == 1 and children[0]=="false":

        return [
            html.H5("Key"),
            dcc.Input(id="twitter_password", type="password"),
            html.H5("Secret Key"),
            dcc.Input(id="secret_key", type="password"),
            html.H5("Access Token"),
            dcc.Input(id="access_token", type="password"),
            html.H5("Access Token Secret"),
            dcc.Input(id="token_secret", type="password"),
            html.Button("Connect!", id="twitter_connect_button")
        ]
    else:
        return []

@app.callback(Output('api_interface', 'children'),
              [Input('twitter_connect_button', 'n_clicks')],
              [State("twitter_password", "value"),
               State("secret_key", "value"),
               State("access_token", "value"),
               State("token_secret", "value"),
               State("user_id", "children")])
def api_connect(n_clicks, twitter_password, secret_key,
                access_token, token_secret, user_id):

    api = twitter_connect(twitter_password, secret_key,
                          access_token, token_secret)

    return [
        html.H4("Successfully connected to the Twitter API."),
        html.Br(),
    ] + [
        html.H5(str(tweet.text))
        for tweet in api.GetUserTimeline()[:5]
    ]


# These two, along with  the hidden state in Div(id=`connected`)
# work, somehow, but this is definitely not clean and scalable code
@app.callback(
    Output('connected', 'children'),
    [Input('api_interface', 'children')])
def hide_login_form(children):
    if len(children)>=1:
        return ["true"]

    return ["false"]

@app.callback(
    Output('api_login_form', 'style'),
    [Input('api_interface', 'children')])
def hide_login_form(children):

    if len(children)>=1:
        return {"display":"none"}

    return {"display":"inline"}

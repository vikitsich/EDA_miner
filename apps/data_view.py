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





## TODO: Everything below here regarding the twitter API needs
## to be seriously reworked
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

    api = APIs.twitter_connect(twitter_password, secret_key,
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

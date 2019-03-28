from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
from utils import r, pretty_print_tweets
from apps.data_tabs import View_Options

import twitter
import praw
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import pickle


debuger_layout = [
    dcc.Input(id="input1", type="text", value="", style={"display":"none"}),
    dcc.Input(id="input2", type="text", value="", style={"display":"none"}),
    dcc.Input(id="input3", type="text", value="", style={"display":"none"}),
    dcc.Input(id="input4", type="text", value="", style={"display":"none"}),
    html.Button("Connect!", id="connect_button", style={"display":"none"}),
]


API_Options = html.Div(children=[
    html.H4("Connect to an API from the list:"),

    html.Div(children=[
        dcc.Tabs(id="api_choice", value='twitter_api_tab', children=[
            dcc.Tab(label='Twitter', value='twitter_api_tab',
                    id="twitter_api_tab"),
            dcc.Tab(label='Google Sheets', value='gsheets_api_tab',
                    id="gsheets_api_tab"),
            dcc.Tab(label='Reddit', value='reddit_api_tab',
                    id="reddit_api_tab"),
        ]),
    ]),

    html.Div(id="api_login_form", children=[
        *debuger_layout,
    ]),


])




@app.callback(Output('api_login_form', 'children'),
              [Input('api_choice', 'value'),
               Input('connect_button', 'n_clicks')],
              [State("user_id", "children"),
               State("input1", "value"),
               State("input2", "value"),
               State("input3", "value"),
               State("input4", "value")])
def api_connect(api_choice, n_clicks, user_id,
                input1, input2,
                input3, input4):
    """
        Depending on the tab choice, provide the appropriate form.
        This callback is also responsible for adding the submit button
        if necessary.
    """


    connected = r.get(f"{user_id}_{api_choice}") is not None

    if api_choice == "twitter_api_tab":

        if n_clicks is not None and n_clicks >= 1:

            if not connected:
                api = twitter_connect(input1, input2,
                                      input3, input4)
                r.set(f"{user_id}_{api_choice}", "true")

                # store the api object to redis so it
                # can be used in other parts
                r.set(f"{user_id}_twitter_handle", pickle.dumps(api))

                return [
                    html.H4("Successfully connected to the Twitter API."),
                    html.Br(),
                    *debuger_layout,
                ] + pretty_print_tweets(api, 5)

            else:
                return [
                    html.H4("Connected previously"),
                    *debuger_layout,
                ]

        elif not connected:
            return twitter_layout

        else:
            return [
                html.H4("Connected previously"),
                *debuger_layout,
            ]


    elif api_choice == "gsheets_api_tab":

        if n_clicks is not None and n_clicks >= 1:

            if not connected:
                gc, spreadsheet, ws, data = google_sheets_connect(input1,
                                                                  input2)

                r.set(f"{user_id}_{api_choice}", "true")

                # userid_data_gsheets
                r.set(f"{user_id}_gsheets_api_data", pickle.dumps(data))

                return [
                    html.H4("Successfully connected to the Google Sheets API."),
                    html.Br(),
                    *debuger_layout,
                ]

        elif not connected:
            return gsheets_layout

        else:
            return [
                html.H4("Connected previously"),
                *debuger_layout,
            ]

    elif api_choice == "reddit_api_tab":

        if n_clicks is not None and n_clicks >= 1:

            if not connected:
                reddit_api = reddit_connect(input1, input2)

                r.set(f"{user_id}_{api_choice}", "true")
                r.set(f"{user_id}_reddit_handle", pickle.dumps(reddit_api))

                return [
                    html.H4("Successfully connected to the Reddit API."),
                    html.Br(),
                    *debuger_layout,
                ]

        elif not connected:
            return reddit_layout

        else:
            return [
                html.H4("Connected previously"),
                *debuger_layout,
            ]

    else:
        return [
            html.H4(f"{api_choice} not yet implemented"),
            html.H4("Debug element, please ignore"),
            *debuger_layout,
        ]



twitter_layout = [
    html.H5("Key"),
    dcc.Input(id="input1", type="text"),
    html.H5("Secret Key"),
    dcc.Input(id="input2", type="text"),
    html.H5("Access Token"),
    dcc.Input(id="input3", type="text"),
    html.H5("Access Token Secret"),
    dcc.Input(id="input4", type="text"),

    html.Button("Connect!", id="connect_button",
                style={"display":"inline"})
]

gsheets_layout = [
    html.H5("Credentials file path"),
    dcc.Input(id="input1", type="text"),
    html.H5("Secret Key"),
    dcc.Input(id="input2", type="text"),

    dcc.Input(id="input3", type="text", style={"display":"none"}),
    dcc.Input(id="input4", type="text", style={"display":"none"}),

    html.Button("Connect!", id="connect_button",
                style={"display":"inline"})
]

reddit_layout = [
    html.H5("Client id"),
    dcc.Input(id="input1", type="text"),
    html.H5("Client secret"),
    dcc.Input(id="input2", type="text"),

    dcc.Input(id="input3", type="text", style={"display":"none"}),
    dcc.Input(id="input4", type="text", style={"display":"none"}),

    html.Button("Connect!", id="connect_button",
                style={"display":"inline"})
]


def reddit_connect(client_id, client_secret):

    reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent='EDA miner')

    return reddit


def twitter_connect(API_key, API_secret_key,
                    access_token, access_token_secret,
                    sleep_on_rate_limit=True):
    """Connect to Twitter API, and return a handle"""

    print("Connecting to the Twitter API...")

    api = twitter.Api(consumer_key=API_key,
                      consumer_secret=API_secret_key,
                      access_token_key=access_token,
                      access_token_secret=access_token_secret,
                      sleep_on_rate_limit=sleep_on_rate_limit)
    api.VerifyCredentials()

    return api


def google_sheets_connect(credentials_file, gspread_key):

    print("Connecting to the GSheets API...")


    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    # load credentials from file
    credentials = (ServiceAccountCredentials
                   .from_json_keyfile_name(credentials_file, scope))

    # create an interface to google
    gc = gspread.authorize(credentials)

    # connect to a certain spreadsheet, using it's key
    # e.g. full address: https://docs.google.com/spreadsheets/d/1802UymlFPQE2uvk_T8XI3kX1kWniYOngS6sQSnXoe2U/
    # remember to either allow the service account's email (see the authorization .json file)
    # to access the spreadsheet or to allow access to everyone who has a link (or both)
    spreadsheet = gc.open_by_key(gspread_key)
    ws = spreadsheet.get_worksheet(0)

    data = ws.get_all_values()
    data = pd.DataFrame(data[1:], columns=data[0])

    return (gc, spreadsheet, ws, data)


def facebook_connect():
    raise NotImplementedError

def google_docs_connect():
    raise NotImplementedError

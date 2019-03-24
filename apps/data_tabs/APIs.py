import dash_core_components as dcc
import dash_html_components as html

import twitter


API_Options = html.Div(children=[
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


def twitter_connect(API_key, API_secret_key,
                    access_token, access_token_secret,
                    sleep_on_rate_limit=True):
    """Connect to Twitter API, and return a handle"""

    api = twitter.Api(consumer_key=API_key,
                      consumer_secret=API_secret_key,
                      access_token_key=access_token,
                      access_token_secret=access_token_secret,
                      sleep_on_rate_limit=sleep_on_rate_limit)

    api.VerifyCredentials()

    return api


def facebook_connect():
    raise NotImplementedError

def google_docs_connect():
    raise NotImplementedError

def google_sheets_connect():
    raise NotImplementedError

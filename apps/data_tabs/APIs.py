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


def google_sheets_connect(credentials_file, gspread_key):

    # TODO: Incomplete. Needs frontend interface
    raise NotImplementedError


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
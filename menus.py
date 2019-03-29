"""
    This module will collect all unchanging views and dash
    components (buttons, sidemenus, etc) so that the code
    in index.py is cleaner and abstracted.

    You should probably not write code here.
"""

import dash_core_components as dcc
import dash_html_components as html

import dash_table

from server import app
from utils import mapping, load_df, cleanup, r, encode_image

import uuid


# This page appears first, when the user first accesses the page
# Here, the user will be prompted to log in.
landing_page = html.Div([
        html.H2("Welcome to our app! :D"),
        html.H4("Would you like to login?"),
        dcc.RadioItems(
            options=[
                {'label': 'Yes, log me in', 'value': 'yes'},
                {'label': 'No, leave me alone', 'value': 'no'}
            ],
            value='yes',
            labelStyle={'display': 'inline-block',
                        "padding":"10px"},
            id="login_choice",
        ),
        html.Div(id="landing_page_form", children=[
            html.Div(id="login_form", children=[
                dcc.Input("username", type="text", value="",
                          placeholder="username"),
            ], style={"display":"none"}),

        ]),
        html.Div(html.Button("Submit", id="submit_login_choice")),
    ], id="landing_page")


SideBar = [

    html.Img(id="app_logo", src=encode_image("assets/images/y2d.png")),
    html.Br(),

    html.H2("Sidemenu1"),
    html.Button('Dark/Light theme', id="dark_theme"),

    # Collapsible button with external links
    html.Button([
        html.Span('External links'),
        html.I("", className="fa fa-caret-down", style={"fontSize":"24px",
                                                 "verticalAlign":"middle",
                                                 "paddingLeft":"5px"}),
    ], id='button_collapse', n_clicks=0),
    html.Div(id='sidebar_collapsible_button', children=[
        html.Ul([
            html.Li(html.A([
                    html.Span("GitHub repo  "),
                    html.I(className="fab fa-github", style={"fontSize":"28px",
                                                             "verticalAlign":"bottom",
                                                             "paddingTop":"5px"}),

                    ], href="https://github.com/KMouratidis/EDA_miner",
                   target="_blank"),
                ),
            html.Li('I am just padded text'),
        ])
    ]),

    # Placeholder for low-level submenus, if needed
    html.H2("Sidemenu2"),
    html.Div(children=[], id="low_level_tabs_submenu")
]


MainMenu = [

    # Tabs, level-1
    html.Div(children=[
        dcc.Tabs(id="high_level_tabs", value='data', children=[
            dcc.Tab(label='Data view', value='data',
                    id="data"),
            dcc.Tab(label='Explore & Visualize', value='EDA',
                    id="EDA"),
            dcc.Tab(label='Analyze & Predict', value='modelling',
                    id="modelling"),
        ]),
    ]),

    # Placeholder for level-2 tabs
    html.Div(id="selected_subpage"),

    # Due to a known Dash bug, the table
    # must be present in the first layout
    html.Div(id="table_container", children=[
        dash_table.DataTable(id='table',),
    ], style={"display":"none"}),
]


def serve_layout():
    """
        The layout of our app needs to be inside a function
        so that every time some new session starts a new
        session_id is generated.
    """

    # TODO: append above uuid to a Redis list.
    session_id = str(uuid.uuid4())

    return html.Div(children=[

        # TODO: Better implementation of sessions.
        # This generates a unique id for the session, based on which
        # one can keep his data in disk. This may need changing to
        # either using tokens or to some login form
        # TAKE A LOOK AT dcc.Store
        html.H2(session_id, id="session_id", style={"display":"none"}),
        html.H2(session_id, id="user_id", style={"display":"none"}),

        # Sidebar / menu
        html.Div(children=SideBar, className="two columns", id="sidebar"),

        # main Div
        html.Div(children=MainMenu, className="nine columns", id="mainmenu"),

    ], className="row", style={"display": "none"}, id="main_page")

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import dash_table
import dash_callback_chain as chainvis

from server import app
from apps import data_view, exploration_view, analyze_view, exploration_tabs
from apps.exploration_tabs import KPIs
from utils import cleanup, r
from menus import SideBar, MainMenu

from functools import partial
import pandas as pd
import base64
import datetime
import io
import atexit
import signal
import uuid
import redis



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


landing_page = html.Div([
        html.H2("Welcome to our app! :D"),
        html.H4("Would you like to login?"),
        dcc.RadioItems(
            options=[
                {'label': 'Yes, log me in', 'value': 'yes'},
                {'label': 'No, leave me alone', 'value': 'no'}
            ],
            value='yes',
            labelStyle={'display': 'inline-block'},
            id="login_choice",
        ),
        html.Div(id="landing_page_form", children=[
            html.Div(id="login_form", children=[
                dcc.Input("username", type="text", value=""),
            ], style={"display":"none"}),

        ]),
        html.Div(html.Button("Submit", id="submit_login_choice")),
    ], id="landing_page")


app.layout = html.Div([
    landing_page,
    serve_layout(),
])


# Show or display login form
@app.callback(Output("login_form", "style"),
              [Input("login_choice", "value")])
def show_login_input(value):
    if value == "yes":
        return {"display":"inline"}
    else:
        return {"display":"none"}


# Return appropriate layout after submit page
@app.callback([Output("main_page", "style"),
               Output("landing_page", "style"),
               Output("user_id", "children")],
              [Input("submit_login_choice", "n_clicks")],
              [State("session_id", "children"),
               State("username", "value")])
def go_to_main_page(n_clicks, session_id, username):
    if n_clicks is not None and n_clicks >= 1:
        outputs = [{"display":"inline"}, {"display":"none"}]
    else:
        outputs = [{"display":"none"}, {"display":"inline"}]

    if username is not None and len(username) >= 3:
        outputs += [username]
    else:
        outputs += [session_id]

    return outputs


# Input and Output defined in MainMenu
@app.callback(Output('selected_subpage', 'children'),
              [Input('high_level_tabs', 'value')])
def high_level_tabs(tab):
    """
        For the first level of tabs, decide which submenu to
        return. Choices are: Data View, Exploratory Data Analysis
        and Modelling.
    """

    if tab == 'EDA':
        return exploration_view.layout
    elif tab == "modelling":
        return analyze_view.layout
    elif tab == "data":
        return data_view.layout
    else:
        return '404'


#Input and Output for the Sidebar, for each lower level tab
@app.callback(Output('low_level_tabs_submenu', 'children'),
              [Input('viz_tabs', 'value')])
def update_sidebar_menus(tab):
    """
        For the second level of tabs, show different sidebar menu. Choises are:
        Baseline Modelling, Built KPIs.
        This is implemented only for KPI tab
    """
    if tab == 'exploration':
        return [html.H4(f"Tab is {tab}")]
    if tab == 'kpi':
        return KPIs.SideBar_KPIs
    if tab == 'graphs3d':
        return [html.H4(f"Tab is {tab}")]
    if tab == 'networks':
        return [html.H4(f"Tab is {tab}")]


@app.callback(Output('low_level_tabs_submenu', 'style'),
              [Input('high_level_tabs', 'value')])
def high_level_tabs(tab):
    if tab != "EDA":
        return {"display":"none"}
    else:
        return {"display":"inline"}


## When the sidebar button is clicked, collapse the div
@app.callback(Output('sidebar_collapsible_button', 'style'),
              [Input('button_collapse', 'n_clicks')],)
def button_toggle(n_clicks):
    if n_clicks % 2 == 1:
        return {'display': 'none'}
    else:
        return {'display': 'block'}



if __name__ == "__main__":
    # TODO: Implement user_id correctly:
    # create a Redis entry with all `user_id`s that
    # joined the session and cleanup for each of them

    try:
        app.run_server(debug=True, host= '0.0.0.0')

    finally:
        cleanup(r)

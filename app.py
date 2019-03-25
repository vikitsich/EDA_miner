from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import dash_table
import dash_callback_chain as chainvis

from server import app
from apps import data_view, exploration_view, analyze_view, view_tabs
from apps.view_tabs import KPIs
from utils import cleanup, r
from menus import SideBar, MainMenu

import pandas as pd
import base64
import datetime
import io
import atexit
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
        html.H2(session_id, id="user_id", style={"display":"none"}),

        # Sidebar / menu
        html.Div(children=SideBar, className="two columns", id="sidebar"),

        # main Div
        html.Div(children=MainMenu, className="nine columns", id="mainmenu"),

    ], className="row")


app.layout = serve_layout



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
@app.callback(Output('sidebar', 'children'),
              [Input('visuals-content', 'value')])

def low_level_tabs_submenus(tab):
    """
        For the second level of tabs, show different sidebar menu. Choises are: 
        Baseline Modelling, Built KPIs.
        This is implemented only for KPI tab
    """
    if tab == 'exploration':
        return 
    if tab == 'kpi':
        return KPIs.SideBar_KPIs
    if tab == 'graphs3d':
        return
    if tab == 'networks':
        return 



## When the sidebar button is clicked, collapse the div
@app.callback(Output('sidebar_collapsible_button', 'style'),
              [Input('button_collapse', 'n_clicks')],)
def button_toggle(n_clicks):
    if n_clicks % 2 == 1:
        return {'display': 'none'}
    else:
        return {'display': 'block'}

## Only exists due to a known bug in dash
@app.callback(Output("user_id", "children"),
              [Input("table", "data")],
              [State("user_id", "children")])
def debug_func(data, user_id):
    return user_id



if __name__ == "__main__":
    # TODO: Implement user_id correctly:
    # create a Redis entry with all `user_id`s that
    # joined the session and cleanup for each of them
    atexit.register(cleanup, r, "user_id")
    app.run_server(debug=True, host= '0.0.0.0')

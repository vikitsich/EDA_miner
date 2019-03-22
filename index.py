from dash import Dash
from dash.dependencies import Input, Output, Event, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

# import dash_callback_chain as chainvis

from utils import mapping, load_df, cleanup, r
from apis import twitter_connect

import pandas as pd
import base64
import datetime
import io
import atexit
import uuid
import redis

from app import app
from apps import data_view, exploration_view, analyze_view


def serve_layout():
    """
        The layout of our app needs to be inside a function
        so that every time some new session starts a new
        session_id is generated.
    """

    # TODO: append above uuid to a Redis list.
    session_id = str(uuid.uuid4())

    return html.Div(children=[

        dcc.Location(id='url', refresh=False),

        # TODO: Better implementation of sessions.
        # This generates a unique id for the session, based on which
        # one can keep his data in disk. This may need changing to
        # either using tokens or to some login form
        # TAKE A LOOK AT dcc.Store
        html.H2(session_id, id="user_id", style={"display":"none"}),

        # Sidebar / menu
        html.Div(children=[
            html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(
                open("y2d.png", 'rb').read()).decode()),
                     style={
                         'height': '150px',
                         "display": "block",
                    }),

            html.H2("Sidemenu1"),
            html.Br(),

            html.Button('Show / Hide', id='button_collapse'),
            html.Div(id='button_container', children=[
                html.Ul([
                    html.Li("I'm not padded :'("),
                    html.Li('I am padded', style={"paddingLeft":"30px"}),
                    html.Li('I am even more padded', style={"paddingLeft":"60px"}),
                ])
            ]),
            html.H2("Sidemenu2"),
            html.Button("Ich bin ein button"),
            html.H2("Sidemenu4"),
            # chainvis.CallbackChainVisualizer(id="chain"),
        ], className="two columns"),

        # main Div
        html.Div(children=[
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

            html.Div(id="high_level_tabs_content"),

            # Due to a known Dash bug, the table
            # must be present in the first layout
            html.Div(id="table_container", children=[
                dash_table.DataTable(id='table',),
            ], style={"display":"none"}),

        ], className="nine columns"),

    ], className="row")


app.layout = serve_layout
# app.scripts.config.serve_locally = True


# This is to display the callback chains
# @app.callback( Output('chain', 'dot'), [Input('chain', 'id')] )
# def show_chain(s):
#     return chainvis.dot_chain(app, ["show_chain"])



@app.callback(Output('high_level_tabs_content', 'children'),
              [Input('high_level_tabs', 'value')])
def high_level_tabs(tab):
    """
        For the first level of tabs, decide which submenu to
        return. Choices are: Data View, Exploratory Data Analysis
        and Modelling (stats, )
    """

    if tab == 'EDA':
        return exploration_view.layout
    elif tab == "modelling":
        return analyze_view.layout
    elif tab == "data":
        return data_view.layout
    else:
        return '404'


## When the sidebar button is clicked, collapse the div
@app.callback(Output('button_container', 'style'),
              [Input('button_collapse', 'n_clicks')],)
def button_toggle(n_clicks):
    if n_clicks % 2 == 1:
        return {'display': 'none'}
    else:
        return {'display': 'block'}



@app.callback(Output("user_id", "children"),
              [Input("table", "data")],
              [State("user_id", "children")])
def passing(data, user_id):
    """Only exists due to a known bug in dash"""
    return user_id




if __name__ == "__main__":
    # TODO: Implement user_id correctly:
    # create a Redis entry with all `user_id`s that
    # joined the session and cleanup for each of them
    atexit.register(cleanup, r, "user_id")
    app.run_server(debug=True, host= '0.0.0.0')

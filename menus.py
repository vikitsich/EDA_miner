"""
    This module will collect all unchanging dash components
    (buttons, sidemenus, etc) so that the code in index.py
    is cleaner and abstracted.
"""

import dash_core_components as dcc
import dash_html_components as html

import dash_table

from server import app
from utils import mapping, load_df, cleanup, r, encode_image


SideBar = [

    html.Img(id="app_logo", src=encode_image("images/y2d.png")),

    html.H2("Sidemenu1"),
    html.Br(),

    html.Button('Show / Hide', id='button_collapse', n_clicks=0),
    html.Div(id='sidebar_collapsible_button', children=[
        html.Ul([
            html.Li('Example list item'),
            html.Li('I am padded'),
        ])
    ]),
    html.H2("Sidemenu2"),
    html.Div(children=[
        html.Button("ich bin ein button"),
        html.H3("I will be replaced, per lvl2-tab")
    ], id="low_level_tabs_submenu")
]


debug = True
if debug:
    from dash.dependencies import Input, Output, State
    import dash_callback_chain as chainvis
    app.scripts.config.serve_locally = True
    SideBar += [chainvis.CallbackChainVisualizer(id="chain")]

    # This is to display the callback chains
    @app.callback( Output('chain', 'dot'), [Input('chain', 'id')] )
    def show_chain(s):
        return chainvis.dot_chain(app, ["show_chain"])


MainMenu = [

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

    html.Div(id="selected_subpage"),

    # Due to a known Dash bug, the table
    # must be present in the first layout
    html.Div(id="table_container", children=[
        dash_table.DataTable(id='table',),
    ], style={"display":"none"}),
]

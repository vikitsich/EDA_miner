from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import dash_table
import dash_bootstrap_components as dbc

import pandas as pd
import datetime
import pickle
import quandl

from server import app
from utils import r, load_df, pretty_print_tweets



def get_available_choices(redisConn, user_id):

    results = {
        "twitter_api": redisConn.get(f"{user_id}_twitter_api_handle"),
        "gsheets_api": redisConn.get(f"{user_id}_gsheets_api_data"),
        "user_data": redisConn.get(f"{user_id}_user_dataframe"),
        "reddit_api": redisConn.get(f"{user_id}_reddit_handle"),
    }

    quandl_datasets = [x.decode() for x in redisConn.keys(f"{user_id}_quandl_*")]
    results.update({"_".join(q.split("_")[1:]):q
                    for q in quandl_datasets})

    options=[
        {'label': k, 'value': k}
        for k,v in results.items() if v is not None
    ]
    if len(options) < 1:
        options = [{'label': "No uploaded data yet", 'value': "no_data"}]

    return options, results

def get_data(api_data_choice, user_id):
    if api_data_choice == "gsheets_api":
        df = r.get(f"{user_id}_gsheets_api_data")
        df = pickle.loads(df)

    # uploaded data
    elif api_data_choice == "user_data":
        df =  load_df(r, user_id)

    else:
        df = None

    return df


def View_Options(user_id):

    options, results = get_available_choices(r, user_id)
    available_choices = html.Div(dcc.Dropdown(options=options,
                                              id="api_data_choice"),
                                 style={"display":"inline-block",
                                        "width":"30%"})

    return [
        html.Br(),

        available_choices,

        dcc.Input(id="dataset_name", style={"display":"none"}),

        html.Div(id="table_view", children=[
            dash_table.DataTable(id='table'),
        ]),
    ]



@app.callback(Output("dataset_name", "style"),
              [Input("api_data_choice", "value")],
              [State("user_id", "children")])
def display_subtaset_choices(api_data_choice, user_id,):
    if api_data_choice == "quandl_api":
        return {"display":"inline"}
    else:
        return {"display":"none"}


@app.callback(Output("table_view", "children"),
              [Input("api_data_choice", "value")],
              [State("user_id", "children")])
def render_table(api_data_choice, user_id):

    if api_data_choice == "twitter_api":
        api = r.get(f"{user_id}_twitter_api_handle")

        return pretty_print_tweets(api, 5)

    elif api_data_choice == "reddit_api":

        api = r.get(f"{user_id}_reddit_handle")

        return [
            html.H4("Write the name of a subreddit:"),
            dcc.Input(id="subreddit_choice", type="text", value="",),
            html.Button("Gimme dem reddits", id="reddit_submit"),

            html.Br(),
            html.Br(),
            html.Div(id="subreddit_posts"),
        ]

    elif (api_data_choice is not None) and ("quandl" in api_data_choice):

        # TODO: this should go to the get_data function
        df = pickle.loads(r.get(f"{user_id}_{api_data_choice}"))

    else:
        df = get_data(api_data_choice, user_id)

    if df is None:
        return [html.H4("Nothing to display")]


    df = df[df.columns[:10]]

    # if not, return this table
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



@app.callback(Output("subreddit_posts", "children"),
              [Input("reddit_submit", "n_clicks")],
              [State("subreddit_choice", "value"),
               State("user_id", "children")])
def display_reddit_posts(n_clicks, subreddit_choice, user_id):

    if n_clicks is not None and n_clicks >=1:

        if subreddit_choice is not None:

            api = pickle.loads(r.get(f"{user_id}_reddit_handle"))
            subreddit = api.subreddit(subreddit_choice)

            posts = [
                html.Div([
                    dbc.Card([
                        dbc.CardHeader([
                            html.H4(post.title),
                            html.A("view at reddit", href=post.permalink),
                        ]),
                        dbc.CardBody([
                            dbc.CardTitle(f"Written by {post.author.name}, score: {post.score}"),
                            dbc.CardText(dcc.Markdown(post.selftext),),
                        ]),
                    ]),
                    html.Br(),
                ]) for post in subreddit.hot(limit=5)
            ]

            return posts

        else:
            return [html.H4("No subreddit choice")]

    else:

        return [html.H4("No reddit data to display.")]

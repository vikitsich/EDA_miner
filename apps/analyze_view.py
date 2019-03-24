from dash.dependencies import Input, Output, Event, State
import dash_core_components as dcc
import dash_html_components as html

from app import app
from utils import mapping, load_df, r

import pandas as pd
import base64
import datetime

## TODO: Port internal functionality to apps.analyze_tabs

layout = html.Div(children=[
    html.Div(children=[

        dcc.Tabs(id="analyze_tabs", value="", children=[
            dcc.Tab(label='Regression', value='regression',
                    id="regression"),
            dcc.Tab(label='Classification', value='classification',
                    id="classification"),
            dcc.Tab(label='Clustering', value='clustering',
                    id="clustering"),
            dcc.Tab(label='Econometrics', value='econometrics',
                    id="econometrics"),
        ]),
    ]),
    html.Div(id="model-content"),
])


## Subtabs
@app.callback(Output('model-content', 'children'),
              [Input('analyze_tabs', 'value')],
              [State("user_id", "children")])
def tab_subpages(tab, user_id):
    """
        This callback is called when a level two tab
        is selected in the analysis menu. Accordingly,
        it returns an interface to provide further
        specifications for the model.
    """

    df = load_df(r, user_id)
    if df is None:
        columns = ["No data are uploaded"]
    else:
        columns = df.columns

    if tab == 'regression':
        available_choices = dcc.Dropdown(
            options=[
                {'label': 'Linear Regression', 'value': 'linr'},
                {'label': 'Support Vector Regressor', 'value': 'svr'},
                {'label': 'Decision Tree Regressor', 'value': 'dtr'}
            ], value='linr', id="algo_choice")

    elif tab == "classification":
        available_choices = dcc.Dropdown(
            options=[
                {'label': 'Logistic Regression', 'value': 'logr'},
                {'label': 'XGBoost', 'value': 'xgb'},
            ], value='logr', id="algo_choice")

    elif tab == "clustering":
        available_choices = dcc.Dropdown(
            options=[
                {'label': 'DBSCAN', 'value': 'dbscan'},
                {'label': 'K-Means Clustering', 'value': 'kmc'},
            ], value='kmc', id="algo_choice")

    elif tab == "econometrics":
        return [html.H4("Not implement yet..."),]

    else:
        return [html.H4("Click on a subtab..."),]



    # Unless we have clustering, we should also have
    # a target Y variable
    if tab != "clustering":
        Y_Var = [
            html.H4("Target:"),
            dcc.Dropdown(
                options=[
                    {'label': col, 'value': col}
                    for col in columns],
                id="yvar",
        ),]
    else:
        Y_Var = [
            html.H4("Target Not applicable"),
            dcc.Dropdown(
                options=[
                    {'label': col, 'value': col}
                    for col in columns],
                id="yvar",
                style={"display": "none"}
        ),]

    return [html.Div(children=[
            html.Br(),
            html.Div(children=[
                html.H4("Model:"),
                available_choices,
                html.H4("Variables:"),
                dcc.Dropdown(
                    options=[
                        {'label': col, 'value': col}
                        for col in columns],
                    multi=True,
                    id="xvar",
                ),
                *Y_Var,
                html.Br(),
                html.Div(id="model_choice"),
            ], className="four columns"),
        ])]

## Create the "fit" button
@app.callback(Output('model_choice', 'children'),
              [Input('algo_choice', 'value')])
def prepare_model(choice):
    """
        This creates a button that can later be clicked to
        fit the selected model.
    """
    return [
        html.Button(f"Fit {choice}", id="fit_model", n_clicks=0),
        html.Div(id="model_results",),
    ]


## Callback on "fit-button" that performs the fitting
@app.callback(Output('model_results', 'children'),
              [Input('fit_model', 'n_clicks')],
              [State("user_id", "children"),
               State("xvar", "value"),
               State("yvar", "value"),
               State("algo_choice", "value")])
def fit_model(n_clicks, user_id, xcols, ycols, model_choice):
    """
        This function takes the user-specified values when
        the `fit` button is clicked and
    """

    if n_clicks >= 1:

        df = load_df(r, user_id)

        # TODO: add **kwargs to the models
        # This dict returns an sklearn model instance
        model = mapping[model_choice]()


        # take selected columns, cast to arrays
        # TODO: maybe do some preprocessing here?
        xcols = df[xcols].values

        if ycols is not None:
            ycols = df[ycols].values

        try:
            model.fit(xcols, ycols)
        except:
            return [html.H4("Your model choice is wrong")]

        return html.H4(f"Model score: {model.score(xcols, ycols)}")

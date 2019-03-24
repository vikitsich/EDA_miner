import dash_core_components as dcc
import dash_html_components as html

import dash_table

import pandas as pd
import datetime



def View_Options(df):

    if df is None:
        # if you don't have any tables stored in
        #  memory prompt the user to upload one
        return [html.H3("Upload data first, dummy...")]

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

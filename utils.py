from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBClassifier
from sklearn.cluster import KMeans, DBSCAN

import dash_html_components as html

import pandas as pd
import base64
import datetime
import io
import atexit
import uuid
import redis

r = redis.Redis(host="localhost", port=6379, db=0)


mapping = {
    "logr": LogisticRegression,
    "linr": LinearRegression,
    "xgb": XGBClassifier,
    "dtr": DecisionTreeRegressor,
    "svr": SVR,
    "kmc": KMeans,
    "dbscan": DBSCAN,
}

# TODO: Implement user_id correctly:
# create a Redis entry with all `user_id`s that
# joined the session and cleanup for each of them
def cleanup(redisConn, user_id):
    """
        Deletes everything stored in the redis server.
    """
    redisConn.delete(f"{user_id}_user_dataframe")


def load_df(redisConn, user_id):
    answer = redisConn.get(f"{user_id}_user_dataframe")
    if answer is not None:
        answer = pd.read_msgpack(answer)

    return answer


# TODO: this function needs to be reviewed because
# it doesn't work correctly on error (i.e. returns a Div).
def parse_contents(contents, filename, date, user_id):
    """
        After decoding the uploaded file, handle any
        remaining operations here. This was stolen
        from the dash docs.
    """

    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    # Store to redis for caching
    r.set(f"{user_id}_user_dataframe", df.to_msgpack(compress='zlib'))

    return html.Div([
        "Data uploaded sucessfully."
    ])

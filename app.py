from dash import Dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',]

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config['suppress_callback_exceptions']=True

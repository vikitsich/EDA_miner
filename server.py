from dash import Dash

external_stylesheets = []

app = Dash(__name__, external_stylesheets=external_stylesheets)

# Only to be used in production, safely ignore for now
server = app.server

# Any other configurations for the Dash/Flask server go here
app.config['suppress_callback_exceptions'] = True

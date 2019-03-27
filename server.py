from dash import Dash

external_stylesheets = ["https://use.fontawesome.com/releases/v5.8.1/css/all.css"]

app = Dash(__name__, external_stylesheets=external_stylesheets)

# Only to be used in production, safely ignore for now
server = app.server

# Any other configurations for the Dash/Flask server go here
app.config['suppress_callback_exceptions'] = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>EDA Miner</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        <div class="app0">{%app_entry%}</div>

        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

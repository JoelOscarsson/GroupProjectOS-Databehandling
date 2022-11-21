import dash
from dash.dependencies import Output, Input
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly_express as px

# Importing from all modules and classes from another py file.
# Then creating a df that has been processed by the modules load_data and get_data_path

from load_data2 import get_data_path, load_data, DataProcessing
df = DataProcessing(load_data(get_data_path))


# Creating dash app
app = dash.Dash(__name__)

app.layout = html.Main([
    # Headers or titles
    html.H1("120 Years of OS history"),
    html.H2("Exploratory graph"),
    # Dropdown är fältet man kan klicka på
    dcc.Dropdown(id = "os-dropdown", options= [{"label": name, }])    
])



if __name__ == "__main__":
    # run app if script is run from main
    app.run_server(debug=True)
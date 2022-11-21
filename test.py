import dash
from dash.dependencies import Output, Input
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly_express as px


from data_processing import get_data_path, load_data, DataProcessing
df = DataProcessing(load_data(get_data_path()))




country_options = [
    {"label": "China", "value": "CHN"},
    {"label": "All countries", "value": "all"},




# Creating dash app
app = dash.Dash(__name__)

# Creating layout
app.layout = html.Main([
    html.H1("120 years of Olympic Games"),
    html.P("Choose something to visualize"),
    # id that we can reference the dropdown to
    dcc.Dropdown(id = "explorative dropdown",
    options = [{"label": "Sports (Top 10)", "value": "sports_top10"}]

])


if __name__ == "__main__":
    app.run_server(debug = True)

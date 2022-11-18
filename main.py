# add selection of preselected diagrams/themes: chooses called function/methods
# in those selected themes, the available options can change?
# clickable box to show average of the measurement (all countries)

# add selection of country China or All
# add selection of either our selection of sports, or top China sports, or all sports
# add selection of what to sort on
# add some bubbles? some other diagrams?
# reset button?

import dash
from dash.dependencies import Output, Input
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly_express as px

from data_processing import get_data_path, load_data, DataProcessing
df = DataProcessing(load_data(get_data_path()))

country_options = [
    {"label": "China", "value": "China"},
    {"label": "All countries", "value": "All"},
]

plot_options = [{"label": i, "value": i} for i in ["line", "bar", "scatter"]]

app = dash.Dash(__name__)

app.layout = html.Main([
    html.H1("120 years of OS history"),
    dcc.RadioItems(
        id = "country-radio",
        options = country_options,
        value = "All",
    ),   
    html.P("Choose chart"),
    dcc.Dropdown(
        id = "chart-dropdown",
        value = "explorative_all",
    ),    
    html.P("Choose x"),
    dcc.Dropdown(
        id = "x-dropdown",
        # options = x_options_dropdown,
        value = "Games",
    ),
    html.P("Choose y"),    
    dcc.Dropdown(
        id = "y-dropdown",
        # options = y_options_dropdown,
        value = "Medal",
    ),
    html.P("Choose grouping/color"),    
    dcc.Dropdown(
        id = "grouping-dropdown",
        # options = grouping_options_dropdown,
        # value = "Sex",
    ),
    dcc.RadioItems(id = "plot-radio", options = plot_options, value = "bar"),
    dcc.Graph(id = "os-graph"),
    ]
)

@app.callback(
    Output("chart-dropdown", "options"),
    Input("country-radio", "value"),
)
def chart_filter(country):
    if country == "China":
        chart_options = [
                {"label": "Explorative", "value": "explorative"},
                {"label": "China2", "value": "china2"},  
        ]
    else:
        chart_options = [
                {"label": "Explorative", "value": "explorative"},
                {"label": "All2", "value": "all2"},  
        ]        
    return chart_options


@app.callback(
    Output("x-dropdown", "options"),
    Output("y-dropdown", "options"),
    Output("grouping-dropdown", "options"),
    Input("chart-dropdown", "value")
)
def chart_options_filter(chart):
    if chart == "china2":
        x_options_dropdown = [
            {"label": "test", "value": "test"}
        ]
    else:  
        x_options_dropdown = [
            {"label": "Olympic games", "value": "Games"},
            {"label": "Sports", "value": "Sport"},
            {"label": "Years", "value": "Year"},
            {"label": "Age", "value": "Age"},
            {"label": "Height", "value": "Height"},    
            {"label": "Weight", "value": "Weight"}
        ]
    y_options_dropdown = [
        {"label": "Participants", "value": "ID"},
        {"label": "Number of medals", "value": "Medal"},
        {"label": "Age", "value": "Age"},
        {"label": "Height", "value": "Height"},
        {"label": "Weight", "value": "Weight"}
    ]
    grouping_options_dropdown = [
        {"label": "Sports", "value": "Sport"},
        {"label": "Sex", "value": "Sex"},
        {"label": "Season", "value": "Season"},
    ]    
    return x_options_dropdown, y_options_dropdown, grouping_options_dropdown


@app.callback(
    Output("os-graph", "figure"),
    Input("country-radio", "value"),
    Input("chart-dropdown", "value"),
    Input("x-dropdown", "value"),
    Input("y-dropdown", "value"),
    Input("grouping-dropdown", "value"),
    Input("plot-radio", "value"),
)
def update_graph(country, chart, x, y, grouping, plot):

    if chart



    # if chart == "joel_charts":
        # return df.joel_plots(argument)
    if country == "China":
        df = DataProcessing(load_data(get_data_path())).noc("CHN")
    else: 
        df = DataProcessing(load_data(get_data_path()))

    return df.olymics_plot_df(x, y, grouping=grouping, plot=plot)



if __name__ == "__main__":
    app.run_server(debug = True)
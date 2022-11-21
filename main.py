# add selection of preselected diagrams/themes: chooses called function/methods
# in those selected themes, the available options can change

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
    {"label": "China", "value": "CHN"},
    {"label": "All countries", "value": "all"},
]

sort_options = [
    {"label": "Sports", "value": "sports"},
    {"label": "Sports (Top 10)", "value": "sports_top10"},
    {"label": "Countries", "value": "countries"},
    {"label": "Countries (Top 10)", "value": "countries_top10"}    
]

x_options_dropdown = [
    {"label": "Olympic games", "value": "Games"},
    {"label": "Countries", "value": "NOC"},
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

plot_options = [{"label": i, "value": i} for i in ["line", "bar", "scatter"]]

app = dash.Dash(__name__)

app.layout = html.Main([
    html.H1("120 years of OS history"),

    html.H2("Exploratory graph"),

    dcc.RadioItems(
        id = "country-radio",
        options = country_options,
        value = "CHN",
    ),
    html.P("Sort by medal count"),
    dcc.RadioItems(
        id = "sort-radio",
        options = sort_options,
    ),      
    # html.P("Choose chart"),
    # dcc.Dropdown(
    #     id = "chart-dropdown",
    #     value = "explorative_all",
    # ),    
    html.P("Choose x"),
    dcc.Dropdown(
        id = "x-dropdown",
        options = x_options_dropdown,
        value = "Games",
    ),
    html.P("Choose y"),    
    dcc.Dropdown(
        id = "y-dropdown",
        options = y_options_dropdown,
        value = "ID",
    ),
    html.P("Choose grouping/color"),    
    dcc.Dropdown(
        id = "grouping-dropdown",
        options = grouping_options_dropdown,
        # value = "Sex",
    ),
    dcc.RadioItems(id = "plot-radio", options = plot_options, value = "bar"),
    dcc.Graph(id = "exploratory-graph"),
    html.H2("test"),
    dcc.Graph(id = "new-graph"),

    ]
)



@app.callback(
    Output("exploratory-graph", "figure"),
    Input("country-radio", "value"),
    Input("sort-radio", "value"), 
    # Input("chart-dropdown", "value"),
    Input("x-dropdown", "value"),
    Input("y-dropdown", "value"),
    Input("grouping-dropdown", "value"),
    Input("plot-radio", "value"),
)

def update_graph(country, sort, x, y, grouping, plot):

    df = DataProcessing(load_data(get_data_path())).noc_filter(country)

    if sort:
        df.sort_plot(sort)

    return df.olymics_plot_df(x, y, grouping=grouping, plot=plot)

@app.callback(
    Output("top10-country-medals", "figure"),
    Output("age-distribution-athletes", "figure"),
    Output("sex-distribution", "figure"),
    Input("num_dropdown", "value"),
    Input("num_dropdown", "value"),
    Input("num_dropdown", "value"),
)

def update_graph2(num, df):
    df = DataProcessing(load_data(get_data_path()))

    fig = df.top_10_countries_medals(num)
    fig2 = df.age_distribution_athletes()
    fig3 = df.sex_distribution_athletes()

    return fig, fig2, fig3


if __name__ == "__main__":
    app.run_server(debug = True)


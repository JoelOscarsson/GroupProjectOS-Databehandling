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
# Radio options
medal_list = "Gold Silver Bronze Total".split()
medal_options = [{'label': medal, 'value': medal} for medal in medal_list]

sport_list = df.sort_plot['sport'].unique().tolist()
sport_list.append("All Sports")
sport_list.sort()
sport_options_dropdown = [
    {'label':sport, 'value': sport} 
    for sport in sport_list
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
     dbc.Row(className='mt-4', children=[
        dbc.Col(
            # responsivity
            html.P("Choose sport:"), xs="12", sm="12", md="6", lg="4", xl={"size": 1, "offset": 1},
            className="mt-1"
        ),
        dbc.Col(
            dcc.Dropdown(id='sport-dropdown', className='',
                         options=sport_options_dropdown,
                         value='All sports',
                         placeholder='All sports'), xs="12", sm="12", md="12", lg="4", xl="3"),

        dbc.Col([
            dbc.Card([
                dcc.RadioItems(id='medal-radio', className="m-1",
                                  options=medal_options,
                                  value='Total'
                               ),
            ])
        ], xs="12", sm="12", md="12", lg='4', xl="3"),
    ]),

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

# @app.callback(
#     Output("chart-dropdown", "options"),
#     Input("country-radio", "value"),
# )
# def chart_filter(country):
#     if country == "China":
#         chart_options = [
#                 {"label": "Explorative", "value": "explorative"},
#                 {"label": "China2", "value": "china2"},  
#         ]
#     else:
#         chart_options = [
#                 {"label": "Explorative", "value": "explorative"},
#                 {"label": "All2", "value": "all2"},  
#         ]        
#     return chart_options


# @app.callback(
#     Output("x-dropdown", "options"),
#     Output("y-dropdown", "options"),
#     Output("grouping-dropdown", "options"),
#     Input("chart-dropdown", "value")
# )
# def chart_options_filter(chart):
#     if chart == "china2":
#         x_options_dropdown = [
#             {"label": "test", "value": "test"}
#         ]
#     else:  
#         x_options_dropdown = [
#             {"label": "Olympic games", "value": "Games"},
#             {"label": "Countries", "value": "NOC"},
#             {"label": "Sports", "value": "Sport"},
#             {"label": "Years", "value": "Year"},
#             {"label": "Age", "value": "Age"},
#             {"label": "Height", "value": "Height"},    
#             {"label": "Weight", "value": "Weight"}
#         ]
#     y_options_dropdown = [
#         {"label": "Participants", "value": "ID"},
#         {"label": "Number of medals", "value": "Medal"},
#         {"label": "Age", "value": "Age"},
#         {"label": "Height", "value": "Height"},
#         {"label": "Weight", "value": "Weight"}
#     ]
#     grouping_options_dropdown = [
#         {"label": "Sports", "value": "Sport"},
#         {"label": "Sex", "value": "Sex"},
#         {"label": "Season", "value": "Season"},
#     ]    
#     return x_options_dropdown, y_options_dropdown, grouping_options_dropdown


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


if __name__ == "__main__":
    app.run_server(debug = True)
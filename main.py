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

g1_country_options = [
    {"label": "China", "value": "CHN"},
    {"label": "All countries", "value": "all"},
]

g1_group_options = [
    {"label": "Season", "value": "Season"},
    {"label": "Sex", "value": "Sex"},
]

g1_y_options = [
    {"label": "Number of participants", "value": "ID"},
    {"label": "Number of medals", "value": "Medal"},
    {"label": "Number of medals per participant", "value": "per"},
]

g1_season_options = [
    {"label": "Summer", "value": "Summer"},
    {"label": "Winter", "value": "Winter"}
]

g2_dist_options = [
    {"label": "Age", "value": "Age"},
    {"label": "Height", "value": "Height"},
    {"label": "Weight", "value": "Weight"},
]

g2_plot_options = [
    {"label": "Histogram", "value": "hist"},
    {"label": "Violin plot", "value": "violin"},
    {"label": "Violin plot: sports", "value": "sports"}
]

g3_plot_options = [
    {"label": "Bar", "value": "bar"},
    {"label": "Line", "value": "line"}
]

sports_list = list(df.filter_noc("CHN").df.groupby("Sport")["Medal"].count().sort_values(ascending = False).head(29).index)
sports_list.insert(0, "All")
g3_sports_options = [{"label": i, "value": i} for i in sports_list]


app = dash.Dash(__name__)

app.layout = html.Main([
    html.H1("120 years of OS history"),

    html.H2("China: OS history"),

    dcc.RadioItems(
        id = "g1-country-radio",
        options = g1_country_options,
        value = "CHN",
    ),
    html.P("Group by:"),    
    dcc.RadioItems(
        id = "g1-group-radio",
        options = g1_group_options,
        value = "Season",
    ),
    html.P("Choose y-axis"),    
    dcc.RadioItems(
        id = "g1-y-radio",
        options = g1_y_options,
        value = "ID",
    ),
    dcc.Graph(id = "g1-china-history-graph"),
    dcc.RadioItems(
        id = "g1-season-radio",
        options = g1_season_options
    ),    
    html.H2("China: Distributions and sex differences"),
    html.P("Distributions of:"),     
    dcc.RadioItems(
        id = "g2-dist-radio",
        options = g2_dist_options,
        value = "Age"
    ),
    html.P("Plot:"),     
    dcc.RadioItems(
        id = "g2-plot-radio",
        options = g2_plot_options,
        value = "hist"        
    ),    
    dcc.Graph(id = "g2-china-dist-graph"),
    dcc.Slider(
        id="g2-sports-slider",
        min=1,
        max=10,
        # marks=,
        value=6,
        step=1,
    ),
    html.H2("China: Top sports"),
    dcc.RadioItems(
        id = "g3-plot-radio",
        options = g3_plot_options,
        value = "bar"        
    ),
    dcc.Dropdown(
        id="g3-sports-dropdown",
        options=g3_sports_options,
        value = "All"
    ),       
    dcc.Graph(id = "g3-china-sports-graph"),
    # dcc.RadioItems(
    #     id = "g3-season-radio",
    #     options = g1_season_options
    # ),
 
    ]
)


@app.callback(
    Output("g1-china-history-graph", "figure"),
    Input("g1-country-radio", "value"),
    Input("g1-group-radio", "value"),
    Input("g1-y-radio", "value"),
    Input("g1-season-radio", "value")    
)
def update_graph1(country, grouping, y, season):
    df = DataProcessing(load_data(get_data_path())).filter_noc(country)

    groups = list(df.df[grouping].unique())

    barmode = "relative"
    # default colors: https://plotly.com/python/discrete-color/
    colors = {"Summer": "#d95f02", "Winter": "#7570b3", "M": "#636EFA", "F": "#EF553B"}

    if grouping == "Sex":
        barmode = "group"
        if season:
            df = df.filter_season(season)

    if y == "per":
        df = df.proportion_plot("Games", "Medal", "ID", grouping = grouping)
        fig = px.bar(df.df, x = "Games", y = groups, barmode = barmode, color_discrete_map=colors)
    else:
        df = df.basic_plot("Games", y, grouping = grouping)
        fig = px.bar(df.df, x = "Games", y = groups, barmode = barmode, color_discrete_map=colors)

    return fig

@app.callback(
    Output("g2-china-dist-graph", "figure"),
    Input("g2-dist-radio", "value"),
    Input("g2-plot-radio", "value"),
    Input("g2-sports-slider", "value"),
)
def update_graph2(dist, plot, slider):
    df = DataProcessing(load_data(get_data_path())).filter_noc("CHN")

    if plot == "hist":
        df = df.basic_plot(dist, "ID", grouping = "Sex")
        fig = px.histogram(df.df, x = dist, y = ["M", "F"], nbins = 50, barmode = "overlay", histnorm='probability')
    elif plot == "violin":
        fig = px.violin(df.df, x = "Sex", y = dist, color = "Sex")
        fig.update_traces(meanline_visible=True)
    elif plot == "sports":
        df = df.filter_top("Sport", "ID", slider)
        fig = px.violin(df.df, x = "Sex", y = dist, color = "Sport")
        fig.update_traces(meanline_visible=True)

    return fig

@app.callback(
    Output("g3-china-sports-graph", "figure"),
    Input("g3-plot-radio", "value"),
    # Input("g3-season-radio", "value"),
    Input("g3-sports-dropdown", "value")
)
def update_graph3(plot, sport):
    df = DataProcessing(load_data(get_data_path())).filter_noc("CHN")
    # if season:
        # df = df.filter_season(season)

    if plot == "bar":
        if sport == "All":
            df = df.basic_plot("Sport", "Medal", grouping = "Sex")

            df.df["Total"] = df.df["M"] + df.df["F"]
            df.df = df.df[df.df["Total"] >= 5]
            df.df = df.df.sort_values(by = "Total", ascending = False)

            fig = px.bar(df.df, x = "Sport", y = ["M", "F"])
        else:
            df.df = df.df[df.df["Sport"] == sport]
            df = df.basic_plot("Medal", "ID", grouping = "Sex")
            df.df = df.df.set_index("Medal").loc[["Gold", "Silver", "Bronze"]].reset_index()
            fig = px.bar(df.df, x = "Medal", y = ["M", "F"], barmode = "group")


    elif plot == "line":
        df = df.df[df.df["Year"] > 1983]
        df = DataProcessing(df)
        if sport == "All":
            df = df.filter_top("Sport", "Medal", 5)
            fig = df.basic_plot("Games", "Medal", grouping = "Sport", plot = "line")
        else:
            df.df = df.df[df.df["Sport"] == sport]
            fig = df.basic_plot("Games", "Medal", plot = "line")


        # df = df["Sport"]
        # df = df.filter_top("Sport", "Medal", 5)

        fig.update_layout(title_text = "Chinese medals per OS by sport")

    return fig

if __name__ == "__main__":
    app.run_server(debug = True)
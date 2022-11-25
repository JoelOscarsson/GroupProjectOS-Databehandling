import dash
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly_express as px
from layout import Layout
from data_processing import get_data_path, load_data, DataProcessing


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.MATERIA],  # looks in assets map by default
    # makes responsivity possible (different web browser sizes)
    meta_tags=[dict(name="viewport", content="width=device-width, initial-scale=1.0")],
    # suppress_callback_exceptions=True
)

df = DataProcessing(load_data(get_data_path()))
df_orig = df

app.layout = Layout(df).layout()

server = app.server


@app.callback(
    Output("g1-china-history-graph", "figure"),
    Input("g1-country-radio", "value"),
    Input("g1-group-radio", "value"),
    Input("g1-y-radio", "value"),
    Input("g1-season-radio", "value"),
)
def update_graph1(country, grouping, y, season):
    df = df_orig.filter_noc(country)
    # df = DataProcessing(load_data(get_data_path())).filter_noc(country)

    groups = list(df.df[grouping].unique())

    barmode = "relative"
    # default colors: https://plotly.com/python/discrete-color/
    colors = {"Summer": "#d95f02", "Winter": "#7570b3", "M": "#636EFA", "F": "#EF553B"}

    if grouping == "Sex":
        barmode = "group"
        if season:
            df = df.filter_season(season)

    if y == "per":
        df = df.proportion_plot("Games", "Medal", "ID", grouping=grouping)
        fig = px.bar(
            df.df,
            x="Games",
            y=groups,
            barmode=barmode,
            color_discrete_map=colors,
            labels={"variable": grouping, "value": "Proportion"},
        )
    else:
        df = df.basic_plot("Games", y, grouping=grouping)
        fig = px.bar(
            df.df,
            x="Games",
            y=groups,
            barmode=barmode,
            color_discrete_map=colors,
            labels={"variable": grouping, "value": "Count"},
        )

    return fig


@app.callback(
    Output("g2-china-dist-graph", "figure"),
    Input("g2-dist-radio", "value"),
    Input("g2-plot-radio", "value"),
    Input("g2-sports-slider", "value"),
)
def update_graph2(dist, plot, slider):
    # df = DataProcessing(load_data(get_data_path())).filter_noc("CHN")
    df = df_orig.filter_noc("CHN")

    if plot == "hist":
        df = df.basic_plot(dist, "ID", grouping="Sex")
        fig = px.histogram(
            df.df,
            x=dist,
            y=["M", "F"],
            nbins=50,
            barmode="overlay",
            histnorm="probability",
            labels={"fraction of sum of value": "Fraction", "variable": "Sex"},
        )
    elif plot == "violin":
        fig = px.violin(df.df, x="Sex", y=dist, color="Sex")
        fig.update_traces(meanline_visible=True)
    elif plot == "sports":
        df = df.filter_top("Sport", "ID", slider)
        fig = px.violin(df.df, x="Sex", y=dist, color="Sport")
        fig.update_traces(meanline_visible=True)

    return fig


@app.callback(
    Output("g3-china-sports-graph", "figure"),
    Input("g3-plot-radio", "value"),
    # Input("g3-season-radio", "value"),
    Input("g3-sports-dropdown", "value"),
)
def update_graph3(plot, sport):
    # df = DataProcessing(load_data(get_data_path())).filter_noc("CHN")
    df = df_orig.filter_noc("CHN")

    if plot == "bar":
        labels = {"value": "Medal count", "variable": "Sex"}
        if sport == "All":
            df = df.basic_plot("Sport", "Medal", grouping="Sex")

            df.df["Total"] = df.df["M"] + df.df["F"]
            df.df = df.df[df.df["Total"] >= 5]
            df.df = df.df.sort_values(by="Total", ascending=False)

            fig = px.bar(df.df, x="Sport", y=["M", "F"], labels=labels)
        else:
            df.df = df.df[df.df["Sport"] == sport]
            df = df.basic_plot("Medal", "ID", grouping="Sex")
            df.df = (
                df.df.set_index("Medal").loc[["Gold", "Silver", "Bronze"]].reset_index()
            )
            fig = px.bar(
                df.df,
                x="Medal",
                y=["M", "F"],
                barmode="group",
                labels=labels,
                title=sport,
            )

    elif plot == "line":
        df = df.df[df.df["Year"] > 1983]
        df = DataProcessing(df)
        if sport == "All":
            df = df.filter_top("Sport", "Medal", 5)
            fig = df.basic_plot("Games", "Medal", grouping="Sport", plot="line")
        else:
            df.df = df.df[df.df["Sport"] == sport]
            fig = df.basic_plot("Games", "Medal", plot="line", title=sport)

        # df = df["Sport"]
        # df = df.filter_top("Sport", "Medal", 5)

        # fig.update_layout(title_text="Chinese medals per OS by sport")

    return fig


@app.callback(
    Output("top10-country-medals", "figure"),
    Input("num_dropdown", "value"),
)
def update_graph2(num):
    # df = DataProcessing(load_data(get_data_path()))
    df = df_orig

    fig = df.top_10_countries_medals(num)
    return fig


@app.callback(
    Output("age-distribution-athletes", "figure"),
    Input("dist-radio", "value"),
)
def update_graph2(dist):
    # df = DataProcessing(load_data(get_data_path()))
    df = df_orig

    fig = df.age_distribution_athletes(dist)
    return fig


@app.callback(
    Output("sex-distribution", "figure"),
    Input("dist2-radio", "value"),
)
def update_graph2(dist2):
    # df = DataProcessing(load_data(get_data_path()))
    df = df_orig

    fig = df.sex_distribution_athletes(dist2)
    return fig


@app.callback(
    Output("a1-sport-medals-graph", "figure"),
    Input("a1-sport-radio", "value"),
    Input("a1-plot-radio", "value"),
)
def update_graph2(sport, plot):
    # df = DataProcessing(load_data(get_data_path()))
    df = df_orig

    fig = df.sports_medal_plot(sport, plot)
    return fig


@app.callback(
    Output("a2-dist-graph", "figure"),
    Input("a2-sport-radio", "value"),
)
def update_graph2(sport):
    # df = DataProcessing(load_data(get_data_path()))
    df = df_orig

    fig = df.sports_dist_plot(sport)
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)

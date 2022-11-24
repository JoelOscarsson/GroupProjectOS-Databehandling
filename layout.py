from dash import html, dcc
from data_processing import DataProcessing
import dash_bootstrap_components as dbc


class Layout:
    def __init__(self, df: DataProcessing) -> None:
        self._df = df

        self._g1_country_options = [
            {"label": "China", "value": "CHN"},
            {"label": "All countries", "value": "all"},
        ]

        self._g1_group_options = [
            {"label": "Season", "value": "Season"},
            {"label": "Sex", "value": "Sex"},
        ]

        self._g1_y_options = [
            {"label": "Number of participants", "value": "ID"},
            {"label": "Number of medals", "value": "Medal"},
            {"label": "Number of medals per participant", "value": "per"},
        ]

        self._g1_season_options = [
            {"label": "Summer", "value": "Summer"},
            {"label": "Winter", "value": "Winter"},
        ]

        self._g2_dist_options = [
            {"label": "Age", "value": "Age"},
            {"label": "Height", "value": "Height"},
            {"label": "Weight", "value": "Weight"},
        ]

        self._g2_plot_options = [
            {"label": "Histogram", "value": "hist"},
            {"label": "Violin plot", "value": "violin"},
            {"label": "Violin plot: sports", "value": "sports"},
        ]

        self._g3_plot_options = [
            {"label": "Ranked medal counts", "value": "bar"},
            {"label": "History per sport", "value": "line"},
        ]

        sports_list = list(
            self._df.filter_noc("CHN")
            .df.groupby("Sport")["Medal"]
            .count()
            .sort_values(ascending=False)
            .head(29)
            .index
        )
        sports_list.insert(0, "All")
        self._g3_sports_options = [{"label": i, "value": i} for i in sports_list]

        self._num_options = [
            {"label": 5, "value": 5},
            {"label": 10, "value": 10},
            {"label": 15, "value": 15},
            {"label": 20, "value": 20},
        ]

        self._dist_options = [
            {"label": "Age", "value": "Age"},
            {"label": "Height", "value": "Height"},
            {"label": "Weight", "value": "Weight"},
        ]                
        self._dist2_options = [
            {"label": "Sex", "value": "Sex"},
            {"label": "Sport", "value": "Sport"},
        ]               

        self._a1_sport_options = [
            {"label": "Football", "value": "Football"},
            {"label": "Basketball", "value": "Basketball"},
            {"label": "Gymnastics", "value": "Gymnastics"},
        ]               
        self._a1_plot_options = [
            {"label": "All", "value": "All"},
            {"label": "Divided by sex", "value": "Sex"},
        ]          
        self._a2_sport_options = [
            {"label": "Football", "value": "Football"},
            {"label": "Basketball", "value": "Basketball"},
            {"label": "Gymnastics", "value": "Gymnastics"},
        ]   

    def layout(self):
        return dbc.Container(
            [
                # dbc.Card(
                # dbc.CardBody(html.H1("120 years of OS history")), className="mt-3"
                # ),
                dbc.Row(html.H1("120 years of OS history"), className="mt-3"),
                dbc.Card(
                    dbc.CardBody(html.H2("China: OS history")),
                    className="mt-3",
                ),
                dbc.Row(
                    className="mt-4",
                    children=[
                        dbc.Col(html.P("Choose country:"), className="mt-1"),
                        dbc.Col(
                            dcc.Dropdown(
                                id="g1-country-radio",
                                options=self._g1_country_options,
                                value="CHN",
                            )
                        ),
                        dbc.Col(
                            html.P("Group by:"),
                            className="mt-1",
                            xs=3,
                            md=2,
                            lg={"offset": 3, "size": 2},
                            xl={"offset": 4, "size": 2},
                        ),
                        dbc.Col(
                            dbc.Card(
                                dcc.RadioItems(
                                    id="g1-group-radio",
                                    className="mt-1",
                                    options=self._g1_group_options,
                                    value="Season",
                                    labelStyle={"display": "block"},
                                )
                            ),
                        ),
                    ],
                ),
                dbc.Row(
                    className="mt-4",
                    children=[
                        dbc.Col(html.P("Choose y-axis:"), className="mt-1", lg=2),
                        dbc.Col(
                            dbc.Card(
                                dcc.RadioItems(
                                    id="g1-y-radio",
                                    className="mt-1",
                                    options=self._g1_y_options,
                                    value="ID",
                                    labelStyle={"display": "block"},
                                )
                            ),
                            lg=3,
                        ),
                        dbc.Col(
                            html.P("Filter season:"),
                            className="mt-1",
                            lg={"offset": 3, "size": 2},
                        ),
                        dbc.Col(
                            dbc.Card(
                                dcc.RadioItems(
                                    id="g1-season-radio",
                                    className="mt-1",
                                    options=self._g1_season_options,
                                    labelStyle={"display": "block"},
                                )
                            ),
                            lg=2,
                        ),
                    ],
                ),
                dbc.Row(
                    className="mt-4",
                    children=[
                        dbc.Col(
                            dcc.Graph(id="g1-china-history-graph"),
                        )
                    ],
                ),
                dbc.Row(className="mt-5"),
                dbc.Row(className="mt-5"),
                dbc.Card(
                    dbc.CardBody(html.H2("China: Distributions and sex differences")),
                    className="mt-3",
                ),
                dbc.Row(
                    className="mt-4",
                    children=[
                        dbc.Col(html.P("Distribution:"), className="mt-1", lg=2),
                        dbc.Col(
                            dbc.Card(
                                dbc.RadioItems(
                                    id="g2-dist-radio",
                                    className="mt-1",
                                    options=self._g2_dist_options,
                                    value="Age",
                                )
                            ),
                            lg=2,
                        ),
                        dbc.Col(
                            html.P("Plot type:"),
                            className="mt-1",
                            lg={"offset": 4, "size": 2},
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.RadioItems(
                                    id="g2-plot-radio",
                                    className="mt-1",
                                    options=self._g2_plot_options,
                                    value="hist",
                                )
                            ),
                            lg=2,
                        ),
                    ],
                ),
                dbc.Row(
                    className="mt-4",
                    children=[
                        dbc.Col(
                            dcc.Graph(id="g2-china-dist-graph"),
                        )
                    ],
                ),
                dbc.Row(
                    className="mt-4",
                    children=[
                        dbc.Col(
                            dcc.Slider(
                                id="g2-sports-slider",
                                min=1,
                                max=10,
                                # marks=,
                                value=6,
                                step=1,
                            ),
                        )
                    ],
                ),

                dbc.Row(className="mt-5"),
                dbc.Row(className="mt-5"),
                dbc.Card(
                    dbc.CardBody(html.H2("China: Top sports")),
                    className="mt-3",
                ),
                dbc.Row(
                    className="mt-4",
                    children=[
                        dbc.Col(html.P("Plot:"), className="mt-1", lg=1),
                        dbc.Col(
                            dbc.Card(
                                dcc.RadioItems(
                                    id="g3-plot-radio",
                                    className="mt-1",
                                    options=self._g3_plot_options,
                                    value="bar",
                                    labelStyle={"display": "block"},
                                ),
                            ),
                            lg=3,
                        ),
                        dbc.Col(
                            html.P("Choose sport:"),
                            className="mt-1",
                            lg={"offset": 2, "size": 2},
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                id="g3-sports-dropdown",
                                className="mt-1",
                                options=self._g3_sports_options,
                                value="All",
                            ),
                            lg=4,
                        ),
                    ],
                ),
                dbc.Row(dcc.Graph(id="g3-china-sports-graph"), className="mt-4"),
                dbc.Row(className="mt-5"),
                dbc.Row(className="mt-5"),                    
                dbc.Card(
                    dbc.CardBody(html.H2("All countries: Top performers")),
                    className="mt-3",
                ),               
                dbc.Row(dcc.Graph(id="top10-country-medals"), className="mt-4"),
                dbc.Row(
                    dcc.RadioItems(
                        id="num_dropdown",
                        options=self._num_options, value=10)
                    ),
                dbc.Row(className="mt-5"),
                dbc.Row(className="mt-5"),                    
                dbc.Card(
                    dbc.CardBody(html.H2("All countries: Age/Weight/Height distributions")),
                    className="mt-3",
                ),
                dbc.Row(
                    dcc.RadioItems(
                        id = "dist-radio",
                        options = self._dist_options,
                        value = "Age"
                    )),
                dbc.Row(dcc.Graph(id="age-distribution-athletes"), className="mt-4"),    
                dbc.Row(className="mt-5"),
                dbc.Row(className="mt-5"),                    
                dbc.Card(
                    dbc.CardBody(html.H2("All countries: Sex distribution")),
                    className="mt-3",
                ),
                dbc.Row(
                    dcc.RadioItems(
                        id = "dist2-radio",
                        options = self._dist2_options,
                        value = "Sex"
                    )),
                dbc.Row(dcc.Graph(id="sex-distribution"), className="mt-4"),    
                dbc.Row(className="mt-5"),
                dbc.Row(className="mt-5"),                    
                dbc.Card(
                    dbc.CardBody(html.H2("Sports: Medal count")),
                    className="mt-3",
                ),
                dbc.Row(
                    dcc.RadioItems(
                        id = "a1-sport-radio",
                        options = self._a1_sport_options,
                        value = "Football"
                    )),
                dbc.Row(
                    dcc.RadioItems(
                        id = "a1-plot-radio",
                        options = self._a1_plot_options,
                        value = "All"
                    )),                    
                dbc.Row(dcc.Graph(id="a1-sport-medals-graph"), className="mt-4"),
                dbc.Row(className="mt-5"),
                dbc.Row(className="mt-5"),
                dbc.Card(
                    dbc.CardBody(html.H2("Sports: Age distribution")),
                    className="mt-3",
                ),                               
                dbc.Row(
                    dcc.RadioItems(
                        id = "a2-sport-radio",
                        options = self._a2_sport_options,
                        value = "Football"
                    )),
                # dbc.Row(
                #     dcc.RadioItems(
                #         id = "a1-plot-radio",
                #         options = self._a1_plot_options,
                #         value = "All"
                #     )),                    
                dbc.Row(dcc.Graph(id="a2-dist-graph"), className="mt-4"),
            ]
        )

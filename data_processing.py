import pandas as pd
import plotly_express as px
from functools import reduce

def olymics_plot_df(df: pd.DataFrame, x: str, y: str, grouping: str = None, reverse_sort: bool = False, plot: str = None):
    """
    Quick processing of OS data for plotting x on y, with optional grouping.
    Returns plotly express plot when specified (plot="line", plot="bar" and plot="scatter" supported).
    Otherwise returns the processed pd.DataFrame for manual creation of plots.
    """

    if not grouping:
        # if y is continuous, take mean instead of count
        if df[y].dtype == 'float64':
            df = df.groupby(x)[y].mean().reset_index()
        else:
            df = df.groupby(x)[y].count().reset_index()

        groups = y

    else:
        groups = list(df[grouping].unique())
        df_list = []

        for i in groups:
            df_cat = df[df[grouping] == i]

            # if y is linear, take mean instead of count
            if df[y].dtype == 'float64':
                df_cat = df_cat.groupby(x)[y].mean().reset_index().rename({y: i}, axis=1)
                df_list.append(df_cat)
            else:
                df_cat = df_cat.groupby(x)[y].count().reset_index().rename({y: i}, axis=1)
                df_list.append(df_cat)
                
        # merging a list of dfs
        # source https://statisticsglobe.com/merge-list-pandas-dataframes-python
        df = reduce(lambda left, right:
                            pd.merge(left , right,
                                    on = [x],
                                    how = "outer"),
                            df_list)         

    if reverse_sort:                  
        df = df.sort_values(by = y)
    else:
        df = df.sort_values(by = x)

    if plot == "scatter":
        fig = px.scatter(
            df,
            x = x,
            y = groups,
            labels = {"variable": grouping, "value": y})
        return fig
    elif plot == "bar":
        fig = px.bar(
            df,
            barmode = "group",
            x = x,
            y = groups,
            labels = {"variable": grouping, "value": y})            
        return fig
    elif plot == "line":
        fig = px.line(
            df,
            x = x,
            y = groups,
            labels = {"variable": grouping, "value": y})
        return fig
    else:
        return df
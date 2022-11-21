import os
import pandas as pd
import plotly_express as px
from functools import reduce
import hashlib as hl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def get_data_path():
    directory_path = os.path.dirname(__file__)
    path = os.path.join(directory_path, "Data")
    return path


def load_data(folder_path: str) -> pd.DataFrame:
    files = []

    for file in ["athlete_events.csv", "noc_regions.csv"]:
        file_path = os.path.join(folder_path, file)
        files.append(pd.read_csv(file_path))

    # merge to also get country names
    # keep all rows from athlete_events.csv, even if NOC is not in noc_regions.csv
    df = pd.merge(files[0], files[1], on = "NOC", how = "left")

    # there are duplicates for some reason, dropping them
    df.drop_duplicates(inplace = True)

    # anonymize names
    df["Name"] = df["Name"].apply(lambda x: hl.sha3_256(x.encode()).hexdigest())

    return df


def load_data2(folder_path: str) -> pd.DataFrame:
    # File pathes
    regions = pd.read_csv("Data/noc_regions.csv")
    athlete_events = pd.read_csv("Data/athlete_events.csv")

    # Concatinating 
    df2 = pd.concat([df2,regions], keys="NOC")
    # Merging
    df2 = pd.merge(df2, regions, how="left", on="NOC")

    # anonymize names
    df2["Name"] = df2["Name"].apply(lambda x: hl.sha3_256(x.encode()).hexdigest())

    return df2


class DataProcessing:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def noc_filter(self, noc: str or list):
        if noc == "CHN":
            self.df = self.df[self.df["NOC"] == noc]
        return self

    def sort_plot(self, sort: str or list):
        if "sport" in sort:
            sorted = list(self.df.groupby("Sport")["Medal"].count().sort_values(ascending=False).index)
            sort_column = "Sport"
         
        elif "countr" in sort:
            sorted = list(self.df.groupby("NOC")["Medal"].count().sort_values(ascending=False).index)
            sort_column = "NOC"

        if "top10" in sort:
            # top10_list = list(self.df.groupby("Sport")["Medal"].count().sort_values(ascending=False).head(10).index)
            sorted = sorted[:10]
            self.df = self.df[self.df[sort_column].isin(sorted)]

        # source for sort
        # https://stackoverflow.com/questions/52784410/sort-column-in-pandas-dataframe-by-specific-order            
        self.df[sort_column] = pd.Categorical(self.df[sort_column], categories=sorted)
        self.df.sort_values(sort_column)        

        return self

    def top_10_countries_medals(df2):
        """Making a new DF that is cleaned.
        Gives out visualization """
        df1 = df2.groupby("region")["Medal"].count().nlargest(10).nlargest(10).reset_index()
        plt.figure(figsize=(12,6))
        plt.title("10 countries with the most medals")
        plt.xlabel("Regions")
        plt.ylabel("Medals")
        plt.xticks(rotation=90)
        fig = sns.barplot(x=df1["region"], y=df1["Medal"], palette='pastel')
        return fig

    #fig = top_10_countries_medals(athlete_events)


    def age_distribution_athletes(df2):
        """Plotting age distribution with a histogram, aswell as sorting df"""
        plt.figure(figsize=(12, 6))
        plt.title("Age distribution of the athletes")
        plt.xlabel("Age")
        plt.ylabel("Number of Participants")
        # https://numpy.org/doc/stable/reference/generated/numpy.arange.html
        # https://stackoverflow.com/questions/33458566/how-to-choose-bins-in-matplotlib-histogram
        fig = plt.hist(
            df2.Age, bins=np.arange(10, 80, 2), color="blue", edgecolor="white"
        )
        return fig


    def sex_distribution_athletes(df2):
        """Cleaning df and visualization as pie chart"""
        gender_count = df2.Sex.value_counts()
        myexplode = (0.02, 0.02) # Splitting the pie chart
        plt.pie(gender_count, labels =["M","F"], autopct="%.2f", explode= myexplode)
        plt.title("Sex distribution among the athletes")
        return

    #sex_distribution_athletes(df)


    def olymics_plot_df(self, x: str, y: str, grouping: str = None, reverse_sort: bool = False, plot: str = None):
        """
        Quick processing of OS data for plotting x on y, with optional grouping.
        Returns plotly express plot when specified (plot="line", plot="bar" and plot="scatter" supported).
        Otherwise returns the processed pd.DataFrame for manual creation of plots.
        """
        df = self.df

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
            self.df = df
            return self


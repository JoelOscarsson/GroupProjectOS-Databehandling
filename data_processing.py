import os
import pandas as pd
import plotly_express as px
from functools import reduce
import hashlib as hl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def get_data_path():
    """Gets path for Data folder in pwd, enabling usage of load_data() in .ipynb files"""
    directory_path = os.path.dirname(__file__)
    path = os.path.join(directory_path, "Data")
    return path


def load_data(folder_path: str) -> pd.DataFrame:
    """
    Merges data from athletes_events and noc_regions into a DataFrame.
    Drops duplicates and anonymizes names.
    """
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




class DataProcessing:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def filter_noc(self, noc: str or list):
        df = self.df

        if isinstance(noc, list):
            df = df[df["NOC"].isin(noc)]
        elif not noc == "all":
            df = df[df["NOC"] == noc]

        return DataProcessing(df)

    def filter_season(self, season: str):
        df = self.df
        df = df[df["Season"] == season]

        return DataProcessing(df)

    def filter_top(self, filter_col: str, filter_on_col: str, num: int):
        df = self.df

        filter_ = list(df.groupby(filter_col)[filter_on_col].count().sort_values(ascending=False).head(num).index)
        df = df[df[filter_col].isin(filter_)]

        return DataProcessing(df)
        
    def top_10_countries_medals(self, num):
        """Making a new DF that is cleaned.
        Gives out visualization """
        df1 = self.df.groupby("region")["Medal"].count().nlargest(num).reset_index()
        fig = px.bar(df1, x = "region", y = "Medal", color = "region")
        # plt.figure(figsize=(12,6))
        # plt.title("10 countries with the most medals")
        # plt.xlabel("Regions")
        # plt.ylabel("Medals")
        # plt.xticks(rotation=90)
        # fig = sns.barplot(x=df1["region"], y=df1["Medal"], palette='pastel')
        return fig

    #fig = top_10_countries_medals(athlete_events)


    def age_distribution_athletes(self, dist):
        """Plotting age distribution with a histogram, aswell as sorting df"""
        # plt.figure(figsize=(12, 6))
        # plt.title("Age distribution of the athletes")
        # plt.xlabel("Age")
        # plt.ylabel("Number of Participants")
        # https://numpy.org/doc/stable/reference/generated/numpy.arange.html
        # https://stackoverflow.com/questions/33458566/how-to-choose-bins-in-matplotlib-histogram
        # fig = plt.hist(
            # self.df.Age, bins=np.arange(10, 80, 2), color="blue", edgecolor="white"
        # )
        fig = px.histogram(self.df, dist)
        fig.update_layout(hovermode = "x")
        return fig


    def sex_distribution_athletes(self, dist):
        """Cleaning df and visualization as pie chart"""
        gender_count = self.df[dist].value_counts().head(10).reset_index()

        if dist == "Sport":
            other_index = len(self.df) - gender_count["Sport"].sum()
            other_index_df = pd.DataFrame({"index": ["Other"], "Sport": [other_index]})
            gender_count = pd.concat([gender_count, other_index_df]).reset_index()

        fig = px.pie(gender_count, values = dist, names = "index")
        fig.update_traces(pull=[0.02, 0.02, 0.02, 0.02, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04])

        # myexplode = (0.02, 0.02) # Splitting the pie chart
        # fig = plt.pie(gender_count, labels =["M","F"], autopct="%.2f", explode= myexplode)
        # fig.update_traces(pull=[0.1, 0, 0, 0])

        # plt.title("Sex distribution among the athletes")
        return fig

    
    def proportion_plot(self, x: str, y: str, per: str, grouping: str = None): 
        df_count = self.basic_plot(x, y, grouping).df
        df_total = self.basic_plot(x, per, grouping).df

        
        df_list = []
        for i in self.df[grouping].unique():
            # checks proportion of y in each category of grouping
            df = pd.merge(df_count[[x, i]], df_total[[x, i]], on = x, suffixes = ["_count", "_total"])
            df[i] = df[i + "_count"] / df[i + "_total"]
            df = df.iloc[:,[0,-1]] # keep only x and proportion
            df_list.append(df)

        # merging a list of dfs
        # source https://statisticsglobe.com/merge-list-pandas-dataframes-python
        df = reduce(lambda left, right:
                        pd.merge(left , right,
                                on = [x],
                                how = "outer"),
                        df_list)         

        # fig = px.bar(df, x = x, y = list(df.columns[1:]), barmode = "group")
        return DataProcessing(df)


    def basic_plot(self, x: str, y: str, grouping: str = None, reverse_sort: bool = False, plot: str = None, title: str = None):
        """
        Quick processing of OS data for plotting x on y, with optional grouping.
        Returns plotly express plot when specified (plot="histo", plot="line", plot="bar" and plot="scatter" supported).
        Otherwise returns the processed pd.DataFrame for manual creation of plots or further processing.
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
                labels = {"variable": grouping, "value": y},
                title = title)
            return fig
        elif plot == "bar":
            fig = px.bar(
                df,
                barmode = "group",
                x = x,
                y = groups,
                labels = {"variable": grouping, "value": y},
                title = title)            
            return fig
        elif plot == "histo":
            fig = px.histogram(
                df,
                barmode = "group",
                nbins = 50,
                histnorm = 'probability density',
                x = x,
                y = groups,
                labels = {"variable": grouping, "value": y},
                title = title) 
            return fig            
        elif plot == "line":
            fig = px.line(
                df,
                x = x,
                y = groups,
                markers=True,
                labels = {"variable": grouping, "value": y},
                title = title)
            return fig
        else:
            return DataProcessing(df)


## deprecated method for exploratory plot    
    # def basic_plot_sort(self, sort: str or list):
    #     """Sorting sports and countries by medal in the basic plot."""
    #     df = self.df

    #     if "sport" in sort:
    #         sorted = list(df.groupby("Sport")["Medal"].count().sort_values(ascending=False).index)
    #         sort_column = "Sport"
         
    #     elif "countr" in sort:
    #         sorted = list(df.groupby("NOC")["Medal"].count().sort_values(ascending=False).index)
    #         sort_column = "NOC"

    #     if "top10" in sort:
    #         # top10_list = list(self.df.groupby("Sport")["Medal"].count().sort_values(ascending=False).head(10).index)
    #         sorted = sorted[:10]
    #         df = df[df[sort_column].isin(sorted)]

    #     # source for sort
    #     # https://stackoverflow.com/questions/52784410/sort-column-in-pandas-dataframe-by-specific-order            
    #     df[sort_column] = pd.Categorical(df[sort_column], categories=sorted)
    #     df.sort_values(sort_column)        

    #     return DataProcessing(df)

    def sports_medal_plot(self, sport, plot):
        df = self.df
        sports_Df = df[df["Sport"] == sport]

        # Concating the dummies of Medal 

        sports_Df = pd.concat([sports_Df, pd.get_dummies(sports_Df['Medal'])], axis=1)

        #removing the duplicates in the football dataset
        num_medals = sports_Df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])

        # sorting by the country and sex with the most gold and creating a column for the total medals
        num_medals = num_medals.groupby(["region", "Sex"]).sum(numeric_only=True)[["Gold", "Silver", "Bronze"]].sort_values("Gold",ascending=False).reset_index()
        num_medals['Total'] = num_medals['Gold']+ num_medals['Silver']+ num_medals['Bronze']

        ## visualizing the medal distribution
        top_country = num_medals.sort_values("Total", ascending=False).reset_index()

        if plot == "All":

            fig = px.bar(data_frame = top_country.head(20), x="region"  ,
                
                y="Total",
                labels={"region": "Country", "Total": "Total medals"},
                title= f"Top 20 Countries With the Most Medals in {sport} In The Olympics",
                color="region",
                #log_y= True,
                barmode= "relative"
                
                
            )
            fig.update_layout(
                    xaxis_title = "Countries")
        elif plot == "Sex":
            ## visualizing the gender distribution
            fig = px.bar(data_frame = top_country.head(20), x="region"  ,
            
                y="Total",
            labels={"region": "Country", "Total": "Total medals"},
            title=f"Gender With The Most Medals in {sport} in the Olympics",
            color="Sex",
            #log_y= True,
            barmode= "group"
            
            
            )
            fig.update_layout(
                    xaxis_title = "Countries")

        return fig
        # fig1.show()


    def sports_dist_plot(self, sport):
        df = self.df

        sports_Df = df[df["Sport"] == sport]
        age_football = sports_Df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
        age_football = sports_Df[sports_Df["Age"].notna()] # none zero values

        athlete_age =  pd.DataFrame(dict(Athletes_Ages = age_football["Sport"].groupby(age_football["Age"]).count())).reset_index()
        
        fig = px.bar(data_frame = athlete_age, x="Age"  ,
        
        y="Athletes_Ages",
        labels={"Age": "Age", "Athletes_Ages": "Number of athletes per this Age"},
        title=f"Age Distribution among Athletes of {sport} IN OLYMPICS",
        color="Age",
        #log_y= True,
        barmode= "relative"
        
        
        )
        fig.update_layout(
                xaxis_title = "Ages",
                yaxis_title = "Total Number Per Age",)
        return fig
    




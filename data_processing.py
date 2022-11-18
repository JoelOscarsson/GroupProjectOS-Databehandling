import os
import pandas as pd
import plotly_express as px
from functools import reduce


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

    # df = df["Name"].apply(lambda x: hl.sha3_256(x.encod()).hexdigest())

    return df


class DataProcessing:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def noc(self, noc: str or list):
        if isinstance(noc, list):
            self.df = self.df[self.df["NOC"].isin(noc)]
        else:
            self.df = self.df[self.df["NOC"] == noc]
        return self

    def sports(self, sports: str or list):
        if isinstance(sports, list):
            self.df = self.df[self.df["Sport"].isin(sports)]
        else:
            self.df = self.df[self.df["Sport"] == sports]
        return self

    def top_10_countries(self):
        df_ = self.df.copy()  # good to create a copy 
        df_ = df_[df_["Medal"].isna() == False]
        df_value_counts = df_.value_counts("NOC")
        df_top10 = df_value_counts.head(10)
        df_top10 
        fig = px.bar(df_top10.reset_index().head(10), x="NOC", y=0, title= "Top 10 Countries Medals")
        return fig



    def analysis_on_sports(self):
        sports = ["Football", "Basketball", "Gymnastics"]
        for sport in sports:
            sports_df = self.df[self.df.Sport == sport]
            # Concating the dummies of Medal
            sports_df = pd.concat([sports_df, pd.get_dummies(sports_df["Medal"])], axis=1)
            # removing the duplicates in the football dataset
            num_medals = sports_df.drop_duplicates(
                subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"]
            )
            # Sorting by the country and sex with the most gold and creating a column for the total medals
            num_medals = (
                num_medals.groupby(["region", "Sex"])
                .sum(numeric_only=True)[["Gold", "Silver", "Bronze"]]
                .sort_values("Gold", ascending=False)
                .reset_index()
            )
            num_medals["Total"] = (
                num_medals["Gold"] + num_medals["Silver"] + num_medals["Bronze"]
            )


            ## visualizing the medal distribution
            top_country = num_medals.sort_values("Total", ascending=False).reset_index()


            fig = px.bar(data_frame = top_country.head(20), x="region"  ,
                
                y="Total",
                labels={"region": "Country", "Total": "Total medals"},
                title= f"Top 20 Countries With the Most Medals in {sport} In The Olympics",
                color="region",
                #log_y= True,
                barmode= "relative")


            fig.update_layout(
            xaxis_title = "Countries")
            ## visualizing the gender distribution
            fig1 = px.bar(data_frame = top_country.head(20), x="region"  ,
            
            y="Total",
            labels={"region": "Country", "Total": "Total medals"},
            title=f"Gender With The Most Medals in {sport} in the Olympics",
            color="Sex",
            #log_y= True,
            barmode= "group"
            
            
            )
            fig1.update_layout(
                    xaxis_title = "Countries")
            return fig, fig1


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


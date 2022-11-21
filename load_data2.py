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

    
class DataProcessing:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def top_10_countries_medals(self):
        """Making a new DF that is cleaned.
        Gives out visualization """
        df1 = self.df.groupby("region")["Medal"].count().nlargest(10).nlargest(10).reset_index()
        plt.figure(figsize=(12,6))
        plt.title("10 countries with the most medals")
        plt.xlabel("Regions")
        plt.ylabel("Medals")
        plt.xticks(rotation=90)
        fig = sns.barplot(x=df1["region"], y=df1["Medal"], palette='pastel')
        return fig

    #fig = top_10_countries_medals(athlete_events)


    def age_distribution_athletes(self):
        """Plotting age distribution with a histogram, aswell as sorting df"""
        plt.figure(figsize=(12, 6))
        plt.title("Age distribution of the athletes")
        plt.xlabel("Age")
        plt.ylabel("Number of Participants")
        # https://numpy.org/doc/stable/reference/generated/numpy.arange.html
        # https://stackoverflow.com/questions/33458566/how-to-choose-bins-in-matplotlib-histogram
        fig = plt.hist(
            self.df.Age, bins=np.arange(10, 80, 2), color="blue", edgecolor="white"
        )
        return fig


    def sex_distribution_athletes(self):
        """Cleaning df and visualization as pie chart"""
        gender_count = self.df.Sex.value_counts()
        myexplode = (0.02, 0.02) # Splitting the pie chart
        fig = plt.pie(gender_count, labels =["M","F"], autopct="%.2f", explode= myexplode)
        plt.title("Sex distribution among the athletes")
        return fig

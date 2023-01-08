import random

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from utils import distance
from datasets import datasets

st.title("K-Means")

k = st.slider("K")


class KMeans:
    def calculate_distance_list_from_centroid_list(self, series: pd.Series) -> dict:
        return {centroid: distance.euclidean(centroid, series) for _, centroid in self.centroid_df.iterrows()}

    def create_random_centroid(self):
        self.centroid_df = self.items_df.sample(n=k).reset_index()
        self.centroid_df.index.names = ["centroid"]

    def update_centroid(self):


    def __init__(self, input_df: pd.DataFrame, k: int, init="random"):
        self.items_df = input_df

        self.centroid_df = None
        self.create_random_centroid()

        # if init == "random":
        #     self.random_centroid_assignment()
        # else:
        #     raise NotImplementedError
        #     attribute_name_min_and_max_value = dict()
        #     for attribute in df.columns:
        #         attribute_column = df[attribute]
        #         attribute_name_min_and_max_value[attribute] = (attribute_column.min(), attribute_column.max())

        self.items_df = input_df
        input_df["assignment"] = None
        for i, row in input_df.iterrows():
            distance_from_centroid = self.calculate_distance_list_from_centroid_list(row)
            input_df.iloc[i]["assignment"] = min(iterrows.items(), key=lambda name_distance: name_distance[1])

    def visualize(self):
        fig, ax = plt.subplots()
        sns.scatterplot(data=self.items_df, ax=ax)


k_means_test = KMeans(datasets.countries_and_gdp(), k=5)

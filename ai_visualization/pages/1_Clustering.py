import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from utils import distance
from datasets import datasets


def min_max_normalizer(column: pd.Series):
    return (column - column.min()) / (column.max() - column.min())


def normalize_across_column(df: pd.DataFrame):
    df = df.copy()
    for column in df.columns:
        df[column] = min_max_normalizer(df[column])
    return df


class KMeans:
    def set_centroid_to_random_data_point(self) -> None:
        print("set centroid to random")
        self.centroid_df = None
        self.centroid_df = self.data_point_normalized_df.sample(n=self.k).reset_index(drop=True)
        self.centroid_df.index.names = ["centroid"]

    def set_distance_from_data_point_to_centroid(self) -> None:
        print("set distance")
        for centroid_index in self.centroid_df.index:
            self.data_point_df[centroid_index] = None

        for data_point_index, data_point in self.data_point_df.copy().iterrows():
            for centroid_index, centroid in self.centroid_df.iterrows():
                distance_between = distance.euclidean(self.data_point_normalized_df.loc[data_point_index], centroid)
                self.data_point_df.at[data_point_index, centroid_index] = distance_between

    def assign_data_point_to_centroid(self) -> None:
        print("assign")
        assert isinstance(self.centroid_df, pd.DataFrame) and not self.centroid_df.empty

        self.data_point_df["assignment"] = None
        for i, row in self.data_point_df.copy().iterrows():
            distance_to_centroid = dict(row[self.centroid_df.index])
            centroid_with_min_distance_index = min(distance_to_centroid.items(), key=lambda x: x[1])[0]
            self.data_point_df.at[i, "assignment"] = centroid_with_min_distance_index

    def update_centroid(self):
        print("update")
        for centroid_index, centroid in self.centroid_df.copy().iterrows():
            assigned_to_centroid = self.data_point_df["assignment"] == centroid_index
            for attribute in centroid.index:
                mean = self.data_point_normalized_df[assigned_to_centroid][attribute].mean()
                print("mean", mean)
                self.centroid_df.at[centroid_index, attribute] = mean
        self.assign_data_point_to_centroid()

    def __init__(self, data_point_df: pd.DataFrame, k: int, init="random"):
        self.data_point_df = data_point_df
        self.k = k

        self.data_point_normalized_df = normalize_across_column(data_point_df)

        self.centroid_df = None
        self.set_centroid_to_random_data_point()

        self.set_distance_from_data_point_to_centroid()

        self.assign_data_point_to_centroid()
        # print(self.data_point_df.head())

        # print(self.centroid_df)
        # if init == "random":
        #     self.random_centroid_assignment()
        # else:
        #     raise NotImplementedError
        #     attribute_name_min_and_max_value = dict()
        #     for attribute in df.columns:
        #         attribute_column = df[attribute]
        #         attribute_name_min_and_max_value[attribute] = (attribute_column.min(), attribute_column.max())

    def visualize(self) -> plt.Figure:
        fig, ax = plt.subplots()
        sns.scatterplot(data=self.data_point_df, x="gdp", y="life_expectancy_years", hue="assignment", ax=ax)
        plt.xscale("log")
        numbers_range = [1000 * 2 ** i for i in range(0, 8)]
        plt.xticks(numbers_range, numbers_range)
        return fig


TITLE = "K-Means"
st.set_page_config(layout="wide", page_title=TITLE)

st.title(TITLE)

configuration = st.container()

k = configuration.slider("K", min_value=1, max_value=10)
if "k_means" not in st.session_state or st.session_state.k != k:
    st.session_state.k_means = KMeans(datasets.countries_and_gdp(), k=k)
    st.session_state.k = k

if configuration.button("Update Centroid"):
    st.session_state.k_means.update_centroid()

data_view_col, visualization = st.columns(2)
visualization.pyplot(st.session_state.k_means.visualize())

data_view_container = data_view_col.container()

data_view_container.header("Data Points")
data_view_container.dataframe(st.session_state.k_means.data_point_df)

data_view_container.header("Centroid")
data_view_container.dataframe(st.session_state.k_means.centroid_df)

# create DataFrame
import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df = pd.DataFrame({'points': [18, np.nan, 19, 14, 14, 11, 20, 28, 30, 31,
                              35, 33, 29, 25, 25, 27, 29, 30, 19, 23],
                   'assists': [3, 3, 4, 5, 4, 7, 8, 7, 6, 9, 12, 14,
                               np.nan, 9, 4, 3, 4, 12, 15, 11],
                   'rebounds': [15, 14, 14, 10, 8, 14, 13, 9, 5, 4,
                                11, 6, 5, 5, 3, 8, 12, 7, 6, 5]})

# view first five rows of DataFrame
print(df.head())

# drop rows with NA values in any columns
df = df.dropna()

# create scaled DataFrame where each variable has mean of 0 and standard dev of 1


# view first five rows of scaled DataFrame
print(scaled_df[:5])


def k_means(data: pd.DataFrame, k: int) -> list:
    # Data preparation
    data = data.dropna()  # Get rid of every row containing an empy element
    scaled_df = StandardScaler().fit_transform(df)

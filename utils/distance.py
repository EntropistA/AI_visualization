import numpy as np
import pandas as pd


def euclidean(a: pd.Series, b: pd.Series):
    return np.sqrt(np.sum(np.power(a - b, 2)))

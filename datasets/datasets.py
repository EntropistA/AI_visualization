import os
from pathlib import Path
from contextlib import contextmanager

import pandas as pd

PROJECT_NAME = "AI_visualization"


@contextmanager
def project_root():
    previous_cwd = Path.cwd()
    project_root_index = previous_cwd.parts.index(PROJECT_NAME)
    new_directory = Path(*previous_cwd.parts[:project_root_index + 1])
    os.chdir(new_directory)
    yield
    os.chdir(previous_cwd)


def k_to_thousand(number: str) -> float:
    return float(number.rstrip("k")) * 1000 if number.endswith("k") else number



def countries_and_gdp(year=2019, normalize=True):
    columns = ["country", str(year)]

    income_file_location = Path("datasets", "income_per_person_gdppercapita_ppp_inflation_adjusted.csv")
    with project_root():
        income = pd.read_csv(income_file_location, usecols=columns)
    income.rename(columns={str(year): "gdp"}, inplace=True)
    income["gdp"] = income["gdp"].apply(k_to_thousand)

    life_expectancy_file_location = Path("datasets", "life_expectancy_years.csv")
    with project_root():
        life_expectancy = pd.read_csv(life_expectancy_file_location, usecols=columns)
        life_expectancy.rename(columns={"2019": "life_expectancy_years"}, inplace=True)

    income_life_expectancy = income.set_index("country").join(life_expectancy.set_index("country")).astype("float")
    return income_life_expectancy

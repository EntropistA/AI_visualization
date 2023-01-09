import os
from pathlib import Path
from contextlib import contextmanager

import pandas as pd

PROJECT_NAME = "ai_visualization"


def list_rindex(list_, target):
    for i in reversed(range(len(list_))):
        if list_[i] == target:
            return i
    raise ValueError(f"{target} not found")


@contextmanager
def project_root():
    previous_cwd = Path.cwd()
    project_root_index = list_rindex(previous_cwd.parts, PROJECT_NAME)
    new_directory = Path(*previous_cwd.parts[:project_root_index + 1])
    os.chdir(new_directory)
    try:
        yield
    finally:
        os.chdir(previous_cwd)


def k_to_thousand(number: str) -> float:
    return float(number.rstrip("k")) * 1000 if number.endswith("k") else number


def countries_and_gdp(year=2019, normalize=True):
    columns = ["country", str(year)]

    income_file_location = Path("datasets", "income_per_person_gdppercapita_ppp_inflation_adjusted.csv")
    with project_root():
        raise ValueError(Path.cwd(), income_file_location, income_file_location.exists())
        income = pd.read_csv(income_file_location, usecols=columns)
    income.rename(columns={str(year): "gdp"}, inplace=True)
    income["gdp"] = income["gdp"].apply(k_to_thousand)

    life_expectancy_file_location = Path("datasets", "life_expectancy_years.csv")
    with project_root():
        life_expectancy = pd.read_csv(life_expectancy_file_location, usecols=columns)
        life_expectancy.rename(columns={"2019": "life_expectancy_years"}, inplace=True)

    income_life_expectancy = income.set_index("country").join(life_expectancy.set_index("country")).astype("float")
    return income_life_expectancy

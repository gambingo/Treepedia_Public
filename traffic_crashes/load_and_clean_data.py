import pandas as pd

from directories import CRASH_DATA_DIR


def load_data():
    filepath = CRASH_DATA_DIR / "Traffic_Crashes_-_Crashes.csv"
    df = pd.read_csv(filepath)

    index_col = "CRASH_RECORD_ID"
    df.set_index(index_col, inplace=True)

    _format = "%m/%d/%Y %H:%M:%S %p"
    datetime_columns = ["CRASH_DATE"]
    for col in datetime_columns:
        df[col] = pd.to_datetime(df[col], format=_format)

    return df


def load_people_dataset():
    filepath = CRASH_DATA_DIR / "Traffic_Crashes_-_People.csv"
    df = pd.read_csv(filepath)

    index_col = "PERSON_ID"
    df.set_index(index_col, inplace=True)
    return df
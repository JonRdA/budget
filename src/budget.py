import pandas as pd

def load_track(fpath):
    """Load account transactions data in correct format & return dataframe.
    Format: [date, description, amount, category, subcategory] without header.

    Args:
        fpath (str): csv file path.

    Returns:
        pd.DataFrame: loaded transaction file.
    """
    dt_parser = lambda x : pd.to_datetime(x, format="%d/%m/%Y")
    col_names = ["date", "description", "amount", "cat", "sub"]
    col_types = {"description": "string", "cat": "category", "sub": "category"}

    df = pd.read_csv(fpath, header=None, names=col_names, dtype=col_types,
        parse_dates=[0], date_parser=dt_parser)

    nan_ind = df.isna().any(axis=1)
    if nan_ind.any():
        nan_rows = list(df[nan_ind].index)
        raise ValueError(f"File '{fpath}' has 'nan' values in rows {nan_rows}.")
    return df


a1 = load_track("../input/track_account_01.csv")
a2 = load_track("../input/track_account_02.csv")

print(a1.head())
print(a1.dtypes)


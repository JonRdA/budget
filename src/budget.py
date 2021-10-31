import pandas as pd
import matplotlib.pyplot as plt

# DATA LOADING

def load_track(fpath, n_account):
    """Load account transactions data in correct format & return dataframe.
    Format: [date, description, amount, category, subcategory] without header.

    Args:
        fpath (str): csv file path.
        n_account (int): number of account to ad as column.

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
        raise ValueError(f"File '{fpath}' has 'nan' in rows {nan_rows}.")

    # Add account number as category.
    df["account"] = n_account
    df["account"] = df["account"].astype("category")

    return df


a1 = load_track("../input/track_account_01.csv", 1)
print(a1.head())
print(a1.dtypes)

import re
import json
import logging
import pandas as pd

CAT_COLS = ["y", "m", "cat", "sub", "account"]      # Category dtype

logger = logging.getLogger(__name__)

def expand_date(df):
    """Mutate dataframe by inserting ["year", "month"] columns from date.

    Args:
        df (pd.DataFrame): table containing datetime column called "date".
    """
    df["y"] = df["date"].dt.year
    df["m"] = df["date"].dt.month

def find_duplicates(df_0, df_1):
    """Find duplicate transactions on df_1 that already exist on df_0.

    Performs a smart check only using the overlapping dates of database,
    returns a boolean index array of the dataframe 'df_1'.

    Args:
        df_0 (pd.DataFrame): main database, multiple account transactions.
        df_1 (pd.DataFrame): account database, only one account transctions.

    Returns:
        pd.Series: boolean index series indicating duplicates on 'df_1'.
    """
    try:
        # Select same account & only overlaping time.
        df_0 = df_0[df_0["account"] == df_1.loc[1, "account"]]
        dt_0, dt_1 = df_0.iloc[-1, 0], df_1.iloc[1, 0]
    except KeyError:
        # Account is empty, no duplicates.
        return pd.Series()
    finally:
        if df_0.empty:
            # Database had no transactions of account number.
            return pd.Series()

    if dt_1 <= dt_0:
        filt_0 = df_0["date"].between(dt_1, dt_0)
        df_0 = df_0[filt_0]

        df_joined = pd.concat([df_0, df_1])
        dup_index = df_joined.duplicated(keep=False)
        
        return dup_index[len(df_0):]

    return pd.Series()

def cast_category(df):
    """Mutates dataframe so 'CAT_COLUMNS' are casted as categorical.
    
    Args:
        df (pd.DataFrame): transaction database.
    """
    df[CAT_COLS] = df[CAT_COLS].astype("category")

def assign_tags(row, d):
    """Modify row cat & sub using description if found in dict d mapping.

    Args:
        row (pd.Series): Account or Database row.
        d (dict): dictionary mapping keywords to tags (pair of [cat, sub].

    Returns:
        nr (pd.Series): new row modified with cat & sub set, same row otherwise.
    """
    for k, (c, s) in d.items():
        if re.search(k, row["description"], re.IGNORECASE):
            return pd.Series([c, s], index=["cat", "sub"])
    return pd.Series(index=["cat", "sub"])

def load_json(fpath):
    """Load json dictionary from file path location

    Args:
        fpath (str): file path.

    Returns:
        d (dict): loaded dictionary.
    """
    with open(fpath, "r") as f:
        d = json.load(f)
    return d

if __name__ == "__main__":
    # If module directly run, load log configuration for all modules.
    import logging.config
    logging.config.fileConfig('../log/logging.conf')
    logger = logging.getLogger('utils')

    import budget
    budget.main()

import re
import json
import logging
import datetime
import pandas as pd

logger = logging.getLogger(__name__)

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
            return pd.Series(dtype="float64")

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
    df[["tag", "account"]] = df[["tag", "account"]].astype("category")

def assign_tags(row, d):
    """Modify row tag using description if found in dict d mapping.

    Args:
        row (pd.Series): Account or Database row.
        d (dict): dictionary mapping keywords to tags (pair of [cat, sub].

    Returns:
        nr (pd.Series): new row modified with cat & sub set, same row otherwise.
    """
    for k, v in d.items():
        if re.search(k, row["description"], re.IGNORECASE):
            return pd.Series([v], index=["tag"])
    return pd.Series(index=["tag"])

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

def fit_dates(dt_index, t0, t1):
    """Fit dates to specified `dt_index` for proper selecting between dates.

    If `t0` or `t1` are None or out ouf bound of the `dt_index`, the 
    max and min values of the index are returned, otherwise are untouched.

    Args:
        dt_index (DatetimeIndex): panda object's index.
        t0 (datetime/str): initial date (str format: "yyyy-mm-dd").
        t1 (datetime/str): final date. 

    Returns:
        t0, t1 (tuple): adjusted dates.
    """
    if t0 == None:
        t0 = dt_index.index[0]
    if t1 == None:
        t1 = dt_index.index[-1]
    return t0, t1

def correct_account(db, account, func):
    """Modify amount `db` values of `account` number based on 'func'.

    Args:
        db (pd.DataFrame): Database object's db attribute.
        account (int): number of account to modify.
        func (function): modification to perform.

    Returns:
        mdb (pd.DataFrame): modified database.
    """
    mdb = db.copy()
    filt = mdb["account"] == account
    mdb.loc[filt, "amount"]= mdb["amount"][filt].apply(func)
    logger.warning(f"Account {account} values modified.")
    return mdb
    
if __name__ == "__main__":
    # If module directly run, load log configuration for all modules.
    import logging.config
    logging.config.fileConfig('../log/logging.conf')
    logger = logging.getLogger('utils')

    import budget
    budget.main()

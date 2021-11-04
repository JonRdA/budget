import pandas as pd


CAT_COLS = ["y", "m", "cat", "sub", "account"]      # Category dtype


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
    if df_0.empty:
        return pd.Series()

    # Database with same account & only check date overlap for duplicates.
    df_0 = df_0[df_0["account"] == df_1.loc[1, "account"]]
    dt_0, dt_1 = df_0.iloc[-1, 0], df_1.iloc[1, 0]

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


#sup_dict = { "essential": ["food", "house"],
#    "spending": ["leisure", "tech", "vacation", "finance", "education", "personal", "transport"],
#    "saving": ["saving"],
#    "transfer": ["transfer"]}
#
#def add_sup(df, sup_dict):
#    """Add super-categories column to dataframe as specified on sup_dict dict.
#
#    Args:
#        df (pd.DataFrame): transactions data.
#        sup_dict (dict): super-categories definition.
#
#    Returns:
#        pd.DataFrame: original data with added column.
#    """
#    cat = df["cat"]
#    """Invert dictionary and use it to map cat to supercat"""
#    sups = invert_dict(sup_dict)
#    print(sups)
#    sup = cat.apply(assign_sup, args=(sups,))
#
#    df["sup"] = sup
#    return sup
#
#def assign_sup(category, sup_dict):
#
#    print(category, sup_dict[category])
#    return sup_dict[category]
#
## HELPER FUNCTIONS
#
#def invert_dict(d):
#    """Invert dictionary converting values to keys. Values can be lists.
#
#    Args:
#        d (dict): dictionary to invert.
#
#    Returns:
#        dictionary
#    """
#    nd = {}
#    for k, vs in d.items():
#        for v in vs:
#            nd[v] = k
#    
#    return nd
#
#
#
#
if __name__ == "__main__":

    import budget
    budget.main()


#sup_dict = { "essential": ["food", "house"],
#    "spending": ["leisure", "tech", "vacation", "finance", "education", "personal", "transport"],
#    "saving": ["saving"],
#    "transfer": ["transfer"]}
#
#def add_sup(df, sup_dict):
#    """Add super-categories column to dataframe as specified on sup_dict dict.
#
#    Args:
#        df (pd.DataFrame): transactions data.
#        sup_dict (dict): super-categories definition.
#
#    Returns:
#        pd.DataFrame: original data with added column.
#    """
#    cat = df["cat"]
#    """Invert dictionary and use it to map cat to supercat"""
#    sups = invert_dict(sup_dict)
#    print(sups)
#    sup = cat.apply(assign_sup, args=(sups,))
#
#    df["sup"] = sup
#    return sup
#
#def assign_sup(category, sup_dict):
#
#    print(category, sup_dict[category])
#    return sup_dict[category]
#
## HELPER FUNCTIONS
#
#def invert_dict(d):
#    """Invert dictionary converting values to keys. Values can be lists.
#
#    Args:
#        d (dict): dictionary to invert.
#
#    Returns:
#        dictionary
#    """
#    nd = {}
#    for k, vs in d.items():
#        for v in vs:
#            nd[v] = k
#    
#    return nd
#
#
#
#
if __name__ == "__main__":

    import budget
    budget.main()

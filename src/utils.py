def expand_date(df):
    """Mutate dataframe by inserting ["year", "month"] columns from date.

    Args:
        df (pd.DataFrame): table containing datetime column called "date".
    """
    df["y"] = df["date"].dt.year.astype("category")
    df["m"] = df["date"].dt.month.astype("category")





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

import pandas as pd

class Account(pd.DataFrame):
    """Partial transaction database with one account information.

    Inherited from pandas dataframe contains all transactions sorted by date
    as well as their amount, category, subcategory and account.

    """
    
    def __init__(self, *args, **kwargs):
        """Pandas dataframe initialization with default parameters."""
        super().__init__(*args, **kwargs)

    @classmethod    
    def load(cls, fpath, n_account):
        """Constructor to create instance by loading transactions data.

        Format: [date, description, amount, category, subcat] without header.

        Args:
            fpath (str): csv file path.
            n_account (int): number of account to ad as column.

        Returns:
            Account: instance containing loaded transaction file.
        """
        dt_parser = lambda x : pd.to_datetime(x, format="%d/%m/%Y")
        cname = ["date", "description", "amount", "cat", "sub"]
        ctype = {"description": "string", "cat": "category", "sub": "category"}

        df = pd.read_csv(fpath, header=None, names=cname, dtype=ctype,
            parse_dates=[0], date_parser=dt_parser)

        nan_ind = df.isna().any(axis=1)
        if nan_ind.any():
            nan_rows = list(df[nan_ind].index)
            raise ValueError(f"File '{fpath}' has 'nan' in rows {nan_rows}.")

        # Add account number as category.
        df["account"] = n_account
        df["account"] = df["account"].astype("category")

        return df.sort_values(by=["date", "amount"], ignore_index=True)
        


if __name__ == "__main__":
    import budget
    budget.main()

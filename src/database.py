import pandas as pd

class Database():
    """Complete transaction database with multiple account information.

    Inherited from pandas dataframe contains all transactions sorted by date
    as well as their amount, category, subcategory and account.

    """
    
    def __init__(self, *args, **kwargs):
        """Pandas dataframe initialization with default parameters."""
        self.db = pd.DataFrame(*args, **kwargs)

    def __repr__(self):
        """Print readable representation of Database instance."""
        return str(self.db)
        
    @classmethod    
    def load(cls, fpath):
        """Create database by loading .csv file.

        Args:
            fpath (str): file path.

        Returns:
            Database: instance containing loaded transaction history.
        """
        dt_parser = lambda x : pd.to_datetime(x, format="%Y-%m-%d")
        col_types = {"description": "string", "cat": "category",
                     "sub": "category", "account": int}

        df = pd.read_csv(fpath, header=0, dtype=col_types,
            parse_dates=[0], date_parser=dt_parser)

        # Needs to specify first as int, then as category.
        df["account"] = df["account"].astype("category")

        return cls(df)

    def save(self, fpath):
        """Save database as .csv file.

        Args:
            fpath (str): file path.
        """
        self.db.to_csv(fpath, header=True, index=False, float_format="%.2f")

    def add_account(self, account):
        """Add account transactions to database.

        Args:
            account (Account): new account with transactions to be added.

        TODO"""
        df = pd.concat([self.db, account], ignore_index=True)

        if self.db.iloc[-1, 0] >= account.iloc[0, 0]:
            # TODO raise warning of duplicate days entered. print number rows in account, also move to function in utils to do this.{;:
            print("hey carful duplicate days are being entered.")
            df.drop_duplicates(inplace=True)
            df.sort_values(["date", "amount"], ignore_index=True, inplace=True)

        self.db = df

if __name__ == "__main__":
    import budget
    budget.main()

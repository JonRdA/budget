import pandas as pd

class Database(pd.DataFrame):
    """Complete transaction database with multiple account information.

    Inherited from pandas dataframe contains all transactions sorted by date
    as well as their amount, category, subcategory and account.

    """
    
    def __init__(self, *args, **kwargs):
        """Pandas dataframe initialization with default parameters."""
        super().__init__(*args, **kwargs)

        
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
        self.to_csv(fpath, header=True, index=False, float_format="%.2f")

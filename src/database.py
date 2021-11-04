import logging
import pandas as pd

import utils

logger = logging.getLogger(__name__)

# Solve the constans issue, maybe put them in package init, learn about it.
VIEW_COLS = ["date", "description", "amount"]       # Represent transactaction

class Database():
    """Complete transaction database with multiple account information.

    Inherited from pandas dataframe contains all transactions sorted by date
    as well as their amount, category, subcategory and account.

    """
    
    def __init__(self, *args, **kwargs):
        """Pandas dataframe initialization with default parameters."""
        self.db = pd.DataFrame(*args, **kwargs)
        logger.info(f"Database {self.db.shape} created.")

        if not self.db.empty:
            utils.expand_date(self.db)
            utils.cast_category(self.db)

    def __repr__(self):
        """Print readable representation of Database instance."""
        return str(self.db)

    def __str__(self):
        """Print easily readable representation, 'VIEW_COLS' only showed."""
        return str(self.db[VIEW_COLS])

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

        logger.info(f"Database {df.shape} loaded.")
        return cls(df)

    def save(self, fpath):
        """Save database as .csv file.

        Args:
            fpath (str): file path.
        """
        cols = ["date", "description", "amount", "cat", "sub"]
        self.db.to_csv(fpath, header=True, index=False, float_format="%.2f",
            columns=cols)

    def add_account(self, account):
        """Adds account transactions to database, updates 'db' attribute.

        Raises warning if transactions found in database are added to it.

        Args:
            account (Account): new account with transactions to be added.
        """
        utils.expand_date(account)
        df_0, df_1 = self.db, account

        # Duplicates index is returned, just warns but they can be deleted.
        dup_index = utils.find_duplicates(df_0, df_1)
        if dup_index.any():
            logger.warning(f"Adding duplicate transactions:\n{df_1[dup_index]}")

        logger.info(f"Account {df_1.shape} added to Database {df_0.shape}.")
        df = df_0.append(df_1, ignore_index=True, sort=["date", "amount"])
        utils.cast_category(df)
        self.db = df

if __name__ == "__main__":
    # If module directly run, load log configuration for all modules.
    import logging.config
    logging.config.fileConfig('../log/logging.conf')
    logger = logging.getLogger('database')

    import budget
    budget.main()

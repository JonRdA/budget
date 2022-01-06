import logging
import pandas as pd

import utils

logger = logging.getLogger(__name__)

class Database():
    """Complete transaction database with multiple account information.

    Inherited from pandas dataframe contains all transactions sorted by date
    as well as their amount, category, subcategory and account.

    """
    
    def __init__(self, *args, **kwargs):
        """Pandas dataframe initialization with default parameters."""
        self.db = pd.DataFrame(*args, **kwargs)
        logger.debug(f"Database {self.db.shape} created.")

        if not self.db.empty:
            utils.cast_category(self.db)

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
        col_types = {"description": "string", "tag": "category", "account": int}

        df = pd.read_csv(fpath, header=0, dtype=col_types,
            parse_dates=[0], date_parser=dt_parser)
        df.dropna(how="all", inplace=True)

        logger.debug(f"Database {df.shape} loaded.")
        return cls(df)

    def save(self, fpath):
        """Save database as .csv file.

        Args:
            fpath (str): file path.
        """
        cols = ["date", "description", "amount", "account", "tag"]
        self.db.to_csv(fpath, header=True, index=False, float_format="%.2f",
            columns=cols)

        logger.info(f"Database {self.db.shape} saved on file '{fpath}'.")

    def add_account(self, account):
        """Adds account transactions to database, updates 'db' attribute.

        Raises warning if transactions found in database are added to it.

        Args:
            account (Account): new account with transactions to be added.
        """
        df_0, df_1 = self.db, account

        # Duplicates index is returned, just warns but they can be deleted.
        dup_index = utils.find_duplicates(df_0, df_1)
        if dup_index.any():
            logger.warning(f"Adding duplicate transactions:\n{df_1[dup_index]}")

        logger.debug(f"Account {df_1.shape} added to Database {df_0.shape}.")
        df = df_0.append(df_1, ignore_index=True)
        df.sort_values(by=["date", "amount"], ignore_index=True, inplace=True)
        utils.cast_category(df)
        self.db = df

    def filter(self, name=None, dates=None, cats=None):
        """Filter transactions based on tag or dates.

        Args:
            name (str): category or tag name.
            dates (tuple): (t0, t1) string "yyyy-mm-dd" or datetime.
            cats (dict): dictionary of category definitions.

        Returns:
            df (pd.DataFrame): filtered database subset.
        """
        df = self.db
        if name is not None:
            if cats is None:
                cats = []
            f = self.flt(name, cats)
            df = df[f]

        if dates is not None:
            f_dt = df["date"].between(dates[0], dates[1])
            df =  df.loc[f_dt]

        return df

    def flt(self, name, cats):
        """Inner function to create selection filter for tags & categories.

        Args:
            name (str): name of the category or tag.
            cats (dict): dictionary of category definitions.

        Returns:
            f(pd.Series): boolean index to select on database.
        """
        tag_srs = self.db["tag"]
        if name not in cats:
            f = tag_srs == name
            return f

        fs = pd.DataFrame(index=tag_srs.index)
        for tag in cats[name]:
            fs["new"] = self.flt(tag, cats)
            fs["flt"] = fs.any(axis=1)
        return fs["flt"]


class Notes(pd.Series):
    """Class to save notes of budget when extraordinary transactions happen.

    Inherits from pandas Series and adds a comment with a date.
    """

    def __init__(self, *args, **kwargs):
        """Pandas series initialization with default parameters."""
        super().__init__(*args, **kwargs)

    @classmethod
    def load(cls, fpath):
        """Constructor to create instance by loading notes data [date, note]

        Args:
            fpath (str): csv file path.

        Returns:
            Notes: instance containing loaded notes file.
        """
        srs = pd.read_csv(fpath, header=None, index_col=0,
                squeeze=True, parse_dates=True)
        return cls(srs.sort_index())

    def save(self, fpath):
        """Save Notes as .csv file.

        Args:
            fpath (str): file path.
        """
        self.to_csv(fpath, header=False, index=True)


if __name__ == "__main__":
    # If module directly run, load log configuration for all modules.
    import logging.config
    logging.config.fileConfig('../log/logging.conf')
    logger = logging.getLogger('database')

    import budget
    budget.main()

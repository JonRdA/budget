import logging
import pandas as pd

import utils

logger = logging.getLogger(__name__)

CATS = "../json/cats.json"

class Report():
    """Class for report evaluation: grouping & breakdown of transactions.

        Attributes:
            db (pd.DataFrame): complete transaction database (modified).
            freq (str): pandas offset alias for report frequency.
            tags(dict): list of category names for each supercategory.

            gdb (pd.DataFrame): grouped database of subs, resampled at freq.
        """

    def __init__(self, database, freq="M", cat_file = CATS):
        """Instanciate report object loading database.

        Args:
            database (Database): instance of Database class to use for report.
            freq (str): valid pandas offset string aliases.
            sups_file (str): path to supercategory definition JSON file.
        """
        self.f= freq 
        self.db = database.db.copy()
        self.cats = utils.load_json(cat_file)
        self.correct_account(2, lambda x: x/2)      # Custom for account #2
        #self.tdb = self._group_tags()
        self._group_tags()
        self.cdb = pd.DataFrame()
    
    def __repr__(self):
        """Print readable representation of Database instance."""
        return str(self.db)

    def correct_account(self, account, func):
        """Modify amount values of 'account' number based on 'func'.
        Args:
            account (int): number of account to modify.
            func (function): modification to perform.
        """
        filt = self.db["account"] == account
        self.db.loc[filt, "amount"]= self.db["amount"][filt].apply(func)
        logger.warning(f"Account {account} values modified.")
        
    def _group_tags(self):
        """Group & resample database storing as `tdb` tag-database attribute"""
        gpr = pd.Grouper(key="date", freq=self.f, closed="left")
        tdb = self.db.groupby([gpr, "tag"], observed=True).sum()

        # Pass grouped & resampled tags to dataframe format.
        self.tdb = tdb.unstack(level=-1)
        self.tdb.columns = self.tdb.columns.droplevel()

    def select_cat(self, cat):
        """Select category data from 'tdb', tag-database.

        Recursive implementation to select all the tags that form the category.
        If any tag is itself a cat, recursively iterates until tags found.
        Implements memoization by saving sum of every calculated category.
        
        I.e. select "expenses". First tag is "car", so calls itself with cat=car
        and returns sum of car, then goes to "finance" and repeats.

        Args:
            cat (str): category to select.

        Returns:
            df (pd.DataFrame): categories in columns per time rows.
        """
        df = pd.DataFrame()
        for name in self.cats[cat]:
            if self.is_cat(name):
                try:
                    df[name] = self.cdb[name]
                except KeyError:
                    df[name] = self.select_cat(name).sum(axis=1)
            elif name in self.tdb.columns:
                df[name] = self.tdb[name]

        self.cdb[cat] = df.sum(axis=1)      # Memoization
        return df

    def is_cat(self, name):
        """Check if string `name` is a category defined in file CATS."""
        return bool(self.cats.get(name, False))

    def timeline(self, name, dates=None):
        """Obtain timeline of a group between dates (inclusive).

        Args:
            name (str): category or tag name.
            dates (tuple): (t0, t1) str:"yyyy-mm-dd" or datetime.datetime.

        Returns:
            srs (pd.Series): group timeline with report's frequency.
        """
        if self.is_cat(name):
            srs = self.select_cat(name).sum(axis=1)
        else:
            srs = self.tdb[name]
        srs.name = name     # TODO necessary??
        
        if dates is None:
            return srs
        return srs[dates[0]: dates[1]]

    def breakdown(self, cat, dates=None):
        """Break down category into tags or subcats between `dates`(inclusive).

        Args:
            cat (str): category name.
            dates (tuple): (t0, t1) str:"yyyy-mm-dd" or datetime.datetime.

        Returns:
            srs (pd.Series): sum of transactions per tag in specidied period.
        """
        df = self.select_cat(cat)
        df.dropna(axis=1, how="all", inplace=True)

        if dates is not None:
            df = df.loc[dates[0]:dates[1], :]

        srs = df.sum()
        srs.name = cat
        return srs

        

if __name__ == "__main__":
    # If module directly run, load log configuration for all modules.
    import logging.config
    logging.config.fileConfig('../log/logging.conf')
    logger = logging.getLogger('report')

    import budget
    budget.main()

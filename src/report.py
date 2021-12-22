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
        Implements memoization by saving every calculated category.
        
        I.e. select "expenses". First tag is "car", so calls itself with cat=car
        and returns sum of car, then goes to "finance" and repeats.

        Args:
            cat (str): category to select.
        """
        df = pd.DataFrame()
        
        for tag in self.cats[cat]:
            if self.is_cat(tag):
                try:
                    srs = self.cdb[tag]
                except KeyError:
                    srs = self.select_cat(tag).sum(axis=1)

            elif tag in self.tdb.columns:
                srs = self.tdb[tag]

            df[tag] = srs

        self.cdb[cat] = df.sum(axis=1)      # Memoization
        return df

    def is_cat(self, name):
        """Check if string `name` is a category defined in file CATS."""
        return bool(self.cats.get(name, False))


if __name__ == "__main__":
    # If module directly run, load log configuration for all modules.
    import logging.config
    logging.config.fileConfig('../log/logging.conf')
    logger = logging.getLogger('report')

    import budget
    budget.main()

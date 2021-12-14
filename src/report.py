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
        self.freq = freq
        self.db = database.db.copy()
        self.cats = utils.load_json(cat_file)
        self.correct_account(2, lambda x: x/2)      # Custom for account #2
        self.group_tags()
    
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
        
    def group_tags(self):
        """Group & resample database storing as `tdb` tag-database attribute"""
        gpr = pd.Grouper(key="date", freq=self.freq, closed="left")
        tdb = self.db.groupby([gpr, "tag"], observed=True).sum()

        # Pass grouped & resampled tags to dataframe format.
        self.tdb = tdb.unstack(level=-1)
        self.tdb.columns = self.tdb.columns.droplevel()

    def group_cat(self, cat):
        # TODO recursive check if tag is a group. Change name.
        res = pd.DataFrame()
        for tag in self.cats[cat]:
            try:
                res[tag] = self.tdb[tag]
            except KeyError:
                pass

        return res



if __name__ == "__main__":
    # If module directly run, load log configuration for all modules.
    import logging.config
    logging.config.fileConfig('../log/logging.conf')
    logger = logging.getLogger('report')

    import budget
    budget.main()

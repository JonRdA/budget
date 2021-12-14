import logging
import pandas as pd

import utils

logger = logging.getLogger(__name__)

TAGS = "../json/tags.json"

class Report():
    """Class for report evaluation: grouping & breakdown of transactions.

        Attributes:
            db (pd.DataFrame): complete transaction database (modified).
            freq (str): pandas offset alias for report frequency.
            sups (dict): list of category names for each supercategory.

            tags (pd.DataFrame): resampled & grouped [sub, cat, sup] sums.
        """

    def __init__(self, database, freq="M", sups_file = SUPS):
        """Instanciate report object loading database.

        Args:
            database (Database): instance of Database class to use for report.
            freq (str): valid pandas offset string aliases.
            sups_file (str): path to supercategory definition JSON file.
        """
        self.db = database.db.copy().round({"amount":2})
        self.supd = utils.load_json(sups_file)
        self.freq = freq
        self.correct_account(2, lambda x: x/2)      # Custom for account #2
    
    def __repr__(self):
        """Print readable representation of Database instance."""
        return str(self.db)

#def breakdown(self, sup, t0, t1):
#    """Breakdown the groups

    def correct_account(self, account, func):
        """Modify amount values of 'account' number based on 'func'.
        Args:
            account (int): number of account to modify.
            func (function): modification to perform.
        """
        filt = self.db["account"] == account
        self.db.loc[filt, "amount"]= self.db["amount"][filt].apply(func)
        logger.warning(f"Account {account} values modified.")
        
    def group_by(self, tags):
        """Calculate summary df summing amounts for all cat & sub on freq.

        Perform a dataframe groupby on specified 'tag' & 'date' resampling to
        'freq' value. Groupby data per month and cat. If freq is greater than
        the entire timeline (10Y) it returns the total sum.

        Args:
            tags (tuple): tag type where to perform the grouping ["cat", "sub"].
            freq (str): frequency to resample the resulting time-series.

        Returns:
            df (pd.DataFrame): resampled date index and summed values per tag.
        """
        gpr = pd.Grouper(key="date", freq=self.freq, closed="left")
        df = self.db.groupby([gpr, *tags], observed=True).sum()
        return df

    def group_tags(self, gpath=GROUPS):
        """Categorize transactions by grouping in tags ["cat", "sub", "sup"].

        Stores as attribute 'tags' & 'sups'.
        'tags' is the sum of all tags resampled to the frequency of the report.
        'sups' is the breakdown in categories of the groups or supercategories.

        Args:
            freq (str): frequency to resample the resulting time-series.
            gpath (str): path to group json file.
        """
        # Group-by of transaction database.
        cat = self.group_by(["cat"])
        sub = self.group_by(["sub"])

        # Pass grouped tags to dataframe format.
        tags = cat.unstack(level=-1).join(sub.unstack(level=-1))
        tags.columns = tags.columns.droplevel()

        # Ass code related to subs to be deleted. TODO
        sups = {}
        # Group-by of categories db. Select group from cat & add sum to tags.
        lvls = cat.index.get_level_values(0)
        d = utils.load_json(gpath)
        for k, v in d.items():
            cats = cat.loc[(lvls, v), :]
            sups[k] = cats
            tags.loc[:, k] = cats.groupby(pd.Grouper(level="date")).sum()

        self.tags = tags
        self.sups = sups



if __name__ == "__main__":
    # If module directly run, load log configuration for all modules.
    import logging.config
    logging.config.fileConfig('../log/logging.conf')
    logger = logging.getLogger('report')

    import budget
    budget.main()

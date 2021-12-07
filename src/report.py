import logging
import datetime
import numpy as np
import pandas as pd

import utils

logger = logging.getLogger(__name__)

VIEW_COLS = ["date", "description", "amount", "cat", "sub"]       # Represent transaction
CAT_COLS = ["y", "m", "cat", "sub", "account"]      # Category dtype

class Report():
    """Class for report printing, visualizing and saving

        Attributes:
            db (pd.DataFrame): complete transaction database (modified).
            sup (dict): summary dataframe (sum) for all supercategories.
            msup (pd.DataFrame): monthly summary of supercategories.

        """

    def __init__(self, database):
        """Instanciate report object loading database.

        Args:
            db (pd.DataFrame): db attribute of Database object.
        """
        self.db = database.db.copy()
        self.correct_account(2, lambda x: x/2)      # Custom for account #2
    
    def __repr__(self):
        """Print readable representation of Database instance."""
        return str(self.db[VIEW_COLS])

    def correct_account(self, account, func):
        """Modify amount values of 'account' number based on 'func'.
        Args:
            account (int): number of account to modify.
            func (function): modification to perform.
        """
        filt = self.db["account"] == account
        self.db.loc[filt, "amount"]= self.db["amount"][filt].apply(func)
        logger.warning(f"Account {account} values modified.")
        
    def load_sup(self, fpath):
        """Load 'groups' (dict) from json & save attribute with transaction sum.

        Args:
            fpath (str): path to json file containing cat groups.
        """
        s = {}
        d = utils.load_json(fpath)
        df = self.db.groupby(["y", "m", "cat"], observed=True).sum()
        lvls = df.index.levels

        for k, v, in d.items():
            s[k] = df.loc[(lvls[0], lvls[1], v), :]

        self.sup = s
        self._monthly_sup()

    def _monthly_sup(self):
        """Calculate monthly summary sup and save as date index df attribute."""
        df = pd.DataFrame()
        for k, v in self.sup.items():
            df[k] = v.groupby(["y", "m"], observed=True).sum()

        utils.date_index(df)
        self.msup= df

    # TODO part of summary function to build.
    def expense_evolution(self):
        df = self.msup
        ess = df["essential"]
        non = df["nonessential"]
        ind = ess.index

        plt.bar(ind, ess)
        plt.bar(ind, non, bottom=ess, color="r")
        plt.show()

    # DEPRECATED DELETE?
    def select_group(self, group, col="cat"):
        """Modify database selectring transactions listed in 'group'.
        
        Args:
            group (list): group of categores.
            col (str): column to perform selection, default is "cat".
        """
        filt = self.db[col].isin(group)
        self.db = self.db[filt]

        # Remove unused categories in categorical data.
        #rm_func = lambda x: x.cat.remove_unused_categories()
        #self.db[CAT_COLS] = self.db[CAT_COLS].apply(rm_func, axis=0)

if __name__ == "__main__":
    # If module directly run, load log configuration for all modules.
    import logging.config
    logging.config.fileConfig('../log/logging.conf')
    logger = logging.getLogger('report')

    import budget
    budget.main()

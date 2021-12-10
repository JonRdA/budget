import logging
import pandas as pd

import utils

logger = logging.getLogger(__name__)

CAT_COLS = ["y", "m", "cat", "sub", "account"]      # Category dtype
GROUPS = "../json/groups.json"

class Report():
    """Class for report printing, visualizing and saving

        Attributes:
            db (pd.DataFrame): complete transaction database (modified).
            tags (pd.DataFrame): resampled & grouped transaction sum.
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
        
    def group_by(self, tag, freq="M"):
        """Calculate summary df summing amounts for all cat & sub on freq.

        Perform a dataframe groupby on specified 'tag' & 'date' resampling to
        'freq' value. Groupby data per month and cat.

        Args:
            tag (str): tag type where to perform the grouping ["cat", "sub"].
            freq (str): frequency to resample the resulting time-series.

        Returns:
            df (pd.DataFrame): resampled date index and summed values per tag.
        """
        gpr = pd.Grouper(key="date", freq=freq)
        df = self.db.groupby([gpr, tag], observed=True).sum()
        df.columns = [tag]      # for correct multindex when unpacked.
        return df

    def group_tags(self, freq="M", gpath=GROUPS):
        """Categorize transactions by grouping in tags ["cat", "sub", "sup"].

        Loads a summary dataframe with categorized data and resmpled to 'freq'.
        Sums all the values of the new resampling period per tag.
        Saves dataframe as 'tags' atribute.

        Args:
            freq (str): frequency to resample the resulting time-series.
            gpath (str): path to group json file.
        """
        d = utils.load_json(gpath)

        # Group-by of transaction database.
        cat = self.group_by("cat", freq)
        sub = self.group_by("sub", freq)

        # Pass grouped tags to dataframe format.
        tags = cat.unstack(level=-1).join(sub.unstack(level=-1))
        tags.columns.names=["ttype", "tag"]

        # Group-by of categories db. Select group from cat & add sum to tags.
        lvls = cat.index.get_level_values(0)
        for k, v in d.items():
            cats = cat.loc[(lvls, v), :]
            tags.loc[:, ("sup", k)] = cats.groupby(pd.Grouper(level="date")).sum()

        self.tags = tags


if __name__ == "__main__":
    # If module directly run, load log configuration for all modules.
    import logging.config
    logging.config.fileConfig('../log/logging.conf')
    logger = logging.getLogger('report')

    import budget
    budget.main()

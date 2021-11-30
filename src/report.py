import logging
import numpy as np
import pandas as pd

import utils

logger = logging.getLogger(__name__)

VIEW_COLS = ["date", "description", "amount", "cat", "sub"]       # Represent transactaction
CAT_COLS = ["y", "m", "cat", "sub", "account"]      # Category dtype

class Report():
    """Class for report printing, visualizing and saving."""

    def __init__(self, database):
        """Instanciate report object loading database.

        Args:
            db (pd.DataFrame): db attribute of Database object.
        """
        self.db = database.db.copy()
    
    def __repr__(self):
        """Print readable representation of Database instance."""
        return str(self.db[VIEW_COLS])

    def select_group(self, group, col="cat"):
        """Select in database transactions whose column is listed in 'group'.
        
        Args:
            group (list): group of categores.
            col (str): column to perform selection, default is "cat".
        """
        filt = self.db[col].isin(group)
        self.db = self.db[filt]

        # Remove unused categories in categorical data.
        rm_func = lambda x: x.cat.remove_unused_categories()
        self.db[CAT_COLS] = self.db[CAT_COLS].apply(rm_func, axis=0)

if __name__ == "__main__":
    # If module directly run, load log configuration for all modules.
    import logging.config
    logging.config.fileConfig('../log/logging.conf')
    logger = logging.getLogger('report')

    import budget
    budget.main()

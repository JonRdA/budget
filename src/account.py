import logging
import numpy as np
import pandas as pd

import utils

logger = logging.getLogger(__name__)

class Account(pd.DataFrame):
    """Partial transaction database with one account information.

    Inherited from pandas dataframe contains all transactions sorted by date
    as well as their amount, category, subcategory and account.
    """
    
    def __init__(self, *args, **kwargs):
        """Pandas dataframe initialization with default parameters."""
        super().__init__(*args, **kwargs)
        self.sort_values(by=["date", "amount"], ignore_index=True, inplace=True)

        nan_ind = self.loc[:,["date","description","amount"]].isna().any(axis=1)
        if nan_ind.any():
            nan_rows = list(self[nan_ind].index)
            raise ValueError(f"Account '{self.shape}' has 'nan' in rows {nan_rows}.")

    @classmethod    
    def load(cls, fpath, n_account):
        """Constructor to create instance by loading transactions data.

        Format: [date, description, amount, category, subcat] without header.

        Args:
            fpath (str): csv file path.
            n_account (int): number of account to ad as column.

        Returns:
            Account: instance containing loaded transaction file.
        """
        dt_parser = lambda x : pd.to_datetime(x, format="%d/%m/%Y")
        cname = ["date", "description", "amount", "cat", "sub"]
        ctype = {"description": "string"}

        df = pd.read_csv(fpath, header=None, names=cname, dtype=ctype,
            parse_dates=[0], date_parser=dt_parser)
        df.dropna(how="all", inplace=True)

        df["account"] = n_account
        logger.debug(f"Account {df.shape} loaded.")

        return cls(df)
        
    def modify_cats(self, func, *args, **kwargs):
        """Modify inplace category and sub-category using passed function.

        Args:
            func (function): modifying function to be applied.

        Returns:
            None
        """
        if not self.loc[:, ["cat", "sub"]].isna().all().all():
            logger.warning("Overwriting non-empyt categories")
        self[["cat", "sub"]] = self.apply(func, axis=1, *args, **kwargs)

    def save(self, fpath):
        """Save account as .csv file.

        Args:
            fpath (str): file path.
        """
        cols = ["date", "description", "amount", "cat", "sub"]
        self.to_csv(fpath, header=False, index=False, float_format="%.2f",
            date_format="%d/%m/%Y", columns=cols)

if __name__ == "__main__":
    # If module directly run, load log configuration for all modules.
    import logging.config
    logging.config.fileConfig('../log/logging.conf')
    logger = logging.getLogger('account')

    import budget
    budget.main()

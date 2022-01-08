import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import plot
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
        # Modify account #2 values in half, shared account.
        mdb = correct_account(database.db, 2, lambda x: x/2)

        self.cats = utils.load_json(cat_file)
        self.tdb = group_tags(mdb, freq)
        self.cdb = pd.DataFrame()
    
    def __repr__(self):
        """Print readable representation of Database instance."""
        return str(self.tdb)

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

# Report summary calculations

    def timeline(self, name, dates=None):
        """Obtain timeline of a group between dates (inclusive).

        Args:
            name (str): category or tag name.
            dates (tuple): (t0, t1) str:"yyyy-mm-dd" or datetime.

        Returns:
            srs (pd.Series): group timeline with report's frequency.
        """
        if self.is_cat(name):
            srs = self.select_cat(name).sum(axis=1)
        else:
            srs = self.tdb[name]
        srs.name = name
        srs = srs[srs!=0.0].dropna()
        
        if dates is None:
            return srs
        return srs[dates[0]: dates[1]]

    def timelines(self, cat, dates=None):
        """Obtain timeline of a category between dates (inclusive).

        Returns the lower levels (inmediate subcategory) tag or cat's timeline.

        Args:
            cat (str): category name.
            dates (tuple): (t0, t1) str:"yyyy-mm-dd" or datetime.

        Returns:
            df (pd.DataFrame): category's component's timeline.
        """
        df = self.select_cat(cat)
        df.replace({0.0:np.nan}, inplace=True)
        df.dropna(axis=0, how="all", inplace=True)

        if dates is None:
            return df
        return df[dates[0]: dates[1]]

    def breakdown(self, cat, dates=None):
        """Break down category into tags or subcats between `dates`(inclusive).

        Args:
            cat (str): category name.
            dates (tuple): (t0, t1) string "yyyy-mm-dd" or datetime.

        Returns:
            srs (pd.Series): sum of transactions per tag in specidied period.
        """
        df = self.select_cat(cat)
        df.dropna(axis=1, how="all", inplace=True)

        if dates is not None:
            df = df.loc[dates[0]:dates[1], :]

        srs = df.sum()
        srs.name = cat
        return srs[srs!=0.0].dropna()

# Result plotting

    def plot_cat(self, cat, dates=None):
        """Track category by plotting timeline and breakdown.

        Args:
            cat (str): category or tag name.
            dates (tuple): (t0, t1) str:"yyyy-mm-dd" or datetime.
        """
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20, 9))
        ax1.set_position([.05, .10, .55, .80])
        ax2.set_position([.65, .10, .30, .80])
        tl = self.timeline(cat, dates)
        bd = self.breakdown(cat, dates)
        
        plot.bar(tl, ax=ax1)
        ax1.set_title(f"{cat.title()} transactions timeline")
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Amount [€]")

        plot.pie(bd, ax=ax2)
        ax2.set_title(f"{cat.title()} transactions breakdown")

        print(tl, bd, sep=2 * "\n")

    def plot_cat_bd(self, name, dates=None):
        """Track category by plotting stacked bar breakdown plot.

        Args:
            cat (str): category or tag name.
            dates (tuple): (t0, t1) str:"yyyy-mm-dd" or datetime.
        """

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16, 9))
        ax.set_position([.07, .10, .90, .80])
        df = self.timelines(name, dates)
        
        plot.sbar(df, ax=ax)
        ax.set_title(f"{name.title()} timeline breakdown")
        ax.set_xlabel("Time")
        ax.set_ylabel("Amount [€]")

        print(df)
        

# Functions out of class for initialization

def correct_account(db, account, func):
    """Modify amount `db` values of `account` number based on 'func'.

    Args:
        db (pd.DataFrame): Database object's db attribute.
        account (int): number of account to modify.
        func (function): modification to perform.

    Returns:
        mdb (pd.DataFrame): modified database.
    """
    mdb = db.copy()
    filt = mdb["account"] == account
    mdb.loc[filt, "amount"]= mdb["amount"][filt].apply(func)
    logger.warning(f"Account {account} values modified.")
    return mdb
    
def group_tags(db, freq):
    """Group database `db` by tag & resample with frequency `freq`.

    Args:
        db (pd.DataFrame): Database object's db attribute.
        freq (str): valid pandas offset string aliases.
    
    Returns:
        tdb (pd.DataFrame): tag-database.
    """
    gpr = pd.Grouper(key="date", freq=freq, closed="left")
    tdb = db.groupby([gpr, "tag"], observed=True).sum()

    # Pass grouped & resampled tags to dataframe format.
    tdb = tdb.unstack(level=-1)
    tdb.columns = tdb.columns.droplevel()
    return tdb

if __name__ == "__main__":
    # If module directly run, load log configuration for all modules.
    import logging.config
    logging.config.fileConfig('../log/logging.conf')
    logger = logging.getLogger('report')

    import budget
    budget.main()

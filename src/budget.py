import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import utils
from report import Report
from account import Account
from database import Database

logger = logging.getLogger(__name__)

CAT_FPATH = "../json/transaction_tags.json"

def auto_tag(csv_path, csv_save_path=None, json_path=CAT_FPATH):
    """Modify transaction csv file by filling cat & sub using dictionary data.

    Args:
        csv_path (str): path to csv transaction file.
        json_path (str): path to json dictionary defining cats.

    Returns:
        None
    """
    if csv_save_path == None:
        csv_save_path = csv_path
        
    acc = Account.load(csv_path, 0)
    tag_dict = utils.load_json(json_path)
    acc.modify_tags(utils.assign_tags, d=tag_dict)
    acc.save(csv_save_path)

    flp = int((len(acc) - acc["cat"].isna().sum()) / len(acc) * 100)
    logger.info(f"{flp} % of cats were filled on file {csv_save_path}.")

def acc_to_db():
    """Accounts to database. Load account info, merge and save database."""
    a1 = Account.load("../input/account_01.csv", 1)
    a2 = Account.load("../input/account_02.csv", 2)
    
    d = Database(a1)
    d.add_account(a2)

    d.save("../db/database.csv")

def plot_pie(srs, title=""):
    """Plot donut shaped pie chart.

    Args:
        srs (pd.Series): same sign data with labels in index.

    Returns:
        p (Figure): generated plot.
    """
    if srs.min() < 0:
        raise ValueError(f"Negative values in series {srs}")


    fig, ax = plt.subplots(figsize=[8, 10], dpi=200)
    ax.set_title(title)
    names = [i.title() for i in srs.index]

    ax.pie(srs, labels=names, wedgeprops={'linewidth':7, 'edgecolor':'white'})
    hole = plt.Circle((0,0), .7, color="white")
    ax.add_artist(hole)

    plt.show()
    return fig

def plot_bars(srs):

    height = srs
    bars = srs.index
    x_pos = np.arange(len(bars))

    # Create bars and choose color
    plt.bar(x_pos, height, color = (0.5,0.1,0.5,0.6))

    # Add title and axis names
    plt.title('My title')
    plt.xlabel('categories')
    plt.ylabel('values')

    # Create names on the x axis
    plt.xticks(x_pos, bars)

    # Show graph
    plt.show()
    return

def test():
    """Main function to test developing code."""
    
    d = Database.load("../db/database.csv")
    r = Report(d)

    db = d.db
    dr = r.db

    return

    # Select a subset of cats
    dict_group = utils.load_json("../json/groups.json")
    exp = dict_group["expenses"]

    r = Report(d)

    # Report on cats per month.
    gb = d.db.groupby(["y", "m", "cat"])
    q = gb.sum()
    
    # Report on cats per month.
    gb = d.db.groupby("cat")
    q = gb.sum()

    # Report of certain cat in time.
    cate = "leisure"
    filt = a.db["cat"] == cate
    db = a.db[filt]
    gb = db.groupby(["y", "m"])
    q = gb.sum()

def main():
    test()

    #acc_to_db()
    #auto_tag("../input/auto_tag.csv")

if __name__ == "__main__":
    # If module directly run, load log configuration for all modules.
    import logging.config
    logging.config.fileConfig('../log/logging.conf')
    logger = logging.getLogger('database')

    main()

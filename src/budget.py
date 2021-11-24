import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import utils
from account import Account
from database import Database

logger = logging.getLogger(__name__)

CAT_FPATH = "../json/transaction_cats.json"

def fill_cats(csv_path, csv_save_path=None, json_path=CAT_FPATH):
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
    cat_dict = utils.load_json(json_path)
    acc.modify_cats(utils.detect_cat, d=cat_dict)
    acc.save(csv_save_path)

    flp = int(len(acc) - acc["cat"].isna().sum() / len(acc) * 100)
    logger.info(f"{flp} % of cats were filled on file {csv_save_path}.")

def test():
    """Main function to test developing code."""
    pass

def main():
    test()
    
    a1 = Account.load("../input/account_01.csv", 1)
    a2 = Account.load("../input/account_02.csv", 2)

    d = Database(a1)
    d.add_account(a2)
    return

    # Report on cats per month.
    gb = d.db.groupby(["y", "m", "cat"])
    q = gb.sum()
    
    # Report on cats per month.
    gb = d.db.groupby("cat")
    q = gb.sum()
    plt.pie(q["amount"].abs(), labels=q.index)
    plt.show()
    return

    # Report of certain cat in time.
    cate = "leisure"
    filt = a.db["cat"] == cate
    db = a.db[filt]
    gb = db.groupby(["y", "m"])
    q = gb.sum()


if __name__ == "__main__":
    # If module directly run, load log configuration for all modules.
    import logging.config
    logging.config.fileConfig('../log/logging.conf')
    logger = logging.getLogger('database')

    main()

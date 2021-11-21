import logging
import numpy as np
import pandas as pd

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


def main():
    fill_cats("../input/nocat.csv", "../input/nocat_result.csv")
    return
    a1 = Account.load("../input/nocat.csv", 1)
    

    #a2 = Account.load("../input/track_account_02.csv", 2)
    #a1 = Account.load("../input/test0.csv", 1)
    #a2 = Account.load("../input/test1.csv", 1)

    cat_dict = utils.load_json()

    a1.loc[8, "cat"] = 8
    a1.modify_cats(utils.detect_cat, d=cat_dict)

    dbs = Database(a1)

    #print(dbs)
    print(dbs.db.dtypes)
    return



    # Report on cats per month.
    gb = a.db.groupby(["y", "m", "cat"])
    q = gb.sum()

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

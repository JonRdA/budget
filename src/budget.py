import logging
import numpy as np
import pandas as pd

from account import Account
from database import Database
import utils

logger = logging.getLogger(__name__)

def main():
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

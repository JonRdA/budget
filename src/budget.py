import logging
import pandas as pd

from account import Account
from database import Database
import utils

logger = logging.getLogger(__name__)



def main():
#    a1 = Account.load("../input/track_account_01.csv", 1)
#    a2 = Account.load("../input/track_account_02.csv", 2)
    a1 = Account.load("../input/test0.csv", 1)
    a2 = Account.load("../input/test1.csv", 1)
    """If not empty.
    filter same cat
    check dates
    filter dates on both dfs.
    find duplicates only in dates.
    """


    a = Database(a1)

    #a.add_account(a1)
    a.add_account(a2)
    print(a)
    print(a.db.dtypes)
    return a.db

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

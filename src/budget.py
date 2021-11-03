import logging
import pandas as pd

from account import Account
from database import Database
import utils

logger = logging.getLogger(__name__)


def main():
    a1 = Account.load("../input/track_account_01.csv", 1)
    a2 = Account.load("../input/track_account_02.csv", 2)
    print("accounts")
    print(a1.dtypes, a2.dtypes)

    a = Database()

    a.add_account(a1)
    print("after account 1")
    print(a.db.dtypes)
    a.add_account(a2)
    print("after account 2")
    print(a.db.dtypes)

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

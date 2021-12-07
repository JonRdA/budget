import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import plot
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

def test():
    """Main function to test developing code."""
    
    import datetime
    #d = Database.load("../db/database.csv")
    d = Database.load("../db/test_db.csv")
    
    r = Report(d)

    df = r.db

    g = df.groupby(["y", "m", "sub"], observed=True).sum()
    print(g.head(40))


    return
    r.load_sup("../json/groups.json")

    z = r.msup
    print(z)
    
    return

    exp = r.sup["expenses"]
    inc = r.sup["income"]

    mexp = a["expenses"]
    minc = a["income"]

    print(a)

    a = a["expenses"].squeeze()
    plot.bars(a)

    #r.msup.plot.bar()
    #plt.show()

    return

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

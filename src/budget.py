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
GROUPS = "../json/groups.json"

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
    #d = Database.load("../db/database.csv")
    d = Database.load("../db/test_db.csv")
    r = Report(d)
    df = r.db

    g1 = r.group_by("cat")
    g1 = g1.unstack(level=-1)
    g2 = r.group_by("sub")
    g2 = g2.unstack(level=-1)
    gg = g1.join(g2)

    d = utils.load_json(GROUPS)
    g1 = r.group_by("cat")
    lvls = g1.index.get_level_values(0)
    d1 = lvls

    v = d["expenses"]

    z = g1.loc[(d1, v), :]
    print(z)
    return
    #z = g1.loc[(
    print(z)


    r.load_sup(GROUPS)
    return
    z = df.loc[(lvls[0], "car"), :]
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

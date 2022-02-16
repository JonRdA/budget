import logging
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import plot
import utils
from report import Report
from account import Account
from database import Database, Notes

logger = logging.getLogger(__name__)

AUTOTAG = "../json/auto_tag.json"

def auto_tag(csv_path, csv_save_path=None, json_path=AUTOTAG):
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

    flp = int((len(acc) - acc["tag"].isna().sum()) / len(acc) * 100)
    logger.info(f"{flp} % of cats were filled on file {csv_save_path}.")

def acc_to_db():
    """Accounts to database. Load account info, merge and save database."""
    a1 = Account.load("../input/account_01.csv", 1)
    a2 = Account.load("../input/account_02.csv", 2)
    a3 = Account.load("../input/account_03.csv", 3)
    a4 = Account.load("../input/account_04.csv", 4)
    
    d = Database(a1)
    d.add_account(a2)
    d.add_account(a3)
    d.add_account(a4)

    d.save("../db/database.csv")

def test():
    """Main function to test developing code."""

    d = Database.load("../db/database.csv")
    #d = Database.load("../db/test_db.csv")

    r = Report(d, freq="m")

    t0 = datetime.datetime(2021,9,1)
    t1 = datetime.datetime(2022,5,1)


    inc = r.timeline("income", dates=(t0, t1))
    exp= r.timeline("expenses", dates=(t0, t1))
    df = pd.concat([inc, exp], axis=1)
    #plot.gbar(df)

    ##r.cplot_cat_bd("car", dates=(t0, t1))
    #r.cplot_cat_bd("expenses", dates=(t0, t1))
    #r.cplot_cat_bd("essential", dates=(t0, t1))
    #r.cplot_cat_bd("nonessential", dates=(t0, t1))
    #r.cplot_cat_bd("leisure", dates=(t0, t1))
    #r.cplot_cat_bd("personal", dates=(t0, t1))

    r4= r.timeline("r4")
    print(r4)
    print(r4.sum())

    funds = r.timeline("funds", dates=(t0, t1))
    print(funds)
    print(funds.sum() + 453.28)

    plt.show()

def main():
    acc_to_db()
    #auto_tag("../input/auto_tag.csv")

    test()

if __name__ == "__main__":
    # If module directly run, load log configuration for all modules.
    import logging.config
    logging.config.fileConfig('../log/logging.conf')
    logger = logging.getLogger('budget')
    
    pd.set_option("display.float_format", "{:.2f}".format)

    main()

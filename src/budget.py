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

def export_modified_transactions(db, tag, dates, export_path):
    """Export filtered transactions from tag but modified (account 2 / 2).

    Current modification are:
        account 2 values divided by 2
        account 4 values divided by 3

    Args:
        db (database): db from which to select and modify.
        tag (str): tag to filter from database.
        dates (tuple): (t0, t1) str:"yyyy-mm-dd" or datetime.
        export_path (str).

    Returns
        pd.DataFrame: filtered and modified transactions.
    """
    r = Report(db, freq="m")
    mdb = utils.correct_account(db.db, 2, lambda x: x/2)
    mdb = utils.correct_account(mdb, 4, lambda x: x/3)
    mdb = Database(mdb)
    filtered = mdb.filter(tag, dates, cats=r.cats)
    filtered.to_csv(export_path)

def test():
    """Main function to test developing code."""

    d = Database.load("../db/database.csv")

    r = Report(d, freq="m")

    #export_modified_transactions(d, "vacation", ("2021-04-01", "2022-08-01"), "../input/vacation2.csv")
    #f = d.filter("present", cats=r.cats)

    t0 = datetime.datetime(2021,9,1)
    t1 = datetime.datetime(2022,12,1)

#    t0 = datetime.datetime(2022,3,1)
    #t1 = datetime.datetime(2022,12,1)
    #f = d.filter("r4", cats=r.cats, dates=(t0, t1))
    #print(f)
    #print(f.sum(numeric_only=True))
    #return 8


    #inc = r.timeline("income", dates=(t0, t1))
    #exp= r.timeline("expenses", dates=(t0, t1))
    #df = pd.concat([inc, exp], axis=1)
    #plot.gbar(df)

    r.plot_cat_bd("food", dates=(t0, t1))
    r.plot_cat_bd("buy", dates=(t0, t1))
    r.plot_cat_bd("car", dates=(t0, t1))
    r.plot_cat_bd("expenses", dates=(t0, t1))
    #r.plot_cat_bd("essential", dates=(t0, t1))
    #r.plot_cat_bd("vacation", dates=(t0, t1))
    #r.plot_cat_bd("nonessential", dates=(t0, t1))
    #r.plot_cat_bd("leisure", dates=(t0, t1))
    #r.plot_cat_bd("personal", dates=(t0, t1))
    #r.plot_cat_bd("balance", dates=(t0, t1))       # no good graph, caution
    #r.plot_cat_bd("income", dates=(t0, t1))
    plt.show()

def main():
    #acc_to_db()
    #auto_tag("../input/auto_tag.csv")

    test()

if __name__ == "__main__":
    # If module directly run, load log configuration for all modules.
    import logging.config
    logging.config.fileConfig('../log/logging.conf')
    logger = logging.getLogger('budget')
    
    pd.set_option("display.float_format", "{:.2f}".format)

    main()

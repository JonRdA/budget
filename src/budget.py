import pandas as pd

from account import Account
from database import Database



def main():
    a1 = Account.load("../input/test0.csv", 2)
    a2 = Account.load("../input/test1.csv", 2)

    q = Database(a1)
    print(q)
    q.add_account(a2)
    print(q)


if __name__ == "__main__":
    main()

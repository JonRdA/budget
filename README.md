# BUDGET REPORT
Budget analysing and reporting of bank income-outcome:
 * Read transaction files from different banks/accounts.
 * Merge a unified database.
 * Categorize automatically each transaction.
 * Report and print charts with expense breakdown and monthly evolution.

## CONCEPS
 * `tag`: descriptive word of transaction.
 * `cat`: category that grops similar tags. Can be composed of other cats too.

## FILES
Program needs different input files.
 * `account_transactions.csv` single account transacction files in `input/`.
 * `main_database.csv` joined account database files in `db/`
 * `auto_tag.json` to automatically tag account file in `json/`.
 * `cats.json` file to load cats to perform reports in `json/`.

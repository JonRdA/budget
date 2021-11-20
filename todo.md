# BUDGET
Expense tracking, classification and report automation.

## DEVELOPING
[ ] Everything in account with modifying factors. is number, when goint to database pass as categorical?
[ ] Make inline modification function for cat & sub.
[ ] Make wrapper function with func parameter to modify cat and sub.
[ ] Categorize automatically based on dictionary.
[ ] Categorize according to new cats.
[ ] Start with reporting options. Temporal & cat-wise.
[x] Change inheritance in Database.
[x] parece que al add account se pierde el datatype. solve BUG
[x] Create JSON files for cat, sup, sub.

## IDEAS
* Have new class, Report, where db is modified for different accounts.
* How to treat special accounts? Joint ones. Should be computed specially.
  when reporting. The database must only contain raw info.
* Main database save raw info, add more when loading Y-M.

## TO IMPROVE
* Database.add_account() -> only check account VS Database, it will detect 2 
  duplicates in account, which should not.
* Add retroactive database category modification options.

## LOAD, CLASSIFY & UPDATE DATABASE
[x] Load transactions from different accounts.
[x] Load account number to take into account while reporting.
[ ] Assign 'cat' and 'sub' from dictionay (JSON?)
[ ] Assign manually missing categories.
[x] Add to database.

## REPORT 
[ ] Select based on dictionary lists (supercategories)
[ ] Show graph of expenses timeline of given cat or subcat.
[ ] Filter per month and cat.
[ ] List all cat or subcat expenses per month.
[ ] Think OOP -> Report: 
 [ ] Load accounts fix
 [ ] Fix differences (/2 second one)
 [ ] Join
 
## DATABASE
[x] Sorted by date.

## FILES
[ ] Input tracking files, partial.
[ ] Central database with all information.
[ ] Dictionary for automatic categorization.
[ ] Dictionary for catefoty selection.

## WATCHOUT!
[x] Check for collisions when adding to database.

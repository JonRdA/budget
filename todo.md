# BUDGET
Expense tracking, classification and report automation.

## DEVELOPING
[x] Change inheritance in Database.
[x] parece que al add account se pierde el datatype. BUG
[ ] Start with reporting options. Temporal & cat-wise.
[x] Create JSON files for cat, sup, sub.
[ ] Categorize automatically based on dictionary.

## IDEAS
* How to treat special accounts? Joint ones. Should be computed specially
  when reporting. The database must only contain raw info.
* Main database loaded for reporting. Report object adds more info: Y-M-sup.

## TO IMPROVE
* Database.add_account() -> only check coliding dates to avoid deleting any
  duplicate that should be okay.

## LOAD, CLASSIFY & UPDATE DATABASE
[x] Load transactions from different accounts.
[x] Load account number to take into account while reporting.
[ ] Assign 'cat' and 'sub' from dictionay (JSON?)
[ ] Assign manually missing categories.
[ ] Add to database.

## REPORT 
[ ] Show graph of expenses timeline of given cat or subcat.
[ ] Filter per month and cat.
[ ] List all cat or subcat expenses per month.
[ ] Assing 'super' cat.
[ ] Think OOP -> Report: 
 [ ] Load accounts fix
 [ ] Fix differences (/2 second one)
 [ ] Join
 
## DATABASE
[x] Sorted by date.
[ ] Year & month columns for grouping????
[ ] 'sup' supercategory for reporting how to do it????
[ ] Update supercategories method.

## FILES
[ ] Input tracking files, partial.
[ ] Central database with all information.
[ ] Supercategories for reporting.
[ ] Dictionary for automatic categorization.

## WATCHOUT!
[x] Check for collisions when adding to database.

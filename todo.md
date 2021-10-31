# BUDGET
Expense tracking, classification and report automation.

## DEVELOPING
[ ] Database, OOP inherited from pd.DataFrame? Should contain Y & M?

## IDEAS
* How to treat special accounts? Joint ones. Should be computed specially
  when reporting. The database must only contain raw info.

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
[ ] Sorted by date.
[ ] Year & month columns for grouping.
[ ] 'sup' supercategory for reporting.
[ ] Update supercategories method.

## FILES
[ ] Input tracking files, partial.
[ ] Central database with all information.
[ ] Supercategories for reporting.
[ ] Dictionary for automatic categorization.

## WATCHOUT!
[ ] Check for collisions when adding to database.

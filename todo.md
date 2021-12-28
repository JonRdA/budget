# BUDGET
Expense tracking, classification and report automation.

# TODO
- [x] Group loading from 2 files, cats, sups
- [x] Build wrapper methods `timeline` & `breakdown`
- [x] Improve plots, pie, bar sbar (moth centered, width auto etc.)
- [ ] Database date, tag, cat filtering
- [ ] Report predefined analysis options wrapping `breakdown` & `timeline`.

## REPORTING
Report has functions `timeline(dates, tags)`-> df &
`breakdown(tag, dates)`-> series whose 
results can be plotted with `pie` `bar` & `bars`.
* Use tags dataframe to obtain breakdown & timeline.
* Breakdown, horizontal cut of selected columns, sum.
* Timeline, vertical cut of selected dates, one column.

# IDEAS
Plotting colors.


# IMPROVEMENTS
* Database.add_account() -> only check account VS Database, it will detect 2 
  duplicates in account, which should not.

# FILES
 * Transactions: [individual accounts, database]
 * JSON:  [auto_tag, cats]


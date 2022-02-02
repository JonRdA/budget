# BUDGET
Expense tracking, classification and report automation.

# TODO
- [ ] Modify expenses as full subcat
- [ ] Rethink fund categories
- [ ] Design fund breakdown
- [x] Database filtering based on cats
- [x] Group loading from 2 files, cats, sups
- [x] Build wrapper methods `timeline` & `breakdown`
- [x] Improve plots, pie, bar sbar (moth centered, width auto etc.)
- [x] Database date, tag, cat filtering
- [x] Report predefined analysis options wrapping `breakdown` & `timeline`.
- [x] Use plot init for automatic plotting.


# IDEAS
Plotting colors.
Reporting balance options. Expenses Vs Income. Expense breakdown Ess/Non.

# IMPROVEMENTS
* Database.add_account() -> only check account VS Database, it will detect 2 
  duplicates in account, which should not.

# FILES
 * Transactions: [individual accounts, database]
 * JSON:  [auto_tag, cats]


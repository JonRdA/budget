# BUDGET
Expense tracking, classification and report automation.

# TODO
- [x] Pass nonessential to 'buy' cat.
- [ ] Complete reporting predefined options.
- [ ] Set daily usage functions.
- [ ] Study color, load globally?
- [x] Change cats with rules.

## REPORTING
- [ ] Expense breakdown. For any month or all. Pie chart.
- [ ] Time series, for any cat/group, evolution. Barplot.
    * Between 2 specific dates (months).
    * Add barplot for any cat.
    * Barplot accepts 2 or more inputs.
    * Issue with selecting groups, databases.. 2 reports?

# IDEAS
* Plot (pie & bar) for any group & time span. 
    * Group needs a tag_type, list of tags.
    * Time needs 2 datetimes, start end.
* Do not like report changing database with group. How to handle?
  Separate expenses, incomes and work with both databases. All are needed at a
  groupby level. They are summaries of groups over time, only collide on monthly
  basis. Report load group databases? Load groups as global vars at script?

# IMPROVEMENTS
* Database.add_account() -> only check account VS Database, it will detect 2 
  duplicates in account, which should not.

# FILES
 * Transactions: [individual accounts, database]
 * JSON:  [tag definitions, groups, transaction tags]


# BUDGET
Expense tracking, classification and report automation.

# TODO
- [x] Pass nonessential to 'buy' cat.
- [x] Change cats with rules.
- [x] Set daily usage functions.
- [ ] Add barplot functions, stacked and not.
- [ ] Study color, load globally?

## REPORTING
- [ ] Expense breakdown. For any month or all. Pie chart.
- [ ] Time series, for any cat/group, evolution. Barplot.
    * Between 2 specific dates (months).
    * Add barplot for any cat.
    * Barplot accepts 2 or more inputs.

# IDEAS
* Functions:
    * Basic: data selection, plotting.
    * Abastract: select, print & plotting (needs 2 datetimes as input).
* Plots, make few good plotting functions:
    * Breakdown of group (expenses):
        * Pie chart with separation (one instance)
    * Evolution:
        * Barplot of single data. Input: series.
        * Stacked barplot (various). Input: df
        * Stacked barplot with percentages (various instances), same as previous
          but normalized.

# IMPROVEMENTS
* Database.add_account() -> only check account VS Database, it will detect 2 
  duplicates in account, which should not.

# FILES
 * Transactions: [individual accounts, database]
 * JSON:  [tag definitions, groups, transaction tags]


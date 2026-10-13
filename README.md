# BrightHome Retail — Sales Analytics Dashboard

A portfolio project using **Power BI, Power Query, and DAX** to explore sales, profit, product performance, regional results, customer segments, and shipping metrics for a fictional home-goods retailer.

![BrightHome dashboard overview](screenshots/dashboard/dashboard-overview.png)

## Project at a glance

- **Business scenario:** Fictional multi-region home-goods retailer
- **Dataset size:** 2,500 sales records
- **Model:** Sales, Products, Customers, and Stores tables
- **Tools:** Power BI Desktop, Power Query, DAX, Excel
- **Period:** The project notes include annual summaries for 2023–2025; confirm the workbook/report filters for the exact date range before comparing periods.

## Key reported results

The figures below are the existing project's documented results and are retained from the original business-question notes. Reconcile them against the current PBIX and source workbook before presenting them as independently audited.

| KPI / question | Documented result |
|---|---:|
| Total sales revenue | $1,067,061.93 |
| Total profit | $198,747.08 |
| Overall profit margin | 18.63% |
| Number of orders | 2,500 |
| Average order value | $426.82 |
| Unique customers | 855 |
| Average discount rate | 6.54% |
| Average shipping cost | $30.59 |

## Main insights documented

- **Regions:** South is documented as the highest-sales region; Midwest is documented as the lowest-sales region. West is documented as the most profitable.
- **Categories:** Furniture is documented as the highest-sales and most-profitable category; Decor is documented as the lowest-sales category.
- **Product:** Office Chair is documented as the top product by sales; Sofa is documented as the most profitable product.
- **Customer segment:** Consumer is documented as the largest sales contributor.
- **Shipping:** Standard Class is documented as the most-used shipping mode.

See the [50 business questions and answers](docs/50-business-questions-answers.md) for the full existing result set.

## Dashboard and project files

- [Power BI report](powerbi/BrightHome_Sales_Analytics.pbix)
- [Dataset workbook](data/source/BrightHome_Dataset.xlsx)
- [Dashboard overview screenshot](screenshots/dashboard/dashboard-overview.png)
- [Additional dashboard screenshots](screenshots/dashboard/)
- [Data-model/source-table screenshots](screenshots/data-model/)
- [Data-preparation screenshots](screenshots/data-preparation/)
- [Metric and insight screenshots](screenshots/metrics/)
- [50 business questions and answers — Markdown](docs/50-business-questions-answers.md)
- [50 business questions and answers — PDF](docs/reference/50-business-questions-answers.pdf)
- [Folder structure guide](docs/project-structure.md)

## Suggested exploration path

1. Open the PBIX report in Power BI Desktop.
2. Review the model relationships and confirm the intended table grain.
3. Check Power Query transformations and the derived revenue fields.
4. Review the DAX measures for revenue, profit, and margin.
5. Use dashboard filters to compare region, category, product, customer segment, and shipping mode.
6. Reconcile the headline results in the business-question notes against the current report.

## Recommended next improvements

1. Add a concise measure dictionary with formulas and definitions for sales, profit, profit margin, average order value, and shipping cost.
2. Make sure all monetary metrics use the same currency and that the currency is explicit in the report.
3. Add data-quality checks for keys, duplicate rows, missing values, and relationships between Sales, Products, Customers, and Stores.
4. Turn the strongest findings into recommendations with the supporting KPI, caveats, and a way to measure impact.

## Notes and limitations

- BrightHome is described as a fictional retailer; this should be presented as a simulated portfolio case, not real company performance.
- Financial figures are carried over from the existing project notes. This organization pass preserves the workbook and PBIX rather than recalculating their measures.
- If screenshots and report totals disagree, treat the PBIX and documented measure definitions as the source for reconciliation before publishing conclusions.

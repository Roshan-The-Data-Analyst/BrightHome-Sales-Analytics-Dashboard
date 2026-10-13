# BrightHome Dataset Audit and Metric Reconciliation

## Executive conclusion

The source file `data/source/BrightHome_Dataset.xlsx`, worksheet `brighthome_dataset`, was checked directly. It contains **2,500 transaction records and 15 columns**, covering **2023-01-01 to 2025-12-31**. All 50 documented business-question answers reconcile numerically to the source when interpreted using the definitions below; no headline arithmetic mismatch was found.

The main issue is definition rather than arithmetic: `Sales` equals `Quantity × UnitPrice` for every row and does not deduct the separate discount percentage. Recorded Sales is therefore not demonstrably net revenue after discounts. Existing margin answers use recorded Sales as their denominator.

## Data-quality checks

| Check | Result |
|---|---:|
| Data records | 2,500 |
| Columns | 15 |
| Distinct OrderID values | 2,500 |
| Duplicate OrderID occurrences | 0 |
| Exact duplicate rows | 0 |
| Missing cells | 0 |
| Invalid dates | 0 |
| Distinct customers | 855 |
| Regions | 4 |
| Cities | 14 |
| Categories | 5 |
| Products | 20 |
| Shipping modes | 4 |
| Sales formula check | 2,500 / 2,500 match `Quantity × UnitPrice` at 2 decimals |

The workbook fields are `OrderID`, `OrderDate`, `Region`, `City`, `Category`, `Product`, `Quantity`, `UnitPrice`, `Discount`, `Sales`, `Profit`, `CustomerSegment`, `ShipMode`, `CustomerID`, and `ShippingCost`.

Observed Discount rates are 0% (1,003 orders), 5% (472), 10% (508), 15% (288), and 20% (229). A total of 1,497 orders have a non-zero discount.

## Reconciled headline totals

| Metric | Recomputed from workbook | Documented value | Result |
|---|---:|---:|---|
| Recorded Sales | $1,067,061.93 | $1,067,061.93 | Match |
| Profit | $198,747.08 | $198,747.08 | Match |
| ShippingCost | $76,477.65 | $76,477.65 | Match |
| Profit / recorded Sales | 18.63% | 18.63% | Match, denominator caveat |
| Profit less ShippingCost | $122,269.43 | Derived from source values | Match, assuming Profit excludes shipping |
| (Profit − ShippingCost) / recorded Sales | 11.46% | 11.46% | Match, use precise label |
| Order count | 2,500 | 2,500 | Match |
| Average order value | $426.82 | $426.82 | Match |
| Unique customers | 855 | 855 | Match |
| Average Profit per order | $79.50 | $79.50 | Match |
| Mean Discount percentage | 6.54% | 6.54% | Match |
| Share of orders with discount | 59.88% | 59.88% | Match |
| Average shipping cost | $30.59 | $30.59 | Match |
| Sales / shipping cost | 13.95x | 13.95x | Match |

## Critical definition finding: Sales vs. Discount

Rounded `Quantity × UnitPrice` equals `Sales` in every record. The separate `Discount` field has values from 0% to 20%, but its effect is not reflected in `Sales`.

The unweighted mean Discount rate is **6.54%**. Estimating discount value as `Sales × Discount` gives approximately **$73,494.18** and discount-adjusted Sales of **$993,567.75**; the estimated sales-weighted discount rate is **6.89%**.

These are **exploratory proxies**, not confirmed accounting measures. The file has no explicit `DiscountAmount` or `NetSales` columns, and it does not document whether Profit already accounts for discounts. It also lacks a per-order rounding rule for the discount.

### How to present margins

- Existing ratio: `SUM(Profit) / SUM(Sales) = 18.63%`.
- Existing post-shipping ratio: `(SUM(Profit) - SUM(ShippingCost)) / SUM(Sales) = 11.46%`, assuming Profit excludes ShippingCost.
- Do not relabel these as net profit margins until discount treatment and the Profit definition are confirmed.
- Do not replace the denominator with estimated discount-adjusted Sales while leaving Profit unchanged; the numerator and denominator might then use inconsistent bases.

## Regional performance

| Region | Orders | Recorded Sales | Profit | Shipping costs | Profit less shipping* | Profit / Sales |
|---|---:|---:|---:|---:|---:|---:|
| South | 625 | $274,292.29 | $50,531.96 | $18,872.44 | $31,659.52 | 18.42% |
| Northeast | 653 | $270,042.41 | $47,954.66 | $20,013.58 | $27,941.08 | 17.76% |
| West | 589 | $264,349.20 | $51,438.77 | $17,654.52 | $33,784.25 | 19.46% |
| Midwest | 633 | $258,378.03 | $48,821.69 | $19,937.11 | $28,884.58 | 18.90% |

*Profit less shipping assumes the source Profit field does not already include ShippingCost.

South has the highest recorded Sales, while West has the highest total Profit, highest average Sales per order ($448.81), and highest regional Profit/Sales ratio (19.46%). Revenue and profitability should be reviewed separately.

## Category performance

| Category | Orders | Recorded Sales | Profit | Shipping costs | Profit less shipping* | Profit / Sales |
|---|---:|---:|---:|---:|---:|---:|
| Furniture | 527 | $403,893.16 | $72,102.74 | $16,342.80 | $55,759.94 | 17.85% |
| Appliances | 462 | $285,193.92 | $54,033.85 | $14,651.89 | $39,381.96 | 18.95% |
| Outdoor | 513 | $225,926.75 | $44,240.19 | $15,385.08 | $28,855.11 | 19.58% |
| Kitchenware | 498 | $86,703.88 | $16,201.50 | $14,866.25 | $1,335.25 | 18.69% |
| Decor | 500 | $65,344.22 | $12,168.80 | $15,231.63 | -$3,062.83 | 18.62% |

Furniture leads in recorded Sales and total Profit. Outdoor has the highest Profit/Sales ratio. Assuming Profit excludes shipping, Decor's shipping costs exceed its Profit and Kitchenware has only $1,335.25 remaining after shipping.

## Annual trend

| Year | Orders | Recorded Sales | Profit | Average order value | Profit / Sales | YoY Sales change |
|---|---:|---:|---:|---:|---:|---:|
| 2023 | 851 | $356,708.02 | $64,475.09 | $419.16 | 18.08% | — |
| 2024 | 822 | $349,858.76 | $65,322.26 | $425.62 | 18.67% | -1.92% |
| 2025 | 827 | $360,495.15 | $68,949.73 | $435.91 | 19.13% | +3.04% |

Sales fell 1.92% in 2024 and rose 3.04% in 2025. Orders fell in 2024 and partly recovered in 2025 while average order value rose each year. This is descriptive, not causal.

## Discount and shipping observations

- Pearson correlation between Discount and Profit is **-0.032**, a very weak negative linear association. It does not show that discounts cause profit to fall or have no effect; product mix and other confounders may matter.
- Standard Class is the most-used ship mode (1,391 orders) and records $587,562.39 in Sales.
- Second Class has the highest average ShippingCost ($31.48).
- Consumer contributes $588,967.43, or 55.20% of recorded Sales, and has the most Same Day orders (135).
- Average recorded Sales across the 12 quarters from 2023–2025 is $88,921.83. This is a historical mean, not a forecast.

## Recommended actions

1. Define Sales and discount treatment. If net sales are required, document DiscountAmount and NetSales formulas plus a per-order rounding rule.
2. Confirm what Profit includes before treating `Profit - ShippingCost` as a contribution measure.
3. Label 18.63% as Profit / recorded Sales and 11.46% as (Profit − ShippingCost) / recorded Sales until the margin basis is verified.
4. Review categories and products where shipping could absorb much of the recorded Profit.
5. Compare total profit with margin. Furniture leads in total category Profit, while Outdoor has a higher Profit/Sales ratio.
6. Test discount changes against a baseline instead of inferring causality from the near-zero correlation.

## Reproducibility

Run `python scripts/audit_brighthome.py` from the repository root. The standard-library script reads the XLSX package and regenerates the data-quality audit JSON. It does not modify the workbook or PBIX.

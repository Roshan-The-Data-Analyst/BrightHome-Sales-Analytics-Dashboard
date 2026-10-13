# BrightHome Dataset Data Dictionary

Source: `data/source/BrightHome_Dataset.xlsx`, worksheet `brighthome_dataset`. It contains 2,500 records across 15 columns and covers 2023-01-01 to 2025-12-31.

| Field | Meaning | Audit notes |
|---|---|---|
| `OrderID` | Order identifier | 2,500 distinct IDs; one row per order |
| `OrderDate` | Order date | Stored as Excel serial dates; converts to ISO dates in 2023–2025 |
| `Region` | Sales region | South, Northeast, West, Midwest |
| `City` | City | 14 distinct cities |
| `Category` | Product category | Five categories |
| `Product` | Product name | 20 products |
| `Quantity` | Units in the order | Used with UnitPrice to validate Sales |
| `UnitPrice` | Unit price | Currency code is not stored in the source |
| `Discount` | Discount rate as a decimal | Observed rates: 0%, 5%, 10%, 15%, 20% |
| `Sales` | Recorded sales amount | Equals Quantity × UnitPrice at cent precision for all 2,500 rows; does not deduct Discount |
| `Profit` | Profit measure from source | Underlying formula/cost basis is not documented |
| `CustomerSegment` | Customer segment | Consumer, Corporate, Home Office |
| `ShipMode` | Shipping service | Standard Class, Second Class, First Class, Same Day |
| `CustomerID` | Customer identifier | 855 distinct customers |
| `ShippingCost` | Shipping cost per order | Average $30.59 per order in this audit |

## Caveats

- There is no explicit `NetSales` or `DiscountAmount` field.
- The project describes a fictional US retailer and uses dollar formatting, but the workbook stores no currency code.
- The Profit field is supplied; cost metadata sufficient to independently recompute the underlying Profit measure is absent.
- `Profit - ShippingCost` assumes Profit does not already include shipping.
- Discount-adjusted amounts are proxies until discount formulas and rounding are confirmed.

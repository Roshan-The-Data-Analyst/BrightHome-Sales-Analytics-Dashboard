# BrightHome Repository Structure

```text
BrightHome-Sales-Analytics-Dashboard/
├── README.md
├── .gitignore
├── assets/
│   └── dashboard-background.png
├── data/
│   └── source/
│       └── BrightHome_Dataset.xlsx
├── powerbi/
│   └── BrightHome_Sales_Analytics.pbix
├── screenshots/
│   ├── dashboard/
│   ├── data-model/
│   ├── data-preparation/
│   └── metrics/
└── docs/
    ├── 50-business-questions-answers.md
    ├── project-structure.md
    └── reference/
        └── 50-business-questions-answers.pdf
```

## Folder responsibilities

- **assets/** — background and reusable visual assets.
- **data/source/** — source dataset workbook. Keep it separate from the PBIX.
- **powerbi/** — the primary Power BI report.
- **screenshots/dashboard/** — full dashboard screenshots and detailed views.
- **screenshots/data-model/** — source-table/model documentation screenshots.
- **screenshots/data-preparation/** — Power Query and preparation steps.
- **screenshots/metrics/** — KPI, regional, category, revenue, profit, and margin visuals.
- **docs/** — written analysis, business questions, and supporting reference documents.

## Maintenance checklist

- Preserve the original source files and avoid committing temporary exports or duplicate report backups.
- Keep the README screenshot paths synchronized with file locations.
- Reconcile documented results to the current PBIX before describing them as audited.
- Define each DAX KPI and confirm its numerator, denominator, filter context, and currency.
- Check relationship cardinality, key uniqueness, missing values, and data grain whenever the data is replaced.

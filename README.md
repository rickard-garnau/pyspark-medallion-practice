# pyspark-medallion-practice

Practice project for building a medallion pipeline (bronze → silver → gold) in Databricks using PySpark. Dataset: Snitch Fashion Sales (~1000 rows, Indian e-commerce).

---

## Tech Stack

- PySpark
- Databricks (Unity Catalog, Delta Lake)
- SQL (gold layer)

---

## Structure

```
├── eda.ipynb            # Exploratory data analysis
├── transformation.py    # Silver layer — cleaning and standardization
└── gold.py              # Gold layer — discount vs profit analysis
```

---

## Pipeline

**Bronze** — raw CSV ingested to Unity Catalog volume, no modifications.

**Silver** — standardized and cleaned:
- Three mixed date formats unified with `coalesce` + `try_to_timestamp`
- Inconsistent city names corrected (`bengaluru`, `Hyd`, `hyderbad`)
- Negative `Units_Sold` and invalid `Discount_%` values (> 1.0) set to null
- Ambiguous dates flagged with `date_format_uncertain`

**Gold** — one analysis table:
- `discount_profit`: average profit per discount bucket (0–0.25, 0.25–0.50, 0.50–0.75, 0.75–1.0)

---

## Findings worth noting

`Order_ID` is not a unique key — five different orders (different customers, products, cities) share the same ID. Deduplication on `Order_ID` would have silently dropped four legitimate rows.

Date format ambiguity can't be resolved in code alone. Dates matching both `MM-dd-yyyy` and `dd-MM-yyyy` are flagged rather than guessed. In production, this would go back to the source.

`Sales_Amount` is 0.0 on nearly all rows despite valid prices and quantities. Left unresolved — the column appears to be unpopulated upstream, not a transformation problem.

Discount level shows no correlation with profit across any bucket. All four groups average 800–1000. Whether that's real or an artifact of the `Sales_Amount` issue is unclear.

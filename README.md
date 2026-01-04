# Olist E-Commerce Analytics Platform

An end-to-end Data Platform for analyzing Brazilian e-commerce data (Olist). This project implements a local data lakehouse using **DuckDB** as the analytical engine, **dbt** for modular data modeling, and **Streamlit** for business intelligence.



## Architecture Overview

The project follows the **ELT (Extract, Load, Transform)** approach, prioritizing data integrity and warehouse performance:

- **Ingestion (Python/uv):** Automated scripts handle the "Load" phase, moving raw CSV data into a **DuckDB** local instance.
- **Transformation (dbt):** - **Staging Layer:** Handles data type casting (Timestamps), renaming, and basic cleaning.
    - **Marts Layer:** Implements a **Star Schema** with Fact tables (`fct_orders`) and Dimension tables (`dim_products`, `dim_customers`).
- **Data Quality:** Automated dbt tests ensure schema constraints (unique, not_null) and business logic validation.
- **Serving (Streamlit):** A dashboard providing real-time KPI exploration via Plotly visualizations.

## Tech Stack

- **Engine:** [DuckDB](https://duckdb.org/)
- **Transformation:** [dbt-core](https://www.getdbt.com/) + `dbt-duckdb`
- **Visualization:** [Streamlit](https://streamlit.io/) and [Plotly](https://plotly.com/python/)
- **Environment Management:** [uv](https://github.com/astral-sh/uv) (Fast Python package installer)

## Project Structure

```text
├── dashboard/          
├── dashboard.py        # Streamlit BI application
├── data/               # DuckDB instance and raw source files (gitignored)
├── dbt_project/        # dbt models, schemas, and tests
├── reports/  
├── scripts/            # Python scripts for ingestion and DB inspection
└── inspect_db.py
└── README.md
```

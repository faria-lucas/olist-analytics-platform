import duckdb
import pandas as pd

def setup_database():
    # Connects to the database file (will be created if it doesn't exist)
    con = duckdb.connect('data/olist.duckdb')

    tables = {
        'raw_orders': 'data/olist_orders_dataset.csv',
        'raw_order_items': 'data/olist_order_items_dataset.csv',
        'raw_products': 'data/olist_products_dataset.csv',
        'raw_customers': 'data/olist_customers_dataset.csv'
    }

    for table_name, file_path in tables.items():
        print(f"Ingesting {table_name}...")
        df = pd.read_csv(file_path)
        con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df")

    print("Tables:", con.execute("SHOW TABLES").fetchall())
    con.close()
if __name__ == "__main__":
    setup_database()
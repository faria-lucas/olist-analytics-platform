import duckdb

def setup_database():
    # Connects to the database file (will be created if it doesn't exist)
    con = duckdb.connect('data/olist.duckdb')
    
    # Example of ultra-fast ingestion of an Olist CSV
    # DuckDB automatically detects types
    con.execute("""
        CREATE TABLE IF NOT EXISTS raw_orders AS 
        SELECT * FROM read_csv_auto('data/olist_orders_dataset.csv');
    """)
    
    print("The raw_orders table was successfully created in DuckDB!")
    con.close()

if __name__ == "__main__":
    setup_database()
import duckdb
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

def get_connection():
    return duckdb.connect('data/olist.duckdb', read_only=True)

def list_tables(con):
    tables = con.execute("SHOW TABLES").fetchall()
    table = Table(title="Tables Available in DuckDB", header_style="bold magenta")
    table.add_column("Index", justify="center", style="cyan")
    table.add_column("Table Name", style="green")
    
    for idx, t in enumerate(tables, 1):
        table.add_row(str(idx), t[0])
    
    console.print(table)
    return [t[0] for t in tables]

def preview_table(con, table_name):
    console.print(f"\n[bold yellow] Viewing Top 5 lines of:[/bold yellow] [bold green]{table_name}[/bold green]")
    
    # Loading the data into a DataFrame for nice formatting
    df = con.execute(f"SELECT * FROM {table_name} LIMIT 5").df()
    
    # Creating a dynamically rich table based on the columns of the Financial Statement
    rich_table = Table(show_header=True, header_style="bold white", border_style="dim")
    for col in df.columns:
        rich_table.add_column(col)
    
    for _, row in df.iterrows():
        rich_table.add_row(*[str(val) for val in row.values])
    
    console.print(rich_table)
    
    # Shows total line count
    total = con.execute(f"SELECT count(*) FROM {table_name}").fetchone()[0]
    console.print(f"\n[dim] Total number of records in the table: {total}[/dim]\n")

def main():
    con = get_connection()
    while True:
        table_names = list_tables(con)
        choice = Prompt.ask(
            "Enter the [bold cyan]number[/bold cyan] from the table to see the preview or [bold red]'q'[/bold red] to leave"
        )

        if choice.lower() == 'q':
            break
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(table_names):
                preview_table(con, table_names[idx])
                Prompt.ask("\nPress [bold]Enter[/bold] to return to the menu...")
            else:
                console.print("[red] Invalid index![/red]")
        except ValueError:
            console.print("[red] Please enter a number or 'q'.[/red]")

if __name__ == "__main__":
    main()
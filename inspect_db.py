import duckdb
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

def get_connection():
    return duckdb.connect('data/olist.duckdb', read_only=True)

def list_tables(con):
    tables = con.execute("SHOW TABLES").fetchall()
    table = Table(title="Tabelas Disponíveis no DuckDB", header_style="bold magenta")
    table.add_column("Índice", justify="center", style="cyan")
    table.add_column("Nome da Tabela", style="green")
    
    for idx, t in enumerate(tables, 1):
        table.add_row(str(idx), t[0])
    
    console.print(table)
    return [t[0] for t in tables]

def preview_table(con, table_name):
    console.print(f"\n[bold yellow] Visualizando Top 5 linhas de:[/bold yellow] [bold green]{table_name}[/bold green]")
    
    # Carregando os dados em um DataFrame para formatar bonito
    df = con.execute(f"SELECT * FROM {table_name} LIMIT 5").df()
    
    # Criando a tabela Rich dinamicamente baseada nas colunas do DF
    rich_table = Table(show_header=True, header_style="bold white", border_style="dim")
    for col in df.columns:
        rich_table.add_column(col)
    
    for _, row in df.iterrows():
        rich_table.add_row(*[str(val) for val in row.values])
    
    console.print(rich_table)
    
    # Mostra contagem total de linhas
    total = con.execute(f"SELECT count(*) FROM {table_name}").fetchone()[0]
    console.print(f"\n[dim]Total de registros na tabela: {total}[/dim]\n")

def main():
    con = get_connection()
    while True:
        table_names = list_tables(con)
        choice = Prompt.ask(
            "Digite o [bold cyan]número[/bold cyan] da tabela para ver o preview ou [bold red]'q'[/bold red] para sair"
        )

        if choice.lower() == 'q':
            break
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(table_names):
                preview_table(con, table_names[idx])
                Prompt.ask("\nPressione [bold]Enter[/bold] para voltar ao menu...")
            else:
                console.print("[red] Índice inválido![/red]")
        except ValueError:
            console.print("[red] Por favor, digite um número ou 'q'.[/red]")

if __name__ == "__main__":
    main()
import click
from etl_process.transform_get_sessions_with_more_than_three_clicks import (
    run_transform_sessions_with_more_than_three_clicks,
)


@click.command(
    help="Script de ETL para transformar e salvar em parquet - Transformação Nível 1."
)
@click.option(
    "--from-csv",
    "-f",
    help="Caminho para o arquivo de entrada csv (RAW).",
    required=True,
)
@click.option(
    "--to-parquet", "-f", help="Caminho para o arquivo de saída parquet.", required=True
)
def transform(from_csv: str, to_parquet: str):
    print(f"Transforming {from_csv} to {to_parquet}...")


@click.command(
    help="Script de ETL para transformar e salvar em parquet - Transformação Nível 2. Requer o parquet gerado pela transformação nível 1 (large file)."
)
@click.option(
    "--from-parquet-folder",
    "-f",
    help="Caminho para a pasta de entrada parquet.",
    required=True,
)
@click.option(
    "--to-parquet-file",
    "-f",
    help="Caminho para o arquivo de saída parquet.",
    required=True,
)
def filter_train_sessions(from_parquet_folder: str, to_parquet_file: str):
    run_transform_sessions_with_more_than_three_clicks(
        from_parquet_folder, to_parquet_file
    )


@click.group(help="CLI que executa scripts de ETL.")
def cli():
    """
    CLI que executa scripts de ETL.
    """


if __name__ == "__main__":
    cli.add_command(transform)
    cli.add_command(filter_train_sessions)
    cli()

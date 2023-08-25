import pandas as pd
import polars as pl
from os.path import join


def etl_script():
    """
    Função que realiza a extração, transformação e carga dos dados.
    :return: None
    """
    print("Loading data...")
    otto_train_df = pl.read_ndjson("./data/OTTO/otto-recsys-train.jsonl")
    folder = "./data/transformed"

    print("Writing data...")
    full_path = join(folder, "otto-transformed-train.parquet")
    otto_train_df.write_parquet(
        full_path,
        use_pyarrow=True,
    )

    print("Done!")


if __name__ == "__main__":
    etl_script()

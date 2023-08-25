import pandas as pd
from etl.otto_dataset_etl import OttoDatasetEtl
from os.path import join


def etl_script():
    """
    Função que realiza a extração, transformação e carga dos dados.
    :return: None
    """
    otto_test_df = pd.read_json("./data/OTTO/otto-recsys-train.jsonl", lines=True)
    otto_dataset_etl = OttoDatasetEtl(otto_test_df)
    otto_dataset_etl.transform(drop_original_events=True)
    folder = "./data/transformed"
    complet_name = join(folder, "otto-transformed-train.parquet")
    otto_dataset_etl.dataset.to_parquet(path=complet_name)


if __name__ == "__main__":
    etl_script()

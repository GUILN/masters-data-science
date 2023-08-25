import pandas as pd
from etl.otto_dataset_etl import OttoDatasetEtl
from os.path import join


def etl_script(
    from_file: str = "./data/OTTO/otto-recsys-train.parquet",
    to_folder: str = "./data/transformed/train",
    name: str = "otto-transformed-train",
    chunks: int = 50,
):
    """
    Função que realiza a extração, transformação e carga dos dados.
    :return: None
    """
    print(f"Reading file {from_file}...")
    original_df = pd.read_parquet(from_file)
    total_rows = original_df.shape[0]
    
    for i in range(chunks):
        print(f"Processing chunk {i}...")
        start = i * (total_rows // chunks)
        end = (i + 1) * (total_rows // chunks)
        if i == chunks - 1:
            end = total_rows
        otto_dataset_etl = OttoDatasetEtl(original_df.iloc[start:end].copy())
        print(f"Transforming chunk {i}...")
        otto_dataset_etl.transform(drop_original_events=True)
        complet_name = join(to_folder, f"{name}-{i}.parquet")
        print(f"Recording chunk {i}...")
        otto_dataset_etl.dataset.to_parquet(path=complet_name)
        print(f"Finished to process chunk {i}!")
    print("Finished to process all chunks!")


if __name__ == "__main__":
    etl_script()
 
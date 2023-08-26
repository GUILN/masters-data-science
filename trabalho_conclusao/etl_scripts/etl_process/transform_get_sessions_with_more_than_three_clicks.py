import os
import polars as pl
import tqdm


def run_transform_sessions_with_more_than_three_clicks(
    from_parquet_folder: str, to_parquet_file: str
):
    """
    Transformação Nível 2. Requer o parquet gerado pela transformação nível 1 (large file).
    """
    print(f"Transforming {from_parquet_folder} to {to_parquet_file}...")
    # read all parquet files from folder
    print("Reading parquet files...")

    # read all parquet file names from folder
    parquet_files = []
    print("Getting parquet file names...")
    for file in tqdm.tqdm(os.listdir(from_parquet_folder)):
        if file.endswith(".parquet"):
            parquet_files.append(file)
    # read all parquet files from folder
    transformed_df = pl.DataFrame()
    print("Reading parquet files...")
    for file in tqdm.tqdm(parquet_files):
        # print(f"Reading {file}...")
        transformed_df = transformed_df.vstack(
            pl.read_parquet(os.path.join(from_parquet_folder, file))
        )

    print("Transforming...")
    # create new columns with count of items clicked, carted and ordered
    transformed_df = transformed_df.with_columns(
        items_clicked_count=transformed_df["items_clicked"].apply(lambda s: len(s)),
        items_carted_count=transformed_df["items_carted"].apply(lambda s: len(s)),
        items_ordered_count=transformed_df["items_ordered"].apply(lambda s: len(s)),
    )

    # filter sessions with more than three clicks
    print("Filtering sessions with more than three clicks...")
    transformed_df = transformed_df.filter(pl.col("items_clicked_count") >= 3)
    # save to parquet
    print("Saving to parquet...")
    transformed_df.write_parquet(
        to_parquet_file,
        use_pyarrow=True,
    )
    print(f"Done! Saved to {to_parquet_file}.")

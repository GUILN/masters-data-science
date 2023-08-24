import pandas as pd


class OttoDatasetEtl:
    def __init__(
        self,
        original_dataset: pd.DataFrame,
    ):
        self._original_dataset = original_dataset
        
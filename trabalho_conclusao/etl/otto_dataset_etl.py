from operator import itemgetter
import pandas as pd

"""
Transform Functions - this transform funcions
are defined to be used with DataFrame.apply
"""


def sort_events(row: pd.Series) -> str:
    """
    Sort events by timestamp
    """
    # sequence = [event for event in row.events]
    # return sorted(sequence, key=itemgetter("ts"))
    return sorted(row.events, key=itemgetter("ts"))


def create_list_of_events(row: pd.Series):
    row["items_clicked"] = []
    row["items_carted"] = []
    row["items_ordered"] = []

    for event in row.sorted_events:
        event_type = event["type"]
        if event_type == "clicks":
            row["items_clicked"].append(event["aid"])
        elif event_type == "carts":
            row["items_carted"].append(event["aid"])
        elif event_type == "orders":
            row["items_ordered"].append(event["aid"])

    return row


class OttoDatasetEtl:
    """
    Otto Dataset ETL

    This class is responsible for transforming the original dataset into a
    dataset that can be used by the models.
    """

    def __init__(
        self,
        original_dataset: pd.DataFrame,
    ):
        self._original_dataset = original_dataset

    def transform(self, drop_original_events: bool = True) -> None:
        """
        Transform the original dataset into a dataset that can be used by the
        models.

        Parameters:
        -----------
        drop_original_events: bool
            If True, the original events will be dropped from the dataset.
            Default: True


        The transformations being applied are:
        -------------------------------------
        * Sort events by timestamp
        * Create one column for each event type
        """
        self._sort()
        self._create_list_of_events()
        if drop_original_events:
            self._original_dataset.pop("events")

    def _sort(self) -> None:
        self._original_dataset["sorted_events"] = self._original_dataset.apply(
            sort_events, axis="columns"
        )

    def _create_list_of_events(self) -> None:
        """
        Creates one column for each event type. Event types:

        * clicks
        * carts
        * orders
        """
        self._original_dataset = self._original_dataset.apply(
            create_list_of_events, axis="columns"
        )

    @property
    def dataset(self) -> pd.DataFrame:
        return self._original_dataset

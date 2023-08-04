
import pandas as pd

def stop_outcome_level(row):
    """
    stop_outcome_level - creates a feature that qantifies the gravity level of the
    stop outcome. The higher the level means worse outcome.
    Will follow the rule:
    5. Arrest Driver
    4. Arrest Passenger
    3. Citation
    2. Warning
    1. N/D | No Action | any other
    """
    stop_outcome_level = 1
    if row.stop_outcome == "Arrest Driver":
        stop_outcome_level = 5
    elif row.stop_outcome == "Arrest Passenger":
        stop_outcome_level = 4
    elif row.stop_outcome == "Citation":
        stop_outcome_level = 3
    elif row.stop_outcome == "Warning":
        stop_outcome_level = 2

    return stop_outcome_level


def violation_level(row):
    """
    violation_level - creates a feature that quantifies the gravity level of the
    violation commited. The higher the level means worse violation.
    Will follow the rule:
    5. Speeding
    4. Moving Violation
    3. Seat Belt
    2. Registration/plates
    1. any other
    """
    violation_level = 1
    if row.violation == "Speeding":
        violation_level = 5
    elif row.violation == "Moving Violation":
        violation_level = 4
    elif row.violation == "Seat Belt":
        violation_level = 3
    elif row.violation == "Registration/plates":
        violation_level = 2

    return violation_level


def stop_time_discretization(row):
    """
    stop_time_discretization - quantifies hour
    """
    hour_min = row.stop_time.split(":")
    stop_time_discrete = int(hour_min[0] + hour_min[1])
    return stop_time_discrete

class PoliceDatasetEtl():
    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset
        self._all_search_types = None
        self._clean_transformed_dataset = None
        self._search_types_dataset = None
    
   
    @property 
    def baseline_features(self) -> list:
        """
        Returns baseline features
        """
        return [
            "is_arrested",
            "driver_race",
            "driver_gender",
            "stop_outcome_level",
            "violation_level",
            "search_conducted",
            "search_type",
            "drugs_related_stop",
            "stop_time_discrete_bins",
            "driver_age_bins",
        ]
        
    @property
    def all_search_types(self) -> list[str]:
        """
        Returns all search types contained in the column search_type
        """
        if self._all_search_types is not None:
            return self._all_search_types
        
        all_search_types = (
            self.clean_transform().search_type.dropna().apply(lambda x: x.split(",")).explode().unique().tolist()
        )
        all_search_types.remove("none")
        self._all_search_types = all_search_types
        return self._all_search_types.copy()
    
    @property
    def all_search_types_columns(self) -> list[str]:
        return [st.replace(" ", "_").lower() for st in self.all_search_types]
        
    def clean_transform(self) -> pd.DataFrame:
        """
        Clean and transform the dataset - Clean nulls and create new features
        """
        if self._clean_transformed_dataset is not None:
            return self._clean_transformed_dataset
        cleaned_df = self.dataset.copy()

        cleaned_df["driver_age"] = cleaned_df.driver_age.fillna(0.0)
        cleaned_df["is_arrested"] = cleaned_df.is_arrested.fillna(False) 
        cleaned_df["search_type"] = cleaned_df.search_type.fillna("none") 
        
        featured_df = cleaned_df.copy()
        featured_df["stop_outcome_level"] = featured_df.apply(
            stop_outcome_level, axis="columns"
        )
        featured_df["violation_level"] = featured_df.apply(violation_level, axis="columns")
        """
        proportinal_stop_outcome: measures the proportion of the outcome level with the violation level
        pso = 1: equaly proportional
        pso > 1: disproportionally greater
        pso < 1: disproportionally lower
        """
        featured_df["proportional_stop_outcome"] = (
            featured_df["stop_outcome_level"] / featured_df["violation_level"]
        )
        featured_df["stop_time_discrete"] = featured_df.apply(
            stop_time_discretization, axis="columns"
        )
        """
        is_black_or_hispanic - agrupamento de grupos que históricamente sofrem mais com abordagens policiais
        """
        featured_df["is_black_or_hispanic"] = featured_df.apply(
            lambda row: row.driver_race == "Black" or row.driver_race == "Hispanic",
            axis="columns",
        )

        featured_df["stop_time_discrete_bins"] = pd.cut(
            featured_df["stop_time_discrete"], 4, labels=["dawn", "morning", "evening", "night"]
        )
        """
        driver_age_bins - discretiza o 'driver age' em 4 bins:
        """
        featured_df["driver_age_bins"] = pd.cut(
            featured_df["driver_age"], 4, labels=["jovem", "adulto", "meia_idade", "idoso"]
        )

        """
        counter - column to make counting operations easier
        """
        featured_df["counter"] = 1
       
        self._clean_transformed_dataset = featured_df 
        return self._clean_transformed_dataset.copy()
   
    def get_search_type_df(self) -> pd.DataFrame:
        """ 
        Returns the columns of search_type in a one-hot-encoder style
        """ 
        if self._search_types_dataset is not None:
            return self._search_types_dataset
        
        search_type_df = pd.DataFrame()
        for s_type in self.all_search_types:
            col_name = s_type.replace(" ", "_").lower()
            search_type_df[col_name] = self.clean_transform().search_type.str.contains(s_type).astype(
                int
            )
        self._search_types_dataset = search_type_df
        return self._search_types_dataset.copy()
    
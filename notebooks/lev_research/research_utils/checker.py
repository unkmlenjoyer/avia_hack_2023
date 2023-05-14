import numpy as np
import pandas as pd


class DataChecker:
    """Data values checker"""

    def get_null_values(self, X: pd.DataFrame) -> None:
        """Method to check null values in data

        Parameters
        ----------
        X : pd.DataFrame
            Entry dataset to visualize

        Returns
        -------
        null_values : pd.DataFrame
            Dataset with counter of null rows
        """

        init_shape = X.shape[0]
        null_values = X.isnull().sum().to_frame().reset_index()
        null_values.columns = ["feature_name", "count_null"]
        null_values["percentage"] = np.round(
            100 * null_values["count_null"] / init_shape, 2
        )
        return null_values

    def get_unique_values(self, X: pd.DataFrame) -> None:
        """Method calculate unique values
        in each column of DataFrame

        Parameters
        ----------
        X : pd.DataFrame
            Entry dataset to visualize

        Returns
        -------
        n_uniques : pd.DataFrame
            Dataset with counter of unique values
        """

        n_uniques = X.nunique().to_frame().reset_index()
        n_uniques.columns = ["feature_name", "count_unique"]
        return n_uniques

    def check_duplicates(self, X: pd.DataFrame) -> None:
        """Method calculate unique values
        in each column of DataFrame

        Parameters
        ----------
        X : pd.DataFrame
            Entry dataset to visualize

        Returns
        -------
        None
        """
        init_shape = X.shape[0]
        dupl = X.duplicated().sum()
        percentage = np.round(100 * dupl / init_shape, 2)
        print(f"There are {dupl} row(s). It's {percentage} % from all dataset")

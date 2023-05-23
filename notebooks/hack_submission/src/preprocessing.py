from typing import Dict, List, Union

import numpy as np
import pandas as pd
from airportsdata import Airport
from sklearn.base import BaseEstimator, TransformerMixin

from .utils import convert_time_zones, extract_airports, get_airport_info


class RequestTransformer(BaseEstimator, TransformerMixin):
    """Custom data preprocessor for flight-requests data"""

    def __init__(
        self,
        airport_data: Dict[str, Union[Airport, Dict[str, Dict[str, str]]]],
    ) -> None:
        self.airport_data = airport_data

    def fit(self, X=None, y=None):
        return self

    def transform(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
        X_ = X.copy()

        X_["RequestID"] = X_["RequestID"].astype(str)
        X_["RequestDate"] = pd.to_datetime(X_["RequestDate"])
        X_["RequestDepartureDate"] = pd.to_datetime(X_["RequestDepartureDate"])
        X_["RequestReturnDate"] = pd.to_datetime(X_["RequestReturnDate"])
        X_["DepartureDate"] = pd.to_datetime(X_["DepartureDate"])
        X_["ArrivalDate"] = pd.to_datetime(X_["ArrivalDate"])
        X_["ReturnDepatrureDate"] = pd.to_datetime(X_["ReturnDepatrureDate"])
        X_["ReturnArrivalDate"] = pd.to_datetime(X_["ReturnArrivalDate"])

        X_["IsBaggage"] = X_["IsBaggage"].fillna(0)
        X_["isRefundPermitted"] = X_["isRefundPermitted"].fillna(0)
        X_["isExchangePermitted"] = X_["isExchangePermitted"].fillna(0)

        X_["IsBaggage"] = X_["IsBaggage"].astype(int)
        X_["isRefundPermitted"] = X_["isRefundPermitted"].astype(int)
        X_["isExchangePermitted"] = X_["isExchangePermitted"].astype(int)

        air_names_df = pd.DataFrame(
            list(X_.SearchRoute.apply(lambda x: extract_airports(x)).values),
            columns=["dep_forw", "arr_forw", "dep_back", "arr_back"],
        )

        air_names_df["dep_forw_tz"] = air_names_df["dep_forw"].apply(
            lambda x: get_airport_info(x, self.airport_data)[0]
        )

        air_names_df["dep_forw_country"] = air_names_df["dep_forw"].apply(
            lambda x: get_airport_info(x, self.airport_data)[1]
        )

        air_names_df["arr_forw_tz"] = air_names_df["arr_forw"].apply(
            lambda x: get_airport_info(x, self.airport_data)[0]
        )

        air_names_df["arr_forw_country"] = air_names_df["arr_forw"].apply(
            lambda x: get_airport_info(x, self.airport_data)[1]
        )

        air_names_df["dep_back_tz"] = air_names_df["dep_back"].apply(
            lambda x: get_airport_info(x, self.airport_data)[0]
        )

        air_names_df["dep_back_country"] = air_names_df["dep_back"].apply(
            lambda x: get_airport_info(x, self.airport_data)[1]
        )

        air_names_df["arr_back_tz"] = air_names_df["arr_back"].apply(
            lambda x: get_airport_info(x, self.airport_data)[0]
        )

        air_names_df["arr_back_country"] = air_names_df["arr_back"].apply(
            lambda x: get_airport_info(x, self.airport_data)[1]
        )

        X_ = pd.concat([X_, air_names_df.set_index(X_.index)], axis=1)

        X_["DepartureDate_conv"] = X_.apply(
            lambda x: convert_time_zones(
                x["DepartureDate"], x["dep_forw_tz"], x["arr_forw_tz"]
            ),
            axis=1,
        )

        X_["ReturnDepatrureDate_conv"] = X_.apply(
            lambda x: convert_time_zones(
                x["ReturnDepatrureDate"], x["dep_back_tz"], x["arr_back_tz"]
            )
            if x["dep_back"] != ""
            else pd.to_datetime(np.nan),
            axis=1,
        )

        X_["forw_hours"] = (
            X_["ArrivalDate"] - X_["DepartureDate_conv"]
        ) / np.timedelta64(1, "h")
        X_["back_hours"] = (
            X_["ReturnArrivalDate"] - X_["ReturnDepatrureDate_conv"]
        ) / np.timedelta64(1, "h")

        X_["total_hours"] = X_["forw_hours"] + X_["back_hours"]

        X_["forw_hours_diff_min"] = X_.groupby(["RequestID"])["forw_hours"].transform(
            lambda x: (x - x.min()) / x
        )

        X_["forw_hours_diff_mean"] = X_.groupby(["RequestID"])["forw_hours"].transform(
            lambda x: (x - x.mean()) / x
        )

        X_["back_hours_diff_min"] = X_.groupby(["RequestID"])["back_hours"].transform(
            lambda x: (x - x.min()) / x
        )

        X_["back_hours_diff_mean"] = X_.groupby(["RequestID"])["back_hours"].transform(
            lambda x: (x - x.mean()) / x
        )

        X_["req_dep_hours_diff"] = (
            X_["DepartureDate"] - X_["RequestDepartureDate"]
        ) / np.timedelta64(1, "h")

        X_["req_ret_hours_diff"] = (
            X_["ReturnDepatrureDate"] - X_["RequestReturnDate"]
        ) / np.timedelta64(1, "h")

        X_["price_diff_min_perc"] = X_.groupby(["RequestID"])["Amount"].transform(
            lambda x: (x - x.min()) / x
        )

        X_["price_diff_mean_perc"] = X_.groupby(["RequestID"])["Amount"].transform(
            lambda x: (x - x.mean()) / x
        )

        X_["TravellerGrade"] = X_["TravellerGrade"].fillna("Unknown")

        X_["is_direct"] = X_[["SegmentCount", "back_hours"]].apply(
            lambda x: 1
            if (
                (x.SegmentCount == 1 and pd.isna(x.back_hours))
                or (x.SegmentCount == 2 and x.back_hours > 0)
            )
            else 0,
            axis=1,
        )

        return X_

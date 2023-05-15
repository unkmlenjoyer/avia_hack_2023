"""
Script for first time look to the inpurt data


1. Import necessary
"""

import airportsdata as airdata

# %%
import numpy as np
import pandas as pd
import seaborn as sns
from research_utils.checker import DataChecker
from research_utils.custom_constants import CustomResearchConstants
from research_utils.data_utils import (
    convert_time_zones,
    extract_airports,
    get_airport_info,
)

"""
2. Set libraries settings
"""
# %%
custom_constants = CustomResearchConstants()

# set pandas options
pd.set_option("display.max_rows", custom_constants.PD_MAX_ROWS)
pd.set_option("display.max_columns", custom_constants.PD_MAX_COLUMNS)
pd.set_option("display.width", custom_constants.PD_WIDTH)
pd.set_option("display.max_colwidth", custom_constants.PD_MAX_COL_WIDTH)

# set seaborn options
sns.set_style(custom_constants.SNS_STYLE)
sns.set({"figure.figsize": custom_constants.SNS_FIG_SIZE})

# %%
extend_airport = pd.read_excel("../../data/raw_data/extended_airport_data.xlsx")
extend_airport.columns = [
    "country",
    "tz",
    "air_port_key",
    "city",
    "country_full",
    "time_zone_utc",
]
extend_airport["air_port_key"] = extend_airport["air_port_key"].apply(
    lambda x: x.split(" ")[-1]
)
extend_airport = extend_airport.set_index("air_port_key")
extended_data = extend_airport[["country", "tz"]].to_dict("index")

# %%
airports = airdata.load("IATA") | extended_data


# %%
"""
3. Data loading from .xlsx files
"""

# %%
df_agent = pd.read_excel("../../data/raw_data/RequestAgent.xlsx", index_col=0)

# %%
# df_client = pd.read_excel("../../data/raw_data/RequestClient.xlsx", index_col=0)

# %%
ag_descr = pd.read_excel("../../data/raw_data/DescriptionAgent.xlsx", index_col=0)
cl_descr = pd.read_excel("../../data/raw_data/DescriptionClient.xlsx", index_col=0)

# %%
with open(file="../../docs/research/data_info/agent_description.txt", mode="w") as f:
    for row in ag_descr[["Столбец", "что это", "описание"]].iterrows():
        f.write(" ---- >> ".join(map(str, row[1].values)))
        f.write("\n")
# %%
with open(file="../../docs/research/data_info/client_description.txt", mode="w") as f:
    for row in cl_descr[["Столбец", "что это", "описание"]].iterrows():
        f.write(" ---- >> ".join(map(str, row[1].values)))
        f.write("\n")

"""
4. EDA

4.1 Data structure, types, na and etc.
"""

# %%
dch = DataChecker()

# %%
df_agent.describe()

# %%
df_agent.info()

# %%
# df_client.describe()

# %%
# df_client.info()

# %%
# There are 1530 row(s). It's 0.24 % from all dataset
dch.check_duplicates(df_agent)
# %%
# There are 873 row(s). It's 0.09 % from all dataset
# dch.check_duplicates(df_client)
# %%
dch.get_unique_values(df_agent)
# %%
# dch.get_unique_values(df_client)
# %%
dch.get_null_values(df_agent)
# %%
# dch.get_null_values(df_client)

# %%
# RequestID                 int64 -> convert to str
# EmployeeId                int64 -> convert to str
# RequestDate              object -> convert to datetime
# ClientID                  int64
# TravellerGrade           object
# SearchRoute              object
# RequestDepartureDate     object -> convert to datetime
# RequestReturnDate        object -> convert to datetime
# FligtOption              object
# DepartureDate            object -> convert to datetime
# ArrivalDate              object -> convert to datetime
# ReturnDepatrureDate      object -> convert to datetime
# ReturnArrivalDate        object -> convert to datetime
# SegmentCount              int64
# Amount                    int64
# class                    object
# IsBaggage               float64 -> convert to int
# isRefundPermitted       float64 -> convert to int
# isExchangePermitted     float64 -> convert to int
# isDiscount                int64
# InTravelPolicy            int64
# SentOption                int64

df_agent.dtypes

# %%
# RequestID                 int64  -> convert to str
# RequestDate              object  -> convert to datetime
# ClientID                  int64  -> convert to str
# ClientGrade              object
# SearchRoute              object
# RequestDepartureDate     object -> convert to datetime
# RequestReturnDate        object -> convert to datetime
# FligtOption              object
# DepartureDate            object -> convert to datetime
# ArrivaDate               object -> convert to datetime
# ReturnDepatrureDate      object -> convert to datetime
# ReturnArrivalDate        object -> convert to datetime
# SegmentCount              int64
# Amount                    int64
# class                    object
# IsBaggage                 int64
# isRefundPermitted       float64 -> convert to int
# isExchangePermitted     float64 -> convert to int
# isDiscount                int64
# InTravelPolicy            int64
# FrequentFlyer            object
# SelectedVariant           int64

# df_client.dtypes
# %%
# df_client.head()
# %%
"""
4.2 Target EDA
"""

# 0    96.076573
# 1    3.923427
df_agent.SentOption.value_counts(normalize=True) * 100

# %%
# 0    99.565622
# 1    0.434378
# df_client.SelectedVariant.value_counts(normalize=True) * 100


# %%
"""
5. Feature Engineering

5.1 Convert incorrect datatype

"""

# %%
df_agent["RequestID"] = df_agent["RequestID"].astype(str)
df_agent["EmployeeId"] = df_agent["EmployeeId"].astype(str)
df_agent["RequestDate"] = pd.to_datetime(df_agent["RequestDate"])
df_agent["RequestDepartureDate"] = pd.to_datetime(df_agent["RequestDepartureDate"])
df_agent["RequestReturnDate"] = pd.to_datetime(df_agent["RequestReturnDate"])
df_agent["DepartureDate"] = pd.to_datetime(df_agent["DepartureDate"])
df_agent["ArrivalDate"] = pd.to_datetime(df_agent["ArrivalDate"])
df_agent["ReturnDepatrureDate"] = pd.to_datetime(df_agent["ReturnDepatrureDate"])
df_agent["ReturnArrivalDate"] = pd.to_datetime(df_agent["ReturnArrivalDate"])

# %%
df_agent["IsBaggage"] = df_agent["IsBaggage"].fillna(0)
df_agent["isRefundPermitted"] = df_agent["isRefundPermitted"].fillna(0)
df_agent["isExchangePermitted"] = df_agent["isExchangePermitted"].fillna(0)


df_agent["IsBaggage"] = df_agent["IsBaggage"].astype(int)
df_agent["isRefundPermitted"] = df_agent["isRefundPermitted"].astype(int)
df_agent["isExchangePermitted"] = df_agent["isExchangePermitted"].astype(int)


"""
5.2 Create features
5.2.1 Airport data: timezone, country, is flight not in Russia
"""

# %%
air_names_df = pd.DataFrame(
    list(df_agent.SearchRoute.apply(lambda x: extract_airports(x)).values),
    columns=["dep_forw", "arr_forw", "dep_back", "arr_back"],
)

# %%
# аэропорты, которых нет в либе, надо найти инфу
# TODO https://github.com/unknowngfonovich/avia_hack_2023/issues/1
for item in np.unique(air_names_df.values.reshape(-1)):
    try:
        airports[item]
    except:
        print("аэропорт", item)

# %%

air_names_df["dep_forw_tz"] = air_names_df["dep_forw"].apply(
    lambda x: get_airport_info(x, airports)[0]
)

air_names_df["dep_forw_country"] = air_names_df["dep_forw"].apply(
    lambda x: get_airport_info(x, airports)[1]
)

air_names_df["arr_forw_tz"] = air_names_df["arr_forw"].apply(
    lambda x: get_airport_info(x, airports)[0]
)

air_names_df["arr_forw_country"] = air_names_df["arr_forw"].apply(
    lambda x: get_airport_info(x, airports)[1]
)

air_names_df["dep_back_tz"] = air_names_df["dep_back"].apply(
    lambda x: get_airport_info(x, airports)[0]
)

air_names_df["dep_back_country"] = air_names_df["dep_back"].apply(
    lambda x: get_airport_info(x, airports)[1]
)

air_names_df["arr_back_tz"] = air_names_df["arr_back"].apply(
    lambda x: get_airport_info(x, airports)[0]
)

air_names_df["arr_back_country"] = air_names_df["arr_back"].apply(
    lambda x: get_airport_info(x, airports)[1]
)

# %%
df_agent = pd.concat([df_agent, air_names_df], axis=1)

"""
5.2.3 Working with datetimes
"""

# %% ФИЛЬТР
df_agent = df_agent[
    ~(
        (df_agent["dep_back_tz"] != "")
        & (df_agent["arr_back_tz"] != "")
        & (df_agent["ReturnDepatrureDate"].isna())
    )
]
df_agent = df_agent[df_agent.Amount > 0]


# %%
df_agent["DepartureDate_conv"] = df_agent.apply(
    lambda x: convert_time_zones(
        x["DepartureDate"], x["dep_forw_tz"], x["arr_forw_tz"]
    ),
    axis=1,
)

# %%
df_agent["ReturnDepatrureDate_conv"] = df_agent.apply(
    lambda x: convert_time_zones(
        x["ReturnDepatrureDate"], x["dep_back_tz"], x["arr_back_tz"]
    )
    if x["dep_back"] != ""
    else pd.to_datetime(np.nan),
    axis=1,
)

# %%
df_agent["forw_hours"] = (
    df_agent["ArrivalDate"] - df_agent["DepartureDate_conv"]
) / np.timedelta64(1, "h")
df_agent["back_hours"] = (
    (df_agent["ReturnArrivalDate"] - df_agent["ReturnDepatrureDate_conv"])
    / np.timedelta64(1, "h")
).fillna(0)


# %%
df_agent.groupby(["RequestID"])["back_hours"].transform(
    lambda x: x.max() - x
).value_counts()

# %%
df_agent.groupby(["RequestID"])["forw_hours"].transform(
    lambda x: x.max() - x
).value_counts()

# %%
"""
5.2.3 Price difference compare to others offers in request
"""
# %%

# %%
df_agent.groupby(["RequestID"])["Amount"].transform(lambda x: x.max() - x)
# %%
df_agent.groupby(["RequestID"])["Amount"].transform(lambda x: x - x.min())

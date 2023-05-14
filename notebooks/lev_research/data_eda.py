"""
Script for first time look to the inpurt data


1. Import necessary
"""

# %%
import numpy as np
import pandas as pd
import seaborn as sns
from research_utils.checker import DataChecker
from research_utils.custom_constants import CustomResearchConstants

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

"""
3. Data loading from .xlsx files
"""

# %%
df_agent = pd.read_excel("../../data/raw_data/RequestAgent.xlsx", index_col=0)

# %%
df_client = pd.read_excel("../../data/raw_data/RequestClient.xlsx", index_col=0)


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
df_client.describe()

# %%
df_client.info()

# %%
# There are 1530 row(s). It's 0.24 % from all dataset
dch.check_duplicates(df_agent)
# %%
# There are 873 row(s). It's 0.09 % from all dataset
dch.check_duplicates(df_client)
# %%
dch.get_unique_values(df_agent)
# %%
dch.get_unique_values(df_client)
# %%
dch.get_null_values(df_agent)
# %%
dch.get_null_values(df_client)

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

df_client.dtypes
# %%
df_client.head()
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
df_client.SelectedVariant.value_counts(normalize=True) * 100

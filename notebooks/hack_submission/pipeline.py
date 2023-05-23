# %%
import airportsdata
import numpy as np
import pandas as pd
from config import ModelConfig
from src.modelbuilder import ModelBuilder
from src.preprocessing import RequestTransformer

configuration = ModelConfig()

air_data = airportsdata.load("IATA") | configuration.extended_air_data
data_transformer = RequestTransformer(air_data)
data_transformer.fit()

model_one_way = ModelBuilder.from_file(configuration.path_model_one_way)
model_two_way = ModelBuilder.from_file(configuration.path_model_two_way)


def inference(data: pd.Series) -> float:
    """Get predictions for data

    Parameters
    ----------
    data : pd.Series
        Row with data for offer

    Returns
    -------
    pred_probas : float
        Probas of `1` class prediction
    """

    pred_probas = (
        model_one_way.predict_proba(data[configuration.cols_model_one_way])
        if pd.isna(data.back_hours)
        else model_two_way.predict_proba(data[configuration.cols_model_two_way])
    )

    return pred_probas[1]


# %%
pd.set_option("display.max_rows", 1000)
pd.set_option("display.max_columns", 50)


# %%
data = pd.read_excel("../../data/raw_data/RequestAgent_ToCheck.xlsx", index_col=0)
# %%
data = data.rename(columns={"ValueRu": "TravellerGrade"})
# %%
data = data[~data.index.duplicated()].drop(columns="Position ( from 1 to n)")
# %%
transformed = data_transformer.transform(data)

# %%
data["probas"] = transformed.apply(lambda x: inference(x), axis=1)
# %%
data["Position ( from 1 to n)"] = (
    data.groupby(["RequestID"])["probas"]
    .rank(method="first", ascending=False)
    .astype(int)
)

# %%
data.drop(columns=["probas"]).to_excel(
    "../../data/processed/submission_fit_predict_team.xlsx"
)

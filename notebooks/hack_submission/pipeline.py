# %%
import airportsdata
import numpy as np
import pandas as pd
from config import ServiceConfig
from src.modelbuilder import ModelBuilder
from src.preprocessing import RequestTransformer

configuration = ServiceConfig()

air_data = airportsdata.load("IATA") | configuration.extended_air_data
data_transformer = RequestTransformer(air_data)
data_transformer.fit()

model_one_way = ModelBuilder.from_file(configuration.path_model_one_way)
model_two_way = ModelBuilder.from_file(configuration.path_model_two_way)


def inference(data: pd.DataFrame) -> np.ndarray:
    """Get predictions for data

    Parameters
    ----------
    data : pd.DataFrame
        Batch of data to predict. Batch contains rows for only one unique RequestID

    Returns
    -------
    pred_probas : np.ndarray
        Probas of `1` class prediction
    """

    pred_probas = (
        model_one_way.predict_proba(data[configuration.cols_model_one_way])
        if data.back_hours.isna().sum() > 0
        else model_two_way.predict_proba(data[configuration.cols_model_two_way])
    )[:, 1]

    return pred_probas


# %%
data = pd.read_excel("../../data/raw_data/RequestAgent_ToCheck.xlsx", index_col=0)
# %%
data = data.rename(columns={"ValueRu": "TravellerGrade"})
# %%
data = data[~data.index.duplicated()].drop(columns="Position ( from 1 to n)")
# %%
transformed = data_transformer.transform(data)
data["probas"] = inference(transformed)
# %%
data["Position ( from 1 to n)"] = (
    data.groupby(["RequestID"])["probas"]
    .rank(method="first", ascending=False)
    .astype(int)
)

data.drop(columns=["probas"]).to_excel(
    "../../data/processed/submission_fit_predict_team.xlsx"
)

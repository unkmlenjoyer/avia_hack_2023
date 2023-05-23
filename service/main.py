import os
from typing import Dict

import airportsdata
import numpy as np
import pandas as pd
import uvicorn
from config import ServiceConfig
from fastapi import FastAPI
from src.modelbuilder import ModelBuilder
from src.preprocessing import RequestTransformer

# configuration env
SERVICE_HOST = os.getenv("SERVICE_HOST")
SERVICE_PORT = int(os.getenv("SERVICE_PORT"))

# model config
configuration = ServiceConfig()
air_data = airportsdata.load("IATA") | configuration.extended_air_data
data_transformer = RequestTransformer(air_data)
data_transformer.fit()

# load models
model_one_way = ModelBuilder.from_file(configuration.path_model_one_way)
model_two_way = ModelBuilder.from_file(configuration.path_model_two_way)


app = FastAPI()


def inference(data: pd.Series) -> float:
    """Get predictions for data

    Parameters
    ----------
    data : pd.Series
        Batch of data to predict. Batch contains rows for only one unique RequestID

    Returns
    -------
    pred_probas : float
        Proba of `1` class prediction
    """

    pred_probas = (
        model_one_way.predict_proba(data[configuration.cols_model_one_way])
        if pd.isna(data.back_hours)
        else model_two_way.predict_proba(data[configuration.cols_model_two_way])
    )

    return pred_probas[1]


@app.get("/")
def say_hello():
    return {"msg": "This is ranking service"}


@app.get("/check_health")
def get_health():
    return {"msg": "Service is online"}


@app.post("/predict_batch")
def get_predict(request: Dict):
    """Predict score for batch of unique query"""

    # reformat dict to batch
    batch = pd.DataFrame().from_dict(request, orient="index")

    # create features for every row in RequestID
    tranformed_batch = data_transformer.transform(batch)

    # get probas for rows
    batch["probas"] = tranformed_batch.apply(lambda x: inference(x), axis=1)

    # create rank by probas
    batch["rank_level"] = (
        batch.groupby(["RequestID"])["probas"]
        .rank(method="first", ascending=False)
        .astype(int)
    )

    batch = batch.fillna(np.nan).replace(np.nan, None)

    return batch.to_dict(orient="index")


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=SERVICE_HOST,
        port=SERVICE_PORT,
    )

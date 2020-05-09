import os
import logging
import joblib

from fastapi import FastAPI
from app.config import Config
from app.model import Iris

logger = logging.getLogger(__name__)

model_file = f"{ Config.MODEL_NAME}.pkl"
model_location = os.path.join(Config.MODEL_FOLDER, model_file)

app = FastAPI()
app.model = joblib.load(model_location)


@app.get("/info")
def info():
    """
    Information endpoint for microservice to give model details and use as a health check
    :return: Information about service
    """
    return {
        "description": Config.DESCRIPTION,
        "version": Config.VERSION,
        "model_name": Config.MODEL_NAME
    }


@app.post("/predict")
def predict(iris: Iris):
    input = [iris.sepal_length, iris.sepal_width, iris.petal_length, iris.petal_width]
    prediction = app.model.predict([input])[0]
    species = {
        0: "setosa",
        1: "versicolor",
        2: "virginica"
    }
    predicted_species = species[prediction]
    logger.info(f"Predicted {predicted_species} for iris with the following properties {iris}")
    return {
        "species": predicted_species
    }

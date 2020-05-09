import logging

from fastapi import FastAPI
from app.config import Config


logger = logging.getLogger(__name__)

app = FastAPI()


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
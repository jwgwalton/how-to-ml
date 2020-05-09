import os


class Config(object):
    DESCRIPTION = "A microservice for predicting the species of iris"
    VERSION = "0.0.0"
    MODEL_FOLDER = os.getenv("MODEL_LOCATION", "/tmp")
    MODEL_NAME = os.getenv("MODEL_NAME", "iris_classification_fdd13277-d1e8-4e26-a88d-b63e9596f766")

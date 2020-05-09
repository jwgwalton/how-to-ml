#!/usr/bin/env python

# This is the code to go from data to model artifact
# Sometimes this will be several files
# a good rule of thumb that it can be split when you write to disk 
# (often that can be a good thing if it's a complicated pipelines which takes signficant time)
import os
import uuid
import joblib

import pandas as pd
import numpy as np

from pycm import ConfusionMatrix

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# Where are we saving the model, it makes sense to be configured from an env variable for easy use in a scheduled process
model_folder = os.getenv("MODEL_FOLDER", "/tmp/") 

# We may need to revert to old models so each new model should have its own id.
model_id = uuid.uuid4()
model_name = f"iris_classification_{model_id}.pkl"

# This is a simple import but this would normally involve talking to a database or importing a csv generated from a data extraction process
iris = load_iris()

df = pd.DataFrame(data= np.c_[iris['data'], iris['target']],
                     columns= iris['feature_names'] + ['target'])

columns = [
    'sepal length (cm)', 
    'sepal width (cm)', 
    'petal length (cm)',
    'petal width (cm)', 
]
X = df[columns].values
y = df["target"].values

print("Generating train/test data")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

scaler = MinMaxScaler()
lr = LogisticRegression(multi_class='auto')

pipeline = Pipeline([
    ("scaler", scaler),
    ("lr", lr),
])
print("Fitting Pipeline")
fitted_pipeline = pipeline.fit(X_train, y_train)

predictions = fitted_pipeline.predict(X_test)

confusion_matrix = ConfusionMatrix(actual_vector=y_test, predict_vector=predictions)
print(confusion_matrix)

# Serializing the model to disk
model_location = os.path.join(model_folder, model_name)
print(f"Serialzing the model to {model_location}")
joblib.dump(fitted_pipeline, model_location, compress = 1)

# The next stage is to transfer the model to a storage location (ftp site/google bucket etc) 
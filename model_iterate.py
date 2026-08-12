from model_train import train
from model_test import test
import numpy as np
import matplotlib.pyplot as plt
import random
import json
from datetime import datetime

metrics = []
runs_per_test = 100
seeds = np.random.randint(1, 10000 + 1, size=runs_per_test)

test_name = "Average error"

test_settings = [{
    "training_number": "max",
    "epochs": 2000,
    "learning_rate": 3e-6,
    "regularization": 1e-2,
    "dropout_probability": 0,
    "hidden_layer_list": [32, 32],
    "PCA": False
},
{
    "training_number": "max",
    "epochs": 2000,
    "learning_rate": 3e-6,
    "regularization": 1e-4,
    "dropout_probability": 0,
    "hidden_layer_list": [32, 32],
    "PCA": False
}]

for test_setting in test_settings:

    total_metric = 0

    for seed in seeds:

        train(seed=seed, **test_setting)
        metric = test(seed=seed, hidden_layer_list=test_setting["hidden_layer_list"], PCA=test_setting["PCA"])

        total_metric += metric

    average_metric = total_metric / runs_per_test

    print(average_metric)
    metrics.append(average_metric)

with open("model_data/" + test_name + datetime.now().strftime(" %Y-%m-%d %H:%M:%S") + ".json", "w") as file:
    json.dump(
        {
            "test_settings": test_settings,
            "metrics": metrics
        },
        file,
        indent=2
    )

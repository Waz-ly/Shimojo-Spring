import numpy as np
import matplotlib.pyplot as plt
import json

file_name = "learning_rate 2026-08-07 20:20:28.json"

data = None
with open("model_data/" + file_name) as file:
    data = json.load(file)

plt.plot(data["test_settings"], data["metrics"])
plt.show()

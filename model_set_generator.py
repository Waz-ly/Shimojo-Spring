import os
import numpy as np

def get_test_set(seed=0, test_set_size=10):

    files = []
    for file in os.listdir("stimuli"):
        if file[0] == ".":
            continue

        files.append(file)

    for file in os.listdir("additional_stimuli"):
        if file[0] == ".":
            continue

        files.append(file)

    rng_engine = np.random.default_rng(seed=seed)
    rng_engine.shuffle(files)

    return files[:test_set_size]
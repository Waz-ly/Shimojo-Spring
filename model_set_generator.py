import os
import numpy as np

def get_test_set(seed=2, test_set_size=10):

    files = []

    for file in os.listdir("stimuli"):
        if file[0] == ".":
            continue

        files.append(os.path.splitext(file)[0])

    stimuli_set_number = 1
    while os.path.exists("stimuli_additional" + str(stimuli_set_number)):

        for file in os.listdir("stimuli_additional" + str(stimuli_set_number)):
            if file[0] == ".":
                continue

            files.append(os.path.splitext(file)[0])

        stimuli_set_number += 1

    rng_engine = np.random.default_rng(seed=seed)
    rng_engine.shuffle(files)

    return files[:test_set_size]
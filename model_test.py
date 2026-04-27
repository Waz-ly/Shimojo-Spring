import os
import torch
import librosa
import numpy as np
import openl3
import matplotlib.pyplot as plt
from sound_main import calculate_MDS
from model_set_generator import get_test_set
from model_train import Mapper

results, labels = calculate_MDS(False)
results = results.tolist()
labels = labels.tolist()
test_set = get_test_set()
test_set_names = [os.path.splitext(file)[0] for file in test_set]

model_size = 0
with open('model/model_info.txt', 'r') as file:
    lines = file.readlines()
    model_size = int(lines[0].split()[2])

model = Mapper(input_dim=model_size)
model.load_state_dict(torch.load("model/mapper.pth"))
model.eval()

for file in test_set:
    if os.path.isfile("stimuli/" + file):
        audio_file = "stimuli/" + file
    elif os.path.isfile("stimuli_additional1/" + file):
        audio_file = "stimuli_additional1/" + file
    else:
        raise FileNotFoundError("file from test set not found")
    
    audio, samplerate = librosa.load(audio_file, duration=5)
    audio = np.pad(audio, (0, 5 * samplerate - len(audio)))
    embedding, timestamp = openl3.get_audio_embedding(audio, samplerate, content_type="music", embedding_size=512)
    embedding = embedding.flatten()

    with torch.no_grad():
        tensor = torch.tensor(embedding, dtype=torch.float32)
        prediction = model(tensor.unsqueeze(0)) 
        results.append(prediction.squeeze().numpy())

    labels.append(file)

fg = plt.figure()
ax = fg.add_subplot()

for result, label in zip(results, labels):

    if label in test_set_names:
        color = "lime"
        set_label = "test set MDS"

    elif label in test_set:
        color = "orangered"
        set_label = "test set eval"

    else:
        color = "turquoise"
        set_label = "MDS"

    plt.scatter(result[0], result[1], color=color, s=100, lw=0, label=set_label)
    plt.annotate(
        label, result,
        textcoords="offset points",
        xytext=(5, 5),
        ha="left",
        fontsize=6,
        color=color
    )

plt.show()
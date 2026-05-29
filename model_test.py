import torch
import numpy as np
import matplotlib.pyplot as plt
from sound_main import calculate_MDS
from model_set_generator import get_test_set
from model_train import Mapper

model_size = 0
with open('model/model_info.txt', 'r') as file:
    lines = file.readlines()
    model_size = int(lines[0].split()[2])

model = Mapper(input_dim=model_size)
model.load_state_dict(torch.load("model/mapper.pth"))
model.eval()

results = np.load("model/targets_2d.npy").tolist()
labels = np.load("model/embedding_labels.npy").tolist()

test_set = get_test_set()

embeddings = np.load("model/embeddings.npy")
names = np.load("model/embedding_labels.npy")

include_list = []
for index, name in enumerate(names):
    if name in test_set:
        include_list.append(index)

embeddings = embeddings[include_list]
names = names[include_list]

for name, embedding in zip(names, embeddings):

    with torch.no_grad():
        tensor = torch.tensor(embedding, dtype=torch.float32)
        prediction = model(tensor.unsqueeze(0)) 
        results.append(prediction.squeeze().numpy())

    labels.append(name + "*")

fg = plt.figure()
ax = fg.add_subplot()

for result, label in zip(results, labels):

    if label in test_set:
        color = "lime"
        set_label = "test set MDS"

    elif label[:-1] in test_set:
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
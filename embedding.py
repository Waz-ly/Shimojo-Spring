import numpy as np
import openl3
import librosa
import os
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

audio_files = []
labels = []
for file in os.listdir("stimuli"):
    if file[0] == ".":
        continue
    audio_files.append("stimuli/" + file)
    labels.append(os.path.basename(file))
for file in os.listdir("additional_stimuli"):
    if file[0] == ".":
        continue
    audio_files.append("additional_stimuli/" + file)
    labels.append(os.path.basename(file))

embeddings = []
embedding_lengths = []
for file in audio_files:
    audio, samplerate = librosa.load(file, duration=5)
    audio = np.pad(audio, (0, 5 * samplerate - len(audio)))
    embedding, timestamp = openl3.get_audio_embedding(audio, samplerate, content_type="music", embedding_size=512)
    embeddings.append(embedding.flatten())
    embedding_lengths.append(len(embedding))

initial_pca = PCA()
initial_pca.fit(embeddings)
cumvar = np.cumsum(initial_pca.explained_variance_ratio_)
n_components = np.argmax(cumvar >= 0.95) + 1

pca = PCA(n_components=n_components)
embeddings_reduced_dimensions = pca.fit_transform(embeddings)

X_embedded = TSNE(n_components=2, learning_rate='auto',
                  init='random', perplexity=3).fit_transform(embeddings_reduced_dimensions)

fig = plt.figure()
ax = fig.add_subplot()

plt.scatter(X_embedded[:, 0], X_embedded[:, 1], color="turquoise", s=100, lw=0, label="embeddings")

for (x, y), label in zip(X_embedded, labels):
    plt.annotate(
        label,
        (x, y),
        textcoords="offset points",
        xytext=(5, 5),
        ha="left",
        fontsize=9
    )

plt.savefig("embeddings.png")

plt.show()
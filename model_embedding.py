import numpy as np
import openl3
import librosa
import os
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sound_main import calculate_MDS
from model_set_generator import get_test_set

def get_embeddings():

    test_set = get_test_set()

    audio_files = []
    labels = []
    for file in os.listdir("stimuli"):
        if file[0] == "." or file in test_set:
            continue

        audio_files.append("stimuli/" + file)
        labels.append(os.path.splitext(file)[0])
    for file in os.listdir("additional_stimuli"):
        if file[0] == "." or file in test_set:
            continue

        audio_files.append("additional_stimuli/" + file)
        labels.append(os.path.splitext(file)[0])

    embeddings = []
    for file in audio_files:
        audio, samplerate = librosa.load(file, duration=5)
        audio = np.pad(audio, (0, 5 * samplerate - len(audio)))
        embedding, timestamp = openl3.get_audio_embedding(audio, samplerate, content_type="music", embedding_size=512)
        embeddings.append(embedding.flatten())

    return embeddings, labels

def graph_embeddings(embeddings, labels):

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

    plt.show()

if __name__ == "__main__":

    embeddings, embedding_labels = get_embeddings()
    targets, target_labels = calculate_MDS()

    fixed_targets = []
    fixed_target_labels = []

    for index, label in enumerate(embedding_labels):
        fixed_target_labels.append(target_labels[target_labels.tolist().index(label)])
        fixed_targets.append(targets[target_labels.tolist().index(label)])

    print(embedding_labels, fixed_target_labels)
    if not np.array_equal(embedding_labels, fixed_target_labels):
        raise Exception("labels are not the same")

    graph_embeddings(embeddings, embedding_labels)

    np.save("model/embeddings.npy", embeddings)
    np.save("model/targets_2d.npy", fixed_targets)
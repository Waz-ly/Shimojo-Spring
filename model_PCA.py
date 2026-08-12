import numpy as np
import openl3
import librosa
import os
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sound_main import calculate_MDS
import torch

if __name__ == "__main__":

    X = torch.tensor(np.load("model/embeddings.npy"), dtype=torch.float32)  # (N, D)
    names = np.load("model/embedding_labels.npy")
    y = torch.tensor(np.load("model/targets_2d.npy"),  dtype=torch.float32)  # (N, 2)

    initial_pca = PCA()
    initial_pca.fit(X)
    cumvar = np.cumsum(initial_pca.explained_variance_ratio_)
    n_components = np.argmax(cumvar >= 0.95) + 1

    pca = PCA(n_components=n_components)
    embeddings_reduced_dimensions = pca.fit_transform(X)
    print(n_components)

    np.save("model/pca_embeddings.npy", embeddings_reduced_dimensions)
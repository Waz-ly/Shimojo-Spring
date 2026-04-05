import pygame
import sklearn
import scipy.optimize
import numpy as np
import matplotlib.pyplot as plt
from sound_gui import SoundGUI
from GLOBAL import *

def calculate_MDS():
    result = np.loadtxt('result.csv', delimiter=',', dtype=str)

    labels = result[1:,0]
    data = np.array(result[1:,1:], dtype=float)

    data = np.where(data>0.5, 1/data, np.zeros_like(data))

    mds = sklearn.manifold.MDS(
        n_components=2,
        max_iter=3000,
        eps=1e-9,
        n_init=1,
        random_state=1,
        metric="precomputed",
        n_jobs=1,
        init="classical_mds",
    )
    X_mds = mds.fit(data).embedding_

    X_mds[:, 0] -= np.min(X_mds[:, 0])
    X_mds[:, 1] -= np.min(X_mds[:, 1])
    X_mds /= np.maximum(np.max(X_mds[:, 0]), np.max(X_mds[:, 1]))

    # --------------

    additional_results = np.loadtxt('additional_results.csv', delimiter=',', dtype=str)

    original_labels = additional_results[1:21,0]
    additional_labels = additional_results[21:,0]
    data = np.array(additional_results[21:,1:21], dtype=float)

    original_points = []
    for index, label in enumerate(labels):
        if label in original_labels:
            original_points.append(X_mds[index])

    for index, point in enumerate(data):
        known_distances = 1/point

        def stress(coords_flat):
            coords = coords_flat.reshape(1, 2)
            dists = np.linalg.norm(coords - original_points, axis=1)  # 2D distances
            return np.sum((dists - known_distances) ** 2)

        # Run optimizer from multiple random starts to avoid local minima
        best_result = None
        for _ in range(20):
            x0 = np.random.randn(2)
            res = scipy.optimize.minimize(stress, x0, method='L-BFGS-B')
            if best_result is None or res.fun < best_result.fun:
                best_result = res
        
        X_mds = np.concatenate([X_mds, best_result.x.reshape(1, 2)])
        labels = np.concatenate([labels, [additional_labels[index]]])

    # --------------

    fig = plt.figure()
    ax = fig.add_subplot()

    plt.scatter(X_mds[:, 0], X_mds[:, 1], color="turquoise", s=100, lw=0, label="MDS")

    for (x, y), label in zip(X_mds, labels):
        plt.annotate(
            label,
            (x, y),
            textcoords="offset points",
            xytext=(5, 5),
            ha="left",
            fontsize=9
        )

    plt.show()

    return X_mds, labels

if __name__ == "__main__":

    results, labels = calculate_MDS()

    pygame.mixer.pre_init(SAMPLE_RATE, channels=1)
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    sound_gui = SoundGUI(window, WIDTH, HEIGHT, results, labels)
    sound_gui.play_self()
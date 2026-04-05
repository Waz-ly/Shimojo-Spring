import sklearn
import numpy as np
import matplotlib.pyplot as plt
import pygame

result = np.loadtxt('results/result-0.csv', delimiter=',', dtype=str)

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
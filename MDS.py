import sklearn
import numpy as np
import matplotlib.pyplot as plt

CSV_data = np.loadtxt('similarity_scores/Trevor.csv', delimiter=',', dtype=str)

labels = CSV_data[1:,0]
data = np.array(CSV_data[1:,1:], dtype=float)

data = np.where(data!=0, 1/data, np.zeros_like(data))

cmds = sklearn.manifold.ClassicalMDS(
    n_components=2,
    metric="precomputed",
)
X_cmds = cmds.fit_transform(data)

fig = plt.figure(1)
ax = plt.axes([0.0, 0.0, 1.0, 1.0])

plt.scatter(
    X_cmds[:, 0], X_cmds[:, 1], color="lightcoral", s=100, lw=0, label="Classical MDS"
)

for (x, y), label in zip(X_cmds, labels):
    plt.annotate(
        label,
        (x, y),
        textcoords="offset points",
        xytext=(5, 5),
        ha="left",
        fontsize=9
    )

plt.show()
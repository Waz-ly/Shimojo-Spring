import matplotlib.pyplot as plt
import numpy as np

Wesley_preference = np.loadtxt('preference_scores_radial/Wesley.csv', delimiter=',', dtype=str)
Wesley_familiarity = np.loadtxt('similarity_scores_radial(50)/Wesley.csv', delimiter=',', dtype=str)

labels = Wesley_preference[2:, 0]
print(labels)

if not np.array_equal(labels, Wesley_familiarity[2:, 0]):
    print("failed to match files")

preference = np.array(Wesley_preference[2:, 1], dtype=float)
familiarity = 10 - np.array(Wesley_familiarity[2:, 1], dtype=float)

fig = plt.figure()
ax = fig.add_subplot()

plt.scatter(familiarity, preference, color="turquoise", s=100, lw=0)

for (x, y), label in zip(np.stack((familiarity, preference)).T, labels):
    plt.annotate(
        label,
        (x, y),
        textcoords="offset points",
        xytext=(5, 5),
        ha="left",
        fontsize=9
    )

plt.show()
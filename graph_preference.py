import matplotlib.pyplot as plt
import numpy as np

Wesley_preference = np.loadtxt('preference_scores_radial/Wesley.csv', delimiter=',', dtype=str)
Wesley_familiarity = np.loadtxt('similarity_scores_radial(50)/Wesley.csv', delimiter=',', dtype=str)

Shimojo_preference = np.loadtxt('preference_scores_radial/Shimojo.csv', delimiter=',', dtype=str)
Shimojo_familiarity = np.loadtxt('similarity_scores_radial(50)/Shimojo (note metal).csv', delimiter=',', dtype=str)

Matthias_preference = np.loadtxt('preference_scores_radial/Matthias.csv', delimiter=',', dtype=str)
Matthias_familiarity = np.loadtxt('similarity_scores_radial(50)/Matthias.csv', delimiter=',', dtype=str)

labels = Wesley_preference[2:, 0]
print(labels)

if not np.array_equal(labels, Shimojo_preference[2:, 0]):
    print("failed to match files")

if not np.array_equal(labels, Matthias_preference[2:, 0]):
    print("failed to match files")

preference = (np.array(Wesley_preference[2:, 1], dtype=float) + np.array(Shimojo_preference[2:, 1], dtype=float) + np.array(Matthias_preference[2:, 1], dtype=float)) / 3
familiarity = 10 + (- np.array(Wesley_familiarity[2:, 1], dtype=float) - np.array(Shimojo_familiarity[2:, 1], dtype=float) - np.array(Matthias_familiarity[2:, 1], dtype=float))/3

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
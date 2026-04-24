import matplotlib.pyplot as plt
import numpy as np
from sound_main import calculate_MDS

test_number = 5

x_mds, labels = calculate_MDS()

results = np.loadtxt('week_1_test_results.csv', delimiter=',', dtype=str)
fixed_results = np.zeros_like(results[:,1:])

for index, result in enumerate(results[0,1:]):
    fixed_results[:,labels.tolist().index(result)] = results[:,1+index]

if not np.array_equal(labels, fixed_results[0]):
    print(labels, fixed_results[0])
    raise Exception("labels are not the same")

def raw():
    fg = plt.figure()

    test_map = {
        0: 4,
        1: 2,
        2: 5,
        3: 3,
        4: 6
    }

    title_map = {
        0: "attract",
        1: "fam",
        2: "attract (fam)",
        3: "nov",
        4: "attract (nov)"
    }

    for j in range(test_number):
        data = np.array(fixed_results[j+1,:], dtype=float)

        ax = fg.add_subplot(test_number//3 + 1, 3, test_map[j], projection='3d')
        ax.set_title(title_map[j])
        ax.plot_trisurf(x_mds[:,0], x_mds[:,1], data, linewidth=0.2, antialiased=True)

        for i, label in enumerate(labels):
            ax.text(x_mds[i,0], x_mds[i,1], data[i], label, fontsize=6)

    plt.show() # just tab this line to get the graphs all seperately

def processed():

    processed_map = {
        1: 1,
        2: 2,
        3: 5,
        4: 3,
        5: 6
    }
    processed_title_map = {
        1: "fam + nov",
        2: "attract (nov) - attract",
        3: "nov",
        4: "attract (fam) - attract",
        5: "fam"
    }

    processed = []
    processed.append(np.array(fixed_results[2,:], dtype=float) + np.array(fixed_results[4,:], dtype=float) - 9)
    processed.append(np.array(fixed_results[5,:], dtype=float) - np.array(fixed_results[1,:], dtype=float))
    processed.append(np.array(fixed_results[4,:], dtype=float))
    processed.append(np.array(fixed_results[3,:], dtype=float) - np.array(fixed_results[1,:], dtype=float))
    processed.append(np.array(fixed_results[2,:], dtype=float))

    fg = plt.figure()

    for j in range(len(processed)):

        ax = fg.add_subplot(2, 3, processed_map[j + 1], projection='3d')
        ax.set_title(processed_title_map[j + 1])
        ax.plot_trisurf(x_mds[:,0], x_mds[:,1], processed[j], linewidth=0.2, antialiased=True)

        for i, label in enumerate(labels):
            ax.text(x_mds[i,0], x_mds[i,1], processed[j][i], label, fontsize=6)

    plt.show()

# novelty attract vs novelty
def novelty_donut():
    fig = plt.figure()
    ax = fig.add_subplot()

    novelty = np.array(fixed_results[4,:], dtype=float)
    attract_novelty = np.array(fixed_results[5,:], dtype=float)
    plt.scatter(novelty, attract_novelty, color="turquoise", s=100, lw=0)

    for (x, y), label in zip(np.stack((novelty, attract_novelty)).T, labels):
        plt.annotate(
            label,
            (x, y),
            textcoords="offset points",
            xytext=(5, 5),
            ha="left",
            fontsize=9
        )

    plt.show()

# attract vs familiarity
def familiar_donut():
    fig = plt.figure()
    ax = fig.add_subplot()

    # familiarity attract vs familiarity
    familiarity = 9 - np.array(fixed_results[2,:], dtype=float)
    attract_familiarity = np.array(fixed_results[1,:], dtype=float)
    plt.scatter(familiarity, attract_familiarity, color="turquoise", s=100, lw=0)

    for (x, y), label in zip(np.stack((familiarity, attract_familiarity)).T, labels):
        plt.annotate(
            label,
            (x, y),
            textcoords="offset points",
            xytext=(5, 5),
            ha="left",
            fontsize=9
        )

    plt.show()

novelty_donut()
familiar_donut()

raw()
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

fg = plt.figure()

test_map = {
    0: 4,
    1: 2,
    2: 5,
    3: 3,
    4: 6
}

title_map = {
    0: "pref",
    1: "fam",
    2: "pref (fam)",
    3: "nov",
    4: "pref (nov)"
}

for j in range(test_number):
    data = np.array(fixed_results[j+1,:], dtype=float)

    ax = fg.add_subplot(test_number//3 + 1, 3, test_map[j], projection='3d')
    ax.set_title(title_map[j])
    ax.plot_trisurf(x_mds[:,0], x_mds[:,1], data, linewidth=0.2, antialiased=True)

    for i, label in enumerate(labels):
        ax.text(x_mds[i,0], x_mds[i,1], data[i], label, fontsize=6)

plt.show() # just tab this line to get the graphs all seperately
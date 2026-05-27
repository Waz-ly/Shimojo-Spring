import matplotlib.pyplot as plt
import numpy as np
from sound_main import calculate_MDS
import scipy.stats
import statsmodels.api as sm

test_number = 5

x_mds, labels = calculate_MDS()

results = np.loadtxt('week_1_test_results.csv', delimiter=',', dtype=str)
results = results[:6,]

results2 = np.loadtxt('week_3_test_results.csv', delimiter=',', dtype=str)
results2 = results2[:6,]

fixed_results = np.zeros_like(results[:,1:])

for index, result in enumerate(results[0,1:]):
    fixed_results[0,labels.tolist().index(result)] = results[0,1+index]
    fixed_results[1:,labels.tolist().index(result)] = (np.array(results[1:,1+index],dtype=float) + np.array(results2[1:,1+index],dtype=float)) / 2

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

def novelty_vs_familiarity():

    plt.scatter(
        np.array(fixed_results[2,:], dtype=float),
        np.array(fixed_results[4,:], dtype=float),
        color="turquoise",
        s=100,
        lw=0
    )

    plt.xlabel("familiarity")
    plt.ylabel("novelty")

    m, c, r_value, p_value, *_ = scipy.stats.linregress(
        np.array(fixed_results[2,:], dtype=float),
        np.array(fixed_results[4,:], dtype=float)
    )
    plt.plot(np.array(fixed_results[2,:], dtype=float), m*np.array(fixed_results[2,:], dtype=float) + c, color='r')
    
    textstr = '\n'.join((
        r'$R^2=%.2f$' % (r_value**2, ),
        r'$\text{p value}=%.4f$' % (p_value, )
    ))

    print(r_value**2, p_value)

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    plt.text(0.05, 0.95, textstr, fontsize=14, verticalalignment='top', bbox=props)
    
    plt.plot()
    plt.show()

    def reg_m(y, x):
        x = np.array(x).T
        x = sm.add_constant(x)
        results = sm.OLS(endog=y, exog=x).fit()

        return results

    print(reg_m(
        np.array(fixed_results[1,:], dtype=float),
        [
            np.array(fixed_results[2,:], dtype=float),
            np.array(fixed_results[4,:], dtype=float)
        ]).summary()) # fam, nov

novelty_donut()
familiar_donut()

raw()
processed()

novelty_vs_familiarity()
import numpy as np
import sklearn
from sound_main import procrustes_align
import matplotlib.pyplot as plt
import random

n_targets = 20
trials = 50
MDS_scale_factor = 1.87

similarity_std_error = 2
n_ratings = 10000
n_perturbs = 1000

distance_error = 0
for rating in np.random.normal(5, 3, n_ratings):

    rating = np.clip(rating, 1, 9)

    perturbed_ratings = np.random.normal(rating, similarity_std_error, n_perturbs)
    perturbed_ratings = np.clip(perturbed_ratings, 1, 9)
    distance = 1 / perturbed_ratings

    distance_error += distance.std()

distance_error /= n_ratings
distance_error *= MDS_scale_factor
print(f"expected std error: {distance_error}")

average_dists = []
average_dist_for_noise_std = []

for noise_std in np.arange(0, 1, 0.05):

    for i in range(trials):

        targets = np.random.random((n_targets, 2))

        dissimilarity_matrix = np.zeros((n_targets, n_targets))

        for idx, target in enumerate(targets):

            for idx_other, target_other in enumerate(targets[idx+1:]):

                dist = np.linalg.norm(target - target_other) + random.gauss(0, noise_std)

                dissimilarity_matrix[idx, idx + idx_other + 1] = dist
                dissimilarity_matrix[idx + idx_other + 1, idx] = dist

        X_mds = sklearn.manifold.MDS(
            n_components=2,
            max_iter=3000,
            eps=1e-9,
            n_init=1,
            random_state=i+1,
            n_jobs=1,
            dissimilarity="precomputed"
        ).fit(dissimilarity_matrix).embedding_

        X_mds = procrustes_align(targets, X_mds)

        average_dists.append(np.average([np.linalg.norm(displacement_vec) for displacement_vec in X_mds - targets]))

    average_dist_for_noise_std.append([noise_std, np.average(average_dists)])

average_dist_for_noise_std = np.array(average_dist_for_noise_std)

plt.scatter(average_dist_for_noise_std[:, 0], average_dist_for_noise_std[:, 1])
plt.ylabel("average_dist")
plt.xlabel("noise_std")
plt.show()

# plt.scatter(targets[:, 0], targets[:, 1], c="#00FF00")
# plt.scatter(X_mds[:, 0], X_mds[:, 1], c="#0000FF")
# plt.show()
import torch
import numpy as np
import matplotlib.pyplot as plt
from sound_main import calculate_MDS
from model_set_generator import get_test_set
from model_train import Mapper

def test(seed=1, plot=False, hidden_layer_list=[32, 32], PCA=False):

    model_size = 0
    with open('model/model_info.txt', 'r') as file:
        lines = file.readlines()
        model_size = int(lines[0].split()[2])

    model = Mapper(input_dim=model_size, layer_sizes=hidden_layer_list)
    model.load_state_dict(torch.load("model/mapper.pth"))
    model.eval()

    MDS_targets = np.load("model/targets_2d.npy").tolist()
    MDS_names = np.load("model/embedding_labels.npy").tolist()

    test_set = get_test_set(seed=seed)
    test_set_list = [index for index, name in enumerate(MDS_names) if name in test_set]

    test_set_embeddings = None
    if PCA:
        test_set_embeddings = np.load("model/pca_embeddings.npy")[test_set_list]
    else:
        test_set_embeddings = np.load("model/embeddings.npy")[test_set_list]
    test_set_names = np.load("model/embedding_labels.npy")[test_set_list]

    model_results = []

    for name, embedding in zip(test_set_names, test_set_embeddings):

        with torch.no_grad():
            tensor = torch.tensor(embedding, dtype=torch.float32)
            prediction = model(tensor.unsqueeze(0))
            predicted_coords = prediction.squeeze().numpy()

            model_results.append(predicted_coords)

    # from scipy.spatial import procrustes

    # # Get model predictions for ALL points (train + test)
    # all_embeddings = np.load("model/embeddings.npy")
    # with torch.no_grad():
    #     all_preds = model(torch.tensor(all_embeddings, dtype=torch.float32)).numpy()

    # all_targets = np.load("model/targets_2d.npy")

    # # Procrustes aligns preds to targets (handles translation, scale, rotation)
    # _, preds_aligned, disparity = procrustes(all_targets, all_preds)
    # print("Procrustes disparity:", disparity)  # lower = better structural match

    if plot:

        fg = plt.figure()
        ax = fg.add_subplot()

        for target, name in zip(MDS_targets, MDS_names):

            color = "lime" if name in test_set else "turquoise"

            plt.scatter(target[0], target[1], color=color, s=100, lw=0, label="true MDS targets")
            plt.annotate(
                name, target,
                textcoords="offset points",
                xytext=(5, 5),
                ha="left",
                fontsize=6,
                color=color
            )

        for result, name in zip(model_results, test_set_names):

            plt.scatter(result[0], result[1], color="orangered", s=100, lw=0, label="model results")
            plt.annotate(
                name, result,
                textcoords="offset points",
                xytext=(5, 5),
                ha="left",
                fontsize=6,
                color="orangered"
            )

        plt.show()

    total_dist = 0
    actual_results = []
    actual_names = []

    for name, coord in zip(test_set_names, model_results):

        actual_coord = MDS_targets[MDS_names.index(name)]
        total_dist += np.linalg.norm(coord - actual_coord)

        actual_results.append(actual_coord)
        actual_names.append(name)

    average_dist = total_dist / len(model_results)
    print(f"average distance: {average_dist}")

    return average_dist

    # trials = 10000000
    # support_trials = 0

    # for i in range(trials):

    #     monte_carlo_coords = np.random.random((len(actual_results), 2))
    #     total_dist = 0

    #     for monte_carlo_coord, coord in zip(monte_carlo_coords, actual_results):

    #         total_dist += np.linalg.norm(monte_carlo_coord - coord)

    #     monte_carlo_average_dist = total_dist / len(actual_results)

    #     if monte_carlo_average_dist < average_dist:
    #         support_trials += 1

    # print(f"null hypothesis supporting trials: {support_trials}")
    # print(f"p score: {support_trials / trials}")

if __name__ == "__main__":

    test(plot=True, seed=1)
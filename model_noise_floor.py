import numpy as np
import scipy
from sound_main import calculate_MDS, procrustes_align

def estimate_noise_floor(n_runs=30):
    """
    Reruns the MDS pipeline n_runs times with different base random_states,
    Procrustes-aligns each run to a common reference, and reports how much
    each point's coordinates vary across runs. This is a lower bound on the
    achievable prediction error for your NN, since it only captures
    optimization noise -- not noise from the underlying similarity judgments
    themselves (which would require repeated-measurement/bootstrap data to
    estimate).
    """
    all_runs = []
    reference = None
    ref_labels = None

    for run_idx in range(n_runs):
        X, labels = calculate_MDS(plot=False, random_state=run_idx)
        if reference is None:
            reference = X
            ref_labels = labels
        else:
            assert list(labels) == list(ref_labels), "label order changed between runs"
            X = procrustes_align(reference, X)
        all_runs.append(X)

    all_runs = np.stack(all_runs)  # shape: (n_runs, n_points, 2)
    mean_coords = all_runs.mean(axis=0)
    deviations = all_runs - mean_coords  # (n_runs, n_points, 2)
    per_run_point_dist = np.linalg.norm(deviations, axis=2)  # (n_runs, n_points) -- Euclidean distance from mean

    # mean Euclidean distance per point (same unit as your model's metric)
    per_point_mean_dist = per_run_point_dist.mean(axis=0)  # (n_points,)

    print("Per-point noise floor (mean Euclidean distance from mean position, across runs):")
    for label, dist in zip(ref_labels, per_point_mean_dist):
        print(f"  {label:>15s}: {dist:.4f}")

    overall_mean_dist = per_run_point_dist.mean()
    print(f"\nOverall noise floor (mean Euclidean distance): {overall_mean_dist:.4f}")
    print(f"Max per-point noise floor: {per_point_mean_dist.max():.4f}")
    print("\nCompare this directly to your model's mean Euclidean distance.")

    return per_point_mean_dist, overall_mean_dist, ref_labels

if __name__ == "__main__":

    estimate_noise_floor()
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from model_set_generator import get_test_set
import random
import matplotlib.pyplot as plt

class Mapper(nn.Module):
    def __init__(self, input_dim, layer_sizes, dropout_probability=0.2):
        super().__init__()
        # self.net = nn.Linear(input_dim, 2)

        layer_sizes = [input_dim] + layer_sizes + [2]

        layers = []
        for in_dim, out_dim in zip(layer_sizes[:-1], layer_sizes[1:]):
            layers.append(nn.Linear(in_dim, out_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout_probability))

        self.net = nn.Sequential(*layers[:-2])

    def forward(self, x):
        return self.net(x)

def train(
        seed=1, training_number="max", epochs=2000,
        learning_rate=3e-6, regularization=1e-4, dropout_probability=0,
        hidden_layer_list=[32, 32],
        plot=False, PCA=False
    ):

    # --- Data ---
    X = None
    if PCA:
        X = torch.tensor(np.load("model/pca_embeddings.npy"), dtype=torch.float32)  # (N, D)
    else:
        X = torch.tensor(np.load("model/embeddings.npy"), dtype=torch.float32)
    names = np.load("model/embedding_labels.npy")
    y = torch.tensor(np.load("model/targets_2d.npy"),  dtype=torch.float32)  # (N, 2)

    test_set = get_test_set(seed)
    delete_list = [index for index, name in enumerate(names) if name in test_set]
    
    X = np.delete(X, delete_list, axis=0)
    y = np.delete(y, delete_list, axis=0)

    if training_number == "max":
        training_number = len(X)

    keep_list = np.arange(len(X))
    random.shuffle(keep_list)
    keep_list = keep_list[:training_number]

    X = X[keep_list]
    y = y[keep_list]

    print(f"training with {training_number} samples...")

    val_num = 5

    keep_list = np.arange(len(X))
    random.shuffle(keep_list)
    val_list, train_list = keep_list[:val_num], keep_list[val_num:]

    X_train, y_train = X[train_list], y[train_list]
    X_validation, y_validation = X[val_list], y[val_list]

    dataset = TensorDataset(X_train, y_train)
    input_dimensions = X.shape[1]
    loader = DataLoader(dataset, batch_size=64, shuffle=True)

    # --- Model ---
    model = Mapper(input_dim=input_dimensions, layer_sizes=hidden_layer_list, dropout_probability=dropout_probability)
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=regularization)
    loss_fn = nn.MSELoss()
    #scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5000, factor=0.5)

    # --- Training ---
    train_loss_history = []
    val_loss_history = []
    best_val_loss = float("inf")
    best_state = None
    epochs_since_improvement = 0

    for epoch in range(epochs):
        epoch_loss = 0
        for X_batch, y_batch in loader:
            pred = model(X_batch)
            loss = loss_fn(pred, y_batch)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()

        train_loss = epoch_loss / len(loader)

        model.eval()
        with torch.no_grad():
            val_pred = model(X_validation)
            val_loss = loss_fn(val_pred, y_validation).item()

        train_loss_history.append(train_loss)
        val_loss_history.append(val_loss)

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_state = {k: v.clone() for k, v in model.state_dict().items()}
            epochs_since_improvement = 0
        else:
            epochs_since_improvement += 1

        if epoch % 20 == 0 and epoch != 0:
            print(f"Epoch {epoch}, Train Loss: {train_loss:.6f}, Val Loss: {val_loss:.6f}")

        # if epochs_since_improvement >= 100:
        #     print(f"Early stopping at epoch {epoch} (no val improvement in {100} epochs)")
        #     break
        
        #scheduler.step(epoch_loss / len(loader))

    if best_state is not None:
        model.load_state_dict(best_state)

    if plot:
        plt.plot(train_loss_history, label="train")
        plt.plot(val_loss_history, label="val")
        plt.legend()
        plt.xlabel("epoch")
        plt.ylabel("MSE loss")
        plt.show()

    print("done training...")

    # --- Save ---

    with open("model/model_info.txt", "w") as file:
        file.write(f"model size: {input_dimensions}")

    torch.save(model.state_dict(), "model/mapper.pth")

if __name__ == "__main__":

    train(plot=True)
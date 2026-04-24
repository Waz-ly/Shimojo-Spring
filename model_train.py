import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

class Mapper(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Linear(input_dim, 2)

        # self.net = nn.Sequential(
        #     nn.Linear(input_dim, 512),
        #     nn.ReLU(),
        #     nn.Linear(512, 128),
        #     nn.ReLU(),
        #     nn.Linear(128, 2)   # output is (x, y)
        # )

    def forward(self, x):
        return self.net(x)

if __name__ == "__main__":

    # --- Data ---
    X = torch.tensor(np.load("model/embeddings.npy"), dtype=torch.float32)  # (N, D)
    y = torch.tensor(np.load("model/targets_2d.npy"),  dtype=torch.float32)  # (N, 2)

    dataset = TensorDataset(X, y)
    input_dimensions = X.shape[1]
    loader = DataLoader(dataset, batch_size=64, shuffle=True)

    # --- Model ---
    model = Mapper(input_dim=input_dimensions)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.MSELoss()

    # --- Training ---
    for epoch in range(200):
        for X_batch, y_batch in loader:
            pred = model(X_batch)
            loss = loss_fn(pred, y_batch)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        if epoch % 20 == 0:
            print(f"Epoch {epoch}, Loss: {loss.item():.4f}")

    print("done training...")

    # --- Save ---

    with open("model/model_info.txt", "w") as file:
        file.write(f"model size: {input_dimensions}")

    torch.save(model.state_dict(), "model/mapper.pth")
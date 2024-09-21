# torchcell/losses/weighted_mse.py
# [[torchcell.losses.weighted_mse]]
# https://github.com/Mjvolk3/torchcell/tree/main/torchcell/losses/weighted_mse.py
# Test file: torchcell/losses/test_weighted_mse.py

import torch
import torch.nn as nn


class WeightedMSELoss(nn.Module):
    def __init__(self, mean_value: float, penalty: float = 1.0):
        super().__init__()
        self.mean_value = mean_value
        self.penalty = penalty

    def forward(self, y_pred, y_true):
        weights = torch.abs(y_true - self.mean_value)
        loss = torch.mean((self.penalty * 1 + weights) * (y_true - y_pred) ** 2)
        return loss


if __name__ == "__main__":
    mean_value = 0.85
    criterion = WeightedMSELoss(mean_value=mean_value, penalty=1.0)
    y_true = torch.tensor([0.2, 0.3])
    y_pred = torch.tensor([0.21, 0.31])
    loss = criterion(y_pred, y_true)
    print(loss)

    y_true = torch.tensor([0.8, 0.9])
    y_pred = torch.tensor([0.81, 0.91])
    loss = criterion(y_pred, y_true)
    print(loss)

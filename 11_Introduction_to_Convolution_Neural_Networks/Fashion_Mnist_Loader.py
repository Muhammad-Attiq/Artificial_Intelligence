import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor

# Download training and test data
training_data = datasets.FashionMNIST(
    root="data",
    train=True,
    download=True,
    transform=ToTensor(),
)

test_data = datasets.FashionMNIST(
    root="data",
    train=False,
    download=True,
    transform=ToTensor(),
)

# Create data loaders
batch_size = 64
train_dataLoader = DataLoader(training_data, batch_size=batch_size)
test_dataLoader = DataLoader(test_data, batch_size=batch_size)

# Print output
for X, y in test_dataLoader:
    print(f"Shape of X [N, C, H, W]: {X.shape}")
    print(f"Shape of y: {y.shape} (y.dtype)")
    break

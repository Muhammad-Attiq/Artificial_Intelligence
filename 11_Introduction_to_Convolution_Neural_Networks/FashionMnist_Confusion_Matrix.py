import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Get cpu, gpu or mps device for training.
Device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)

print(f"Using {Device} device")

# Define model
class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28*28, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10)
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

# Class labels for FashionMNIST
Classes = [
    "T-shirt/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot"
]

# Download training and test data
Training_Data = datasets.FashionMNIST(
    root="data",
    train=True,
    download=True,
    transform=ToTensor(),
)

Test_Data = datasets.FashionMNIST(
    root="data",
    train=False,
    download=True,
    transform=ToTensor(),
)

# Create data loaders
Batch_Size = 64
Train_DataLoader = DataLoader(Training_Data, batch_size=Batch_Size)
Test_DataLoader = DataLoader(Test_Data, batch_size=Batch_Size)

# Initialize model and load trained weights
Model = NeuralNetwork().to(Device)
Model.load_state_dict(torch.load("model.pth", map_location=Device))
print("Loaded PyTorch Model State from model.pth")

# Get all predictions and true labels
Model.eval()
All_Preds = []
All_Labels = []

with torch.no_grad():
    for X, Y in Test_DataLoader:
        X = X.to(Device)
        Pred = Model(X)
        All_Preds.extend(Pred.argmax(1).cpu().numpy())
        All_Labels.extend(Y.numpy())

# Compute confusion matrix
Cm = confusion_matrix(All_Labels, All_Preds)

# Plot confusion matrix
plt.figure(figsize=(10, 8))
Disp = ConfusionMatrixDisplay(confusion_matrix=Cm, display_labels=Classes)
Disp.plot(cmap=plt.cm.Blues, xticks_rotation=45)
plt.title("Confusion Matrix for FashionMNIST Model")
plt.tight_layout()
plt.show()

# Print confusion matrix values
print("\nConfusion Matrix:")
print(Cm)

# Calculate and print per-class accuracy
Per_Class_Acc = Cm.diagonal() / Cm.sum(axis=1)
print("\nPer-class accuracy:")
for I, Class_Name in enumerate(Classes):
    print(f"{Class_Name:15s}: {Per_Class_Acc[I]:.2%}")

import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor

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

Model = NeuralNetwork().to(Device)

# Define loss function and optimizer
Loss_Fn = nn.CrossEntropyLoss()
Optimizer = torch.optim.SGD(Model.parameters(), lr=1e-3)

# Define train function
def Train(Dataloader, Model, Loss_Fn, Optimizer):
    Size = len(Dataloader.dataset)
    Model.train()
    
    for Batch, (X, Y) in enumerate(Dataloader):
        X, Y = X.to(Device), Y.to(Device)
        
        # Compute prediction error
        Pred = Model(X)
        Loss = Loss_Fn(Pred, Y)
        
        # Backpropagation
        Optimizer.zero_grad()
        Loss.backward()
        Optimizer.step()
        
        if Batch % 100 == 0:
            Loss_Value = Loss.item()
            Current = Batch * len(X)
            print(f"Loss: {Loss_Value:.4f} [{Current:>5d}/{Size:>5d}]")

# Define test function
def Test(Dataloader, Model, Loss_Fn):
    Size = len(Dataloader.dataset)
    Num_Batches = len(Dataloader)
    Model.eval()
    Test_Loss, Correct = 0, 0
    
    with torch.no_grad():
        for X, Y in Dataloader:
            X, Y = X.to(Device), Y.to(Device)
            Pred = Model(X)
            Test_Loss += Loss_Fn(Pred, Y).item()
            Correct += (Pred.argmax(1) == Y).type(torch.float).sum().item()
    
    Test_Loss /= Num_Batches
    Correct /= Size
    print(f"Test Error: \n Accuracy: {(100*Correct):>0.1f}%, Avg loss: {Test_Loss:>8f}\n")

# Train the model
Epochs = 5
for T in range(Epochs):
    print(f"Epoch {T+1}:")
    Train(Train_DataLoader, Model, Loss_Fn, Optimizer)
    Test(Test_DataLoader, Model, Loss_Fn)

print("Done!")

# Save the model
torch.save(Model.state_dict(), "model.pth")
print("Saved PyTorch Model State to model.pth")

# Load the model
Model = NeuralNetwork().to(Device)
Model.load_state_dict(torch.load("model.pth"))
print("Loaded PyTorch Model State from model.pth")

# Task 5: Make predictions
Classes = [
    "T-shirt/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandals",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot"
]

Model.eval()
X, Y = Test_Data[0][0], Test_Data[0][1]

with torch.no_grad():
    X = X.to(Device)
    Pred = Model(X)
    Predicted_Class = Classes[Pred.argmax().item()]
    Actual_Class = Classes[Y]
    print(f"Predicted: {Predicted_Class}, Actual: {Actual_Class}")

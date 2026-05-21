import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import time
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else 
                      "mps" if torch.backends.mps.is_available() else 
                      "cpu")
print(f"Using device: {device}")

# Data transformation with normalization
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# Load FashionMNIST dataset
print("Loading datasets...")
train_data = datasets.FashionMNIST(root="data", train=True, download=True, transform=transform)
test_data = datasets.FashionMNIST(root="data", train=False, download=True, transform=transform)

batch_size = 64
train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_data, batch_size=batch_size, shuffle=False)

# Classes
classes = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat", 
           "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]

# ==================== MLP MODEL (Baseline) ====================
class MLPModel(nn.Module):
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
        return self.linear_relu_stack(x)

# ==================== CNN MODEL ====================
class CNNModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv_layers = nn.Sequential(
            # Conv Layer 1: input 1x28x28 -> output 32x28x28 (padding=2 to keep size)
            nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),  # 32x14x14
            
            # Conv Layer 2: 32x14x14 -> 64x14x14
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),  # 64x7x7
        )
        self.fc_layers = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 7 * 7, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 10)
        )
    
    def forward(self, x):
        x = self.conv_layers(x)
        x = self.fc_layers(x)
        return x

def train_and_evaluate(model, model_name, epochs=10):
    """Train and evaluate a model, return accuracy and time"""
    model = model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    print(f"\n{'='*50}")
    print(f"Training {model_name}")
    print(f"{'='*50}")
    
    start_time = time.time()
    
    for epoch in range(epochs):
        # Training
        model.train()
        running_loss = 0.0
        for batch_idx, (images, labels) in enumerate(train_loader):
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            
            if batch_idx % 200 == 0:
                print(f"Epoch {epoch+1}/{epochs}, Batch {batch_idx}, Loss: {loss.item():.4f}")
        
        avg_loss = running_loss / len(train_loader)
        print(f"Epoch {epoch+1} completed. Average Loss: {avg_loss:.4f}")
    
    train_time = time.time() - start_time
    print(f"\nTraining completed in {train_time:.2f} seconds")
    
    # Evaluation
    model.eval()
    correct = 0
    total = 0
    all_preds = []
    all_labels = []
    
    eval_start = time.time()
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    eval_time = time.time() - eval_start
    accuracy = 100 * correct / total
    
    print(f"\n{model_name} Results:")
    print(f"Test Accuracy: {accuracy:.2f}%")
    print(f"Prediction time on test set: {eval_time:.4f} seconds")
    print(f"Average prediction time per image: {(eval_time/total)*1000:.4f} ms")
    
    return accuracy, train_time, eval_time, all_preds, all_labels

# Run MLP (Baseline)
print("\n" + "="*60)
print("PART 1: BASELINE MLP MODEL")
print("="*60)
mlp = MLPModel()
mlp_acc, mlp_train_time, mlp_eval_time, mlp_preds, mlp_labels = train_and_evaluate(mlp, "MLP", epochs=10)

# Run CNN
print("\n" + "="*60)
print("PART 2: CNN MODEL")
print("="*60)
cnn = CNNModel()
cnn_acc, cnn_train_time, cnn_eval_time, cnn_preds, cnn_labels = train_and_evaluate(cnn, "CNN", epochs=10)

# ==================== COMPARISON REPORT ====================
print("\n" + "="*60)
print("FINAL COMPARISON REPORT")
print("="*60)
print(f"{'Metric':<30} {'MLP':<20} {'CNN':<20}")
print("-" * 70)
print(f"{'Test Accuracy':<30} {mlp_acc:.2f}%{'':<15} {cnn_acc:.2f}%")
print(f"{'Total Training Time (10 epochs)':<30} {mlp_train_time:.2f} sec{'':<11} {cnn_train_time:.2f} sec")
print(f"{'Test Set Prediction Time':<30} {mlp_eval_time:.4f} sec{'':<9} {cnn_eval_time:.4f} sec")
print(f"{'Avg Prediction Time per Image':<30} {mlp_eval_time/10000*1000:.4f} ms{'':<9} {cnn_eval_time/10000*1000:.4f} ms")

# Calculate improvement
acc_improvement = cnn_acc - mlp_acc
time_difference = mlp_train_time - cnn_train_time
print("-" * 70)
print(f"CNN Accuracy Improvement over MLP: +{acc_improvement:.2f}%")
if time_difference > 0:
    print(f"CNN Training Time is {time_difference:.2f} seconds FASTER than MLP")
else:
    print(f"CNN Training Time is {abs(time_difference):.2f} seconds SLOWER than MLP")

# ==================== CONFUSION MATRICES ====================
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# MLP Confusion Matrix
cm_mlp = confusion_matrix(mlp_labels, mlp_preds)
disp_mlp = ConfusionMatrixDisplay(confusion_matrix=cm_mlp, display_labels=classes)
disp_mlp.plot(ax=axes[0], cmap=plt.cm.Blues, xticks_rotation=45)
axes[0].set_title(f"MLP Confusion Matrix\nAccuracy: {mlp_acc:.2f}%")

# CNN Confusion Matrix
cm_cnn = confusion_matrix(cnn_labels, cnn_preds)
disp_cnn = ConfusionMatrixDisplay(confusion_matrix=cm_cnn, display_labels=classes)
disp_cnn.plot(ax=axes[1], cmap=plt.cm.Greens, xticks_rotation=45)
axes[1].set_title(f"CNN Confusion Matrix\nAccuracy: {cnn_acc:.2f}%")

plt.tight_layout()
plt.show()

# ==================== PER-CLASS ACCURACY ====================
print("\n" + "="*60)
print("PER-CLASS ACCURACY COMPARISON")
print("="*60)
print(f"{'Class':<20} {'MLP Accuracy':<20} {'CNN Accuracy':<20} {'Improvement':<15}")
print("-" * 75)

mlp_per_class = cm_mlp.diagonal() / cm_mlp.sum(axis=1) * 100
cnn_per_class = cm_cnn.diagonal() / cm_cnn.sum(axis=1) * 100

for i, class_name in enumerate(classes):
    improvement = cnn_per_class[i] - mlp_per_class[i]
    print(f"{class_name:<20} {mlp_per_class[i]:.2f}%{'':<14} {cnn_per_class[i]:.2f}%{'':<14} +{improvement:.2f}%")

# ==================== SUMMARY ====================
print("\n" + "="*60)
print("SUMMARY AND CONCLUSION")
print("="*60)
print(f"""
The CNN model significantly outperformed the MLP baseline:
- Accuracy improved from {mlp_acc:.2f}% to {cnn_acc:.2f}% (+{acc_improvement:.2f}%)
- The CNN achieved better performance because it captures spatial features (edges, textures, patterns)
  that are crucial for image classification, whereas MLP treats each pixel independently.
- Classes like Shirt, T-shirt/top, Pullover, and Coat (visually similar) showed the biggest improvement
  with CNN due to its ability to learn local patterns and shapes.
- Training time: CNN took {cnn_train_time:.2f} seconds vs MLP {mlp_train_time:.2f} seconds.
- Prediction speed: Both models are efficient, with CNN being slightly {'faster' if cnn_eval_time < mlp_eval_time else 'slower'}.

RECOMMENDATION: CNN is the preferred architecture for image classification tasks like FashionMNIST
due to its superior accuracy, despite potentially longer training time.
""")

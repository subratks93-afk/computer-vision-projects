import torch
import torch.nn as nn
import torch.optim as optim

from fire_cnn_model import FireCNN
from data_preprocessing import (
    train_loader,
    val_loader,
    device,
    EPOCHS,
    LEARNING_RATE
)
model = FireCNN().to(device)
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
train_acc_history = []
val_acc_history = []

for epoch in range(EPOCHS):
    model.train()
    running_loss = 0
    correct = 0
    total = 0

    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.float().unsqueeze(1).to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        preds = (outputs > 0.5).float()
        correct += (preds == labels).sum().item()
        total += labels.size(0)

    train_acc = 100 * correct / total
    train_acc_history.append(train_acc)

    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(device), labels.float().unsqueeze(1).to(device)
            outputs = model(inputs)
            preds = (outputs > 0.5).float()
            correct += (preds == labels).sum().item()
            total += labels.size(0)

    val_acc = 100 * correct / total
    val_acc_history.append(val_acc)
   

    print(f"Epoch [{epoch+1}/{EPOCHS}], Train Acc: {train_acc:.2f}%, Val Acc: {val_acc:.2f}%")
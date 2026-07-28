import torch
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix, classification_report

from fire_cnn_model import FireCNN
from data_preprocessing import (
    val_loader,
    class_names,
    device
)

# Load trained model
model = FireCNN().to(device)
model.load_state_dict(torch.load("fire.pt", map_location=device))
model.eval()

y_true = []
y_pred = []
model.eval()
with torch.no_grad():
    for inputs, labels in val_loader:
        inputs = inputs.to(device)
        outputs = model(inputs)
        preds = (outputs > 0.5).float().cpu().numpy()
        y_pred.extend(preds)
        y_true.extend(labels.numpy())

y_pred = np.array(y_pred).flatten().astype(int)
y_true = np.array(y_true).flatten().astype(int)

conf_matrix = confusion_matrix(y_true, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt='d', xticklabels=class_names, yticklabels=class_names, cmap='Oranges')
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

print("\nClassification Report:")
print(classification_report(y_true, y_pred, target_names=class_names))
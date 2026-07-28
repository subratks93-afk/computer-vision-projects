import torch
import matplotlib.pyplot as plt

from train_fire_model import (
    model,
    train_acc_history,
    val_acc_history
)
torch.save(model.state_dict(), "fire.pt") 
print("Model saved as fire.pt") 
plt.plot(train_acc_history, label='Train Accuracy')
plt.plot(val_acc_history, label='Validation Accuracy') 
plt.xlabel('Epochs')
plt.ylabel('Accuracy (%)')
plt.title('Training and Validation Accuracy')

plt.legend()
plt.show()

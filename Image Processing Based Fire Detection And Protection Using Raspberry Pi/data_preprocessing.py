import os 
import torch
import torch.nn as nn 
import torch.optim as optim
from torchvision import datasets, transforms, models 
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report 
import numpy as np
import seaborn as sns
device = torch.device("cuda" if torch.cuda.is_available() else "cpu") 
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 10
LEARNING_RATE = 0.001
DATASET_DIR = "dataset" 
transform = transforms.Compose([
            transforms.Resize((IMG_SIZE, IMG_SIZE)), 
            transforms.ToTensor(), 
            transforms.Normalize([0.5]*3, [0.5]*3)
])
train_data = datasets.ImageFolder(os.path.join(DATASET_DIR), transform=transform) 
train_size = int(0.8 * len(train_data))
val_size = len(train_data) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(train_data, [train_size, val_size]) 
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True) 
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False) 
class_names = train_data.classes
print("Classes:", class_names)

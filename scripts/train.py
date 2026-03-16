import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models, transforms
from torch.utils.data import DataLoader
import time

# Check to use NVIDIA card if available.  Otherwise, CPU.
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Setup/format the data.
data_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Load the dataset.
data_dir = '/mnt/datasets/pokemon_ai/data'
dataset = datasets.ImageFolder(data_dir, transform=data_transforms)

# Set training parameters to manage data flow.
dataloader = DataLoader(dataset, batch_size=512, shuffle=True, num_workers=16)

# Set the model to be use.
model = models.resnet18(weights='DEFAULT')

# Adjust the final layer to match the 151 Gen 1 Pokémon.
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, len(dataset.classes))

# Move model to GPUs.
if torch.cuda.device_count() > 1:
    print(f"Using {torch.cuda.device_count()} GPUs for training!")
    model = nn.DataParallel(model)
model = model.to(device)

# 4. Setup loss function and feedback.
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 5. TRAINING LOOP
num_epochs = 30
print(f"Starting Training for {num_epochs} epochs...")

for epoch in range(num_epochs):
    start_time = time.time()
    model.train()
    running_loss = 0.0
    
    for inputs, labels in dataloader:
        inputs, labels = inputs.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
    
    epoch_duration = time.time() - start_time
    avg_loss = running_loss / len(dataloader)
    print(f"Epoch {epoch+1}/{num_epochs} - Loss: {avg_loss:.4f} - Time: {epoch_duration:.2f}s")

# Save the model and finish.
print("Training Complete! Ready to save.")
state_to_save = model.module.state_dict() if isinstance(model, nn.DataParallel) else model.state_dict()
save_path = '/mnt/checkpoints/pokemon_ai/models/first_poke_model.pth'
torch.save(state_to_save, save_path)
print(f"Model successfully saved to: {save_path}")
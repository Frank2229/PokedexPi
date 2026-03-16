import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import os

# Test Settings
CHECKPOINT = 'models/first_poke_model.pth'
LABEL_FILE = 'labels.txt'
DATA_DIR = 'data'
CONFIDENCE_THRESHOLD = 0.90 # Variable to determine if the scanned object is a Pokemon.

# Initialize the device to be used (GPU or CPU), and set up the model to be used.
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

with open(LABEL_FILE, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

model = models.resnet18()
model.fc = nn.Linear(model.fc.in_features, len(classes))
model.load_state_dict(torch.load(CHECKPOINT, map_location=device))
model = model.to(device).eval()

# Run a test on the image in the directory.
test_image_path = 'test_images/test_pikachu.jpg' 

if not os.path.exists(test_image_path):
    print(f"File not found: {test_image_path}")
    exit()

# --- 4. INFERENCE ---
img = Image.open(test_image_path).convert('RGB')
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])
input_tensor = preprocess(img).unsqueeze(0).to(device)

with torch.no_grad():
    output = model(input_tensor)
    prob = torch.nn.functional.softmax(output[0], dim=0)
    conf, index = torch.max(prob, 0)

# --- 5. THE THRESHOLD LOGIC ---
score = conf.item()
if score < CONFIDENCE_THRESHOLD:
    final_identity = "Unknown / Not a Pokémon"
    display_color = "\033[93m" # Yellow warning color in terminal
else:
    final_identity = classes[index]
    display_color = "\033[92m" # Green success color

# --- 6. DISPLAY ---
print("\n" + "█"*40)
print(f" POKÉDEX RESULT")
print(f" IDENTITY:   {display_color}{final_identity}\033[0m")
print(f" CONFIDENCE: {score*100:.2f}%")
if score < CONFIDENCE_THRESHOLD:
    print(f" (Status: Low confidence - Match rejected)")
print("█"*40 + "\n")
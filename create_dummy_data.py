import os
import numpy as np
from PIL import Image

# Create dummy images for each class to allow training to run
classes = [
    "Potato___Early_blight",
    "Potato___Healthy",
    "Tomato___Early_blight",
    "Tomato___Healthy",
    "Tomato___Late_blight"
]

base_path = "dataset/"

for cls in classes:
    path = os.path.join(base_path, cls)
    if not os.path.exists(path):
        os.makedirs(path)
    
    # Create 10 dummy images per class
    for i in range(10):
        img_array = np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8)
        img = Image.fromarray(img_array)
        img.save(os.path.join(path, f"dummy_{i}.jpg"))

print("Dummy dataset created successfully.")

import torch
from PIL import Image
import os
from RealESRGAN import RealESRGAN
from time import time

input_folder = 'data/frames'
output_folder = 'data/upscaled'

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = RealESRGAN(device, scale=2)

print('Loading weights...')

model.load_weights('weights/RealESRGAN_x2.pth', download=True)

# Ensure the output directory exists
os.makedirs(output_folder, exist_ok=True)

print('Here we go...')

start_time = time()

for i in range(1, 1001):
    print(f'Processing frame {i}')
    input_image = os.path.join(input_folder, f'frame_{i:04d}.png')
    output_image = os.path.join(output_folder, f'frame_{i:04d}.png')

    if os.path.exists(input_image):
        image = Image.open(input_image).convert('RGB')
        sr_image = model.predict(image)
        sr_image.save(output_image)

        # Log progress every 100 frames
#        if i % 2 == 0:
        elapsed_time = time() - start_time
        percentage_done = (i / 1000) * 100
        print(
            f'Processed {i} frames ({percentage_done:.2f}%) in {elapsed_time:.2f} seconds')
    else:
        print(f'{input_image} does not exist')

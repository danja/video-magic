import torch
from PIL import Image
import os
from RealESRGAN import RealESRGAN
from time import time

input_folder = 'data/frames'
output_folder = 'data/upscaled'

# number of frames to process, limit = 0 does all
limit = 401

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = RealESRGAN(device, scale=2)

print('Loading weights...')

model.load_weights('weights/RealESRGAN_x2.pth', download=True)

# Ensure the output directory exists
os.makedirs(output_folder, exist_ok=True)

# Determine the number of frames to process
if limit == 0:
    limit = len([name for name in os.listdir(
        input_folder) if name.endswith('.png')]) + 1

print(f'\nUpscaling {limit} frames...\n')

start_time = time()

for i in range(1, limit):
    print(f'Processing frame {i}')
    input_image = os.path.join(input_folder, f'frame_{i:08d}.png')
    output_image = os.path.join(output_folder, f'frame_{i:08d}.png')

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

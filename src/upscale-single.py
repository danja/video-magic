import torch
from PIL import Image
import numpy as np
from RealESRGAN import RealESRGAN

input_image = 'data/frames/frame_19257.png'
output_image = 'data/upscaled/frame_19257.png'

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = RealESRGAN(device, scale=4)
model.load_weights('weights/RealESRGAN_x4.pth', download=True)


image = Image.open(input_image).convert('RGB')

sr_image = model.predict(image)

sr_image.save(output_image)

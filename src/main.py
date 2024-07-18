import subprocess
from time import time
from RealESRGAN import RealESRGAN
from PIL import Image
import torch
import ffmpeg
import os

### From extract-frames.py ###

video_path = 'data/input/orig-vid-only.mp4'
output_folder = 'data/frames'


def extract_frames(video_path, output_folder):
    ffmpeg.input(video_path).output(f'{output_folder}/frame_%04d.png').run()


extract_frames(video_path, output_folder)

print('Frames extracted, starting upscaling')

### From upscale-many.py ###

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

for i in range(1, 401):
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

print('Upscaling complete. Now to interpolate...')

### From run-rife.py ###

### From run-rife.sh ###


def run_command(command):
    print(f"Executing command: {' '.join(command)}")
    try:
        result = subprocess.run(command, check=True,
                                text=True, capture_output=True)
        print("Command output:")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Error output: {e.stderr}")
        return False


def interpolate():
    # Define the path to the rife executable
    rife_path = '/home/danny/foaf-archive-support/rife/rife-ncnn-vulkan-20221029-ubuntu/rife-ncnn-vulkan'

    # Check if the executable exists
    if not os.path.exists(rife_path):
        print(f"Error: Rife executable not found at {rife_path}")
        return

    # Define input and output directories
    input_dir = 'data/upscaled/'
    output_dir = 'data/interpolated/'

    # Check if input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Input directory not found: {input_dir}")
        return

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Construct the command
    command = [rife_path, '-i', input_dir, '-o', output_dir]

    # Run the command
    success = run_command(command)

    if success:
        print("Rife command executed successfully.")
    else:
        print("Rife command failed.")


interpolate()


### From images-to-vid.py ###

# Input frames directory
input_folder = 'data/interpolated'

# Output video path
output_path = 'data/output/interpolated-snippet.avi'

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)


def create_video_from_frames(input_folder, output_path, start_number=1, num_frames=400, fps=8):
    # Construct the input pattern for the frames
    input_pattern = f"{input_folder}/%08d.png"

# was     input_pattern = f"{input_folder}/frame_%04d.png"

    # Create the ffmpeg input with the frame range and explicit input frame rate
    input_stream = (
        ffmpeg
        .input(input_pattern, start_number=start_number, framerate=fps)
        .filter('fps', fps=fps)
    )

    # Set up the output with lossless encoding
    output = ffmpeg.output(
        input_stream,
        output_path,
        vcodec='huffyuv',  # HuffYUV is a lossless codec compatible with AVI
        pix_fmt='rgb24',   # Use RGB color space for best quality
        acodec='none',     # No audio
        r=fps,             # Ensure output frame rate matches input
        vframes=num_frames  # Limit the number of frames in the output
    )

    # Run the ffmpeg command
    ffmpeg.run(output, overwrite_output=True)


# Call the function to create the video
create_video_from_frames(input_folder, output_path, num_frames=400, fps=8)

print(f"Video created and saved to {output_path}")

print('All done.')

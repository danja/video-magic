import os
import subprocess

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

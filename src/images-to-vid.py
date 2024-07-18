import ffmpeg
import os

# Input frames directory
input_folder = 'data/interpolated'

# Output video path
output_path = 'data/output/interpolated-snippet.avi'

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)


def create_video_from_frames(input_folder, output_path, start_number=1, num_frames=400, fps=8):
    # Construct the input pattern for the frames
    input_pattern = f"{input_folder}/frame_%04d.png"

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

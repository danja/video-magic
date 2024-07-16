import ffmpeg
import os

# Input frames directory
input_folder = 'data/upscaled'

# Output video path
output_path = 'data/output/upscaled-output.mkv'


def create_video_from_frames(input_folder, output_path, start_number=1, end_number=80, fps=8):
    # Construct the input pattern for the frames
    input_pattern = f"{input_folder}/frame_%04d.png"

    # Create the ffmpeg input with the frame range
    input_stream = ffmpeg.input(input_pattern, start_number=start_number)

    # Set up the output with lossless encoding and specified frame rate
    output = ffmpeg.output(input_stream, output_path,
                           vcodec='ffv1',  # FFV1 is a lossless video codec
                           pix_fmt='yuv444p10le',  # High quality pixel format
                           level=3,  # Highest compression level for FFV1
                           g=1,  # Every frame is an intra frame
                           vframes=end_number-start_number+1,  # Number of frames to process
                           r=fps  # Set the frame rate
                           )

    # Run the ffmpeg command
    ffmpeg.run(output, overwrite_output=True)


# Call the function to create the video
create_video_from_frames(input_folder, output_path, fps=8)

print(f"Video created and saved to {output_path}")

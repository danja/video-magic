import ffmpeg
import os

# Use absolute paths
# video_path = os.path.abspath('data/before/orig-vid-only.mp4')
# output_folder = os.path.abspath('data/frames')

video_path = 'data/before/orig-vid-only.mp4'
output_folder = 'data/frames'


def extract_frames(video_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    (
        ffmpeg
        .input(video_path)
        .output(f'{output_folder}/frame_%04d.png')
        .run()
    )


extract_frames(video_path, output_folder)

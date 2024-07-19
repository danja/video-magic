import ffmpeg
import os

video_path = 'data/input/snippet.mp4'
output_folder = 'data/frames'


def delete_files(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


def extract_frames(video_path, output_folder):
    ffmpeg.input(video_path).output(f'{output_folder}/frame_%08d.png').run()


delete_files(output_folder)
extract_frames(video_path, output_folder)

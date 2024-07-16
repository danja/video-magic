import ffmpeg
import os

video_path = 'data/before/orig-vid-only.mp4'
output_folder = 'data/frames'


def extract_frames(video_path, output_folder):
    ffmpeg.input(video_path).output(f'{output_folder}/frame_%04d.png').run()


extract_frames(video_path, output_folder)

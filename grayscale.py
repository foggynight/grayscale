#!/usr/bin/env python3

import os
from sys import argv

import cv2
import moviepy.editor as mp

def error(*message):
    for line in message:
        print(line)
    exit(1)


def parse_argv():
    argc = len(argv)
    if argc < 3 or argc > 3:
        error('grayscale: error: invalid arguments',
              'usage: grayscale INPUT_PATH OUTPUT_PATH')
    input_path = argv[1]
    output_path = argv[2]
    print(f'Reading: {input_path}')
    print(f'Writing: {output_path}')
    return input_path, output_path


def get_extension(path):
    split_path = path.split('.')
    if len(split_path) < 2:
        error(f'grayscale: error: invalid file path: {path}')
    return split_path[-1]


def convert_image(input_path, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        error(f'grayscale: error: failed to open: {input_path}')
    print('Converting image to grayscale...')
    cv2.imwrite(output_path, img)


def get_video_handles(input_path, output_path):
    source = cv2.VideoCapture(input_path)
    if (source.isOpened() == False):
        error(f'grayscale: error: failed to open: {input_path}')
    destination = cv2.VideoWriter(
            output_path,
            cv2.VideoWriter_fourcc(*'mp4v'),
            float(source.get(cv2.CAP_PROP_FPS)),
            (int(source.get(cv2.CAP_PROP_FRAME_WIDTH)), int(source.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    return source, destination


def read_frame(source):
    ret, frame = source.read()
    return frame if ret else None


def convert_video(input_path):
    silent_path = '__silent_' + input_path
    source, destination = get_video_handles(input_path, silent_path)
    print('Converting video to grayscale...')
    while (frame := read_frame(source)) is not None:
        # The frame must be in the BGR format to be written to file. The
        # following converts to GRAY and back to BGR, making the frame grayscale
        # while allowing it to be written to file.
        destination.write(cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR))
    source.release(), destination.release()
    return silent_path


def get_audio(input_path):
    audio_path = '__audio_' + ''.join(input_path.split('.')[:-1]) + '.wav'
    mp.VideoFileClip(input_path).audio.write_audiofile(audio_path)
    return audio_path


def add_audio(audio_path, silent_path, output_path):
    video_clip = mp.VideoFileClip(silent_path)
    audio_clip = mp.AudioFileClip(audio_path)
    video_clip.audio = audio_clip
    print('Adding original audio to converted video...')
    video_clip.write_videofile(output_path, logger=None)


if __name__ == '__main__':
    image_extensions = ['png']
    video_extensions = ['mp4']

    input_path, output_path = parse_argv()
    input_extension = get_extension(input_path)

    if input_extension != get_extension(output_path):
        error('grayscale: error: input and output file extensions differ')

    if input_extension in image_extensions:
        convert_image(input_path, output_path)
    elif input_extension in video_extensions:
        audio_path = get_audio(input_path)
        silent_path = convert_video(input_path)
        add_audio(audio_path, silent_path, output_path)
        os.remove(audio_path)
        os.remove(silent_path)
    else:
        error(f'grayscale: error: invalid input file extension: {input_extension}')

#!/usr/bin/env python3

# *** grayscale ***
#
# Convert an image or video to grayscale.
#
# Copyright (C) 2021 Robert Coffey
# Released under the MIT license

from sys import argv

import cv2

def parse_argv():
    argc = len(argv)
    if argc < 3 or argc > 3:
        print('grayscale: error: invalid arguments')
        print('usage: grayscale INPUT_PATH OUTPUT_PATH')
        exit(1)

    input_path = argv[1]
    output_path = argv[2]

    print(f'Reading: {input_path}')
    print(f'Writing: {output_path}')
    print('Converting to grayscale...')

    return input_path, output_path

def get_extension(path):
    split_path = path.split('.')
    if len(split_path) < 2:
        print(f'grayscale: error: invalid file path: {path}')
        exit(1)

    return split_path[-1]

def convert_image(input_path, output_path):
    img = cv2.imread(input_path, 0)
    if img is None:
        print(f'grayscale: error: failed to open: {input_path}')
        exit(1)

    cv2.imwrite(output_path, img)

def get_video_handles(input_path, output_path):
    source = cv2.VideoCapture(input_path)
    if (source.isOpened() == False):
        print(f'grayscale: error: failed to open: {input_path}')
        exit(1)

    destination = cv2.VideoWriter(
            output_path,
            cv2.VideoWriter_fourcc(*'mp4v'),
            float(source.get(cv2.CAP_PROP_FPS)),
            (int(source.get(cv2.CAP_PROP_FRAME_WIDTH)), int(source.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    return source, destination

def read_frame(source):
    ret, frame = source.read()
    return frame if ret else None

def convert_video(input_path, output_path):
    source, destination = get_video_handles(input_path, output_path)

    while (frame := read_frame(source)) is not None:
        # The frame must be in the BGR format to be written to file. The
        # following converts to GRAY and back to BGR, making the frame
        # grayscale while allowing it to be written to file.
        destination.write(cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR))

    source.release(), destination.release()

if __name__ == '__main__':
    image_extensions = ['png']
    video_extensions = ['mp4']

    input_path, output_path = parse_argv()
    input_extension = get_extension(input_path)

    if input_extension != get_extension(output_path):
        print('grayscale: error: input and output file extensions differ')
        exit(1)

    if input_extension in image_extensions:
        convert_image(input_path, output_path)
    elif input_extension in video_extensions:
        convert_video(input_path, output_path)
    else:
        print(f'grayscale: error: invalid input file extension: {input_extension}')

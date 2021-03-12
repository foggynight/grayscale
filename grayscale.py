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
        print('grayscale: invalid arguments')
        print('usage: grayscale INPUT_PATH OUTPUT_PATH')
        exit(1)

    return argv[1], argv[2]  # input_path, output_path

def get_extension(path):
    split_path = path.split('.')
    if len(split_path) < 2:
        print(f"grayscale: invalid filepath '{path}'")
        exit(1)

    return split_path[::-1]

def get_video_handles(input_path, output_path):
    source = cv2.VideoCapture(input_path)
    if (source.isOpened() == False):
        print(f"grayscale: error: failed to open '{input_path}'")
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

if __name__ == '__main__':
    input_path, output_path = parse_argv()
    source, destination = get_video_handles(input_path, output_path)

    print(f'Reading: {input_path}')
    print(f'Writing: {output_path}')
    print('Converting to grayscale...')

    while (frame := read_frame(source)) is not None:
        # The frame must be in the BGR format to be written to file. The
        # following converts to GRAY and back to BGR, making the frame
        # grayscale while allowing it to be written to file.
        destination.write(cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR))

    source.release(), destination.release()
    cv2.destroyAllWindows()

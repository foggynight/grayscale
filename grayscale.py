#!/usr/bin/env python3

# *** grayscale ***
#
# Convert an image or video to grayscale.
#
# Copyright (C) 2021 Robert Coffey
# Released under the MIT license

from sys import argv

import cv2

def read_frame(source):
    if not source.isOpened():
        return None

    ret, frame = source.read()

    return frame if ret else None

if __name__ == '__main__':
    input_path = argv[1]
    output_path = argv[2]

    print(f"Input path:   {input_path}")
    print(f"Output path:  {output_path}")
    print(f"Converting to grayscale...")

    source = cv2.VideoCapture(input_path)
    if (source.isOpened() == False):
        print(f"grayscale: error: failed to open '{input_path}'")
        exit(1)

    video_fps = float(source.get(cv2.CAP_PROP_FPS))
    video_width = int(source.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(source.get(cv2.CAP_PROP_FRAME_HEIGHT))

    destination = cv2.VideoWriter(
            output_path,
            cv2.VideoWriter_fourcc(*'mp4v'),
            video_fps,
            (video_width, video_height))

    while (frame := read_frame(source)) is not None:
        # The frame must be in the BGR format to be written to file. The
        # following converts to GRAY and back to BGR, making the frame
        # grayscale while allowing it to be written to file.
        destination.write(cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR))

    destination.release()
    source.release()

    cv2.destroyAllWindows()

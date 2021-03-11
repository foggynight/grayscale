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
    video_path = argv[1]

    source = cv2.VideoCapture(video_path)
    if (source.isOpened() == False):
        print(f"grayscale: error: failed to open '{video_path}'")
        exit(1)

    video_fps = float(source.get(cv2.CAP_PROP_FPS))
    video_width = int(source.get(3))
    video_height = int(source.get(4))

    destination = cv2.VideoWriter(
            'output.mp4',
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

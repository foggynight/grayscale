#!/usr/bin/env python3

# *** grayscale ***
#
# Convert an image or video to grayscale.
#
# Copyright (C) 2021 Robert Coffey
# Released under the MIT license

from sys import argv
from time import sleep

import cv2

if __name__ == '__main__':
    playback_fps = 60
    source = cv2.VideoCapture(argv[1])

    while True:
        ret, img = source.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imshow(argv[1], gray)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

        sleep(1 / playback_fps)

    source.release()
    cv2.destroyAllWindows()

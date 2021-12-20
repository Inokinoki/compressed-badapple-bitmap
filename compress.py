import cv2
import numpy as np
import sys

intra_index = 1
prev_intra_frame = None
next_intra_frame = cv2.imread("BadAppleIFrames/image-{:03d}.bmp".format(intra_index))

sum = 0
for i in range(1, 6572 + 1):
    current_frame = cv2.imread("BadAppleAllFrames/image-{:04d}.bmp".format(i))
    if next_intra_frame is not None and np.count_nonzero(current_frame - next_intra_frame) == 0:
        # Poll the next image
        print("Next {}".format(intra_index), file=sys.stderr)
        intra_index += 1
        prev_intra_frame = next_intra_frame
        next_intra_frame = cv2.imread("BadAppleIFrames/image-{:03d}.bmp".format(intra_index))
    else:
        diff = int(np.count_nonzero(current_frame - prev_intra_frame) / 3)
        sum += diff
        print(diff)
        prev_intra_frame = current_frame

print(sum, file=sys.stderr)

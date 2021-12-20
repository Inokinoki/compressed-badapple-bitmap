import cv2
import numpy as np
import sys
import struct

intra_index = 1
prev_intra_frame = None
next_intra_frame = cv2.imread("BadAppleIFrames/image-{:03d}.bmp".format(intra_index), cv2.IMREAD_GRAYSCALE)

sum = 0
with open("BA.bin", "wb") as output_file:
    for i in range(1, 6572 + 1):
        current_frame = cv2.imread("BadAppleAllFrames/image-{:04d}.bmp".format(i), cv2.IMREAD_GRAYSCALE)
        if next_intra_frame is not None and np.count_nonzero(current_frame - next_intra_frame) == 0:
            # Poll the next image
            print("Next {}".format(intra_index), file=sys.stderr)
            intra_index += 1
            prev_intra_frame = next_intra_frame
            next_intra_frame = cv2.imread("BadAppleIFrames/image-{:03d}.bmp".format(intra_index), cv2.IMREAD_GRAYSCALE)

            print("Key frame {}".format(i))
            output_file.write(struct.pack("<I", 0x7FFFFFFF))
        else:
            diff_pixels = current_frame - prev_intra_frame
            diff = int(np.count_nonzero(current_frame - prev_intra_frame) / 3)
            sum += diff
            if diff == 0:
                # No difference
                print("Not diff {}".format(i))
            else:
                # Find and output all differences
                print("Not key frame {}".format(i))
                for xi in range(diff_pixels.shape[1]):
                    for yi in range(diff_pixels.shape[0]):
                        if diff_pixels[yi, xi] >= 128:
                            # print(yi, xi, diff_pixels[yi, xi])
                            output_file.write(struct.pack("<I", 0x80000000 | (xi << 16) | yi))
            output_file.write(struct.pack("<I", 0xFFFFFFFF))
            # print(diff_pixels)
            prev_intra_frame = current_frame

print(sum, file=sys.stderr)

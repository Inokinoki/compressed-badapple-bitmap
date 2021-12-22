import cv2
import numpy as np
import sys
import struct

GRAY_SCALE = 8

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
            diff = int(np.count_nonzero(diff_pixels) / 3)
            diff_pixels_rev = prev_intra_frame - current_frame
            diff += int(np.count_nonzero(diff_pixels_rev) / 3)
            sum += diff
            if diff == 0:
                # No difference
                print("Not diff {}".format(i))
            else:
                # Find and output all differences
                print("Not key frame {}".format(i))
                for xi in range(diff_pixels.shape[1]):
                    for yi in range(diff_pixels.shape[0]):
                        if diff_pixels[yi, xi] >= int(256 / GRAY_SCALE) or diff_pixels_rev[yi, xi] >= int(256 / GRAY_SCALE):
                            # print(yi, xi, diff_pixels[yi, xi])
                            gray_scale = (int(current_frame[yi, xi] / GRAY_SCALE) & (GRAY_SCALE - 1))
                            if diff_pixels[yi, xi] >= int(256 / GRAY_SCALE * 6) or diff_pixels_rev[yi, xi] >= int(256 / GRAY_SCALE * 6):
                                output_file.write(struct.pack("<I", 0x80000000 | (gray_scale << 28) | (xi << 16) | yi))
                                # Modify current_frame
                                current_frame[yi, xi] = (gray_scale * 256 / GRAY_SCALE)
            output_file.write(struct.pack("<I", 0xFFFFFFFF))
            # print(diff_pixels)
            prev_intra_frame = current_frame

print(sum, file=sys.stderr)

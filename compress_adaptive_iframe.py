import cv2
import numpy as np
import sys
import struct

GRAY_SCALE = 8

intra_index = 1
prev_intra_frame = None

sum = 0
with open("BA.bin", "wb") as output_file:
    for i in range(1, 6572 + 1):
        current_frame = cv2.imread("BadAppleAllFrames/image-{:04d}.bmp".format(i), cv2.IMREAD_GRAYSCALE)
        if prev_intra_frame is None:
            prev_intra_frame = current_frame
            print("New key frame {}".format(i))
            output_file.write(struct.pack("<I", 0x7FFFFFFF))
            cv2.imwrite("BadAppleIFramesOutput/image-{:03d}.bmp".format(intra_index), prev_intra_frame)
            intra_index += 1
        else:
            diff_pixels = np.abs(current_frame / int(GRAY_SCALE) - prev_intra_frame / int(GRAY_SCALE)) > 3
            diff = int(np.count_nonzero(diff_pixels))
            #diff_pixels_rev = prev_intra_frame / int(GRAY_SCALE) - current_frame / int(GRAY_SCALE)
            # print(diff_pixels)
            #diff += int(np.count_nonzero(diff_pixels_rev))
            if diff == 0:
                # No difference
                print("Not diff {}".format(i))
                output_file.write(struct.pack("<I", 0xFFFFFFFF))
            elif diff >= int(prev_intra_frame.shape[0] * prev_intra_frame.shape[1] * 1 / 2):
                # Output an intra-frame
                prev_intra_frame = current_frame
                print("New key frame {}".format(i))
                output_file.write(struct.pack("<I", 0x7FFFFFFF))
                cv2.imwrite("BadAppleIFramesOutput/image-{:03d}.bmp".format(intra_index), prev_intra_frame)
                intra_index += 1
            else:
                # Find and output all differences
                print("Not key frame {}".format(i))
                for xi in range(diff_pixels.shape[1]):
                    for yi in range(diff_pixels.shape[0]):
                        if diff_pixels[yi, xi]: # > 3 or diff_pixels_rev[yi, xi] > 3:
                            # print(yi, xi, diff_pixels[yi, xi])
                            gray_scale = (int(current_frame[yi, xi] / GRAY_SCALE) & (GRAY_SCALE - 1))
                            # if diff_pixels[yi, xi] >= int(256 / GRAY_SCALE) or diff_pixels_rev[yi, xi] >= int(256 / GRAY_SCALE):
                            output_file.write(struct.pack("<I", 0x80000000 | (gray_scale << 28) | (xi << 16) | yi))
                            # Modify current_frame
                            current_frame[yi, xi] = (gray_scale * 256 / GRAY_SCALE)
                output_file.write(struct.pack("<I", 0xFFFFFFFF))
                # print(diff_pixels)
                prev_intra_frame = current_frame
                # Accumulate diff
                sum += diff

print(sum, file=sys.stderr)

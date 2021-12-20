import struct

frame_counter = 1

with open("BA.bin", "rb") as input_file:
    while True:
        data = input_file.read(4)
        if not data: break
        s = struct.unpack("<I", data)
        if len(s) > 0:
            v = s[0]
            if v & 0x80000000:
                if v == 0xFFFFFFFF:
                    # print("Keep prev frame and output")
                    frame_counter += 1
                else:
                    # print("Patch prev frame")
                    pass
            else:
                # print("Read frame")
                frame_counter += 1
    print(frame_counter)

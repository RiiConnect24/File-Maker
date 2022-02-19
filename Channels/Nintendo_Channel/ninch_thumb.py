import struct
import os


def u8(data):
    if not 0 <= data <= 255:
        print("u8 out of range: %s" % data, "INFO")
        data = 0
    return struct.pack(">B", data)


def u16(data):
    if not 0 <= data <= 65535:
        print("u16 out of range: %s" % data, "INFO")
        data = 0
    return struct.pack(">H", data)


def u32(data):
    if not 0 <= data <= 4294967295:
        print("u32 out of range: %s" % data, "INFO")
        data = 0
    return struct.pack(">I", data)


class MakeThumb:
    def __init__(self):
        print("Generating File...")
        self.header = {}
        self.make_header()
        self.make_jpeg_table()
        self.write_jpegs()
        self.write_file()

    def offset_count(self):
        """
        This function returns the offset of where the selected table is
        """
        return sum(len(values) for values in list(self.header.values()) if values)

    def make_header(self):
        self.header["unknown"] = u16(0)
        self.header["version"] = u8(6)
        self.header["unknownRegion"] = u8(2)
        self.header["fileSize"] = u32(0)
        self.header[f"unknown1_1"] = u32(601820255)
        self.header[f"unknown1_2"] = u32(1)
        self.header[f"unknown1_3"] = u32(49)
        self.header[f"unknown1_4"] = u32(1)
        self.header[f"unknown1_5"] = u32(1252951207)
        self.header[f"number_of_images"] = u32(120)

    def make_jpeg_table(self):
        for i in range(120):
            self.header[f"jpegSize_{i}"] = u32(0)
            self.header[f"jpegOffset_{i}"] = u32(0)

    def write_jpegs(self):
        deadbeef = {0: 0xDE, 1: 0xAD, 2: 0xBE, 3: 0xEF}
        for i in range(120):
            with open("testing.jpeg", "rb") as image:
                self.header[f"jpegOffset_{i}"] = u32(self.offset_count())
                self.header[f"JPEGData{i}"] = image.read()
                counter = 0
                while self.offset_count() % 32 != 0:
                    self.header[f"deadbeef_{i}_{counter}"] = u8(deadbeef[counter % 4])
                    counter += 1
                # Seek to end of file to set filesize
                image.seek(0, os.SEEK_END)
                self.header[f"jpegSize_{i}"] = u32(image.tell())
                image.close()

    def write_file(self):
        # Now that all the file contents are written, calculate filesize
        self.header["fileSize"] = u32(self.offset_count())

        filename = "testing.thumb"

        if os.path.exists(filename):
            os.remove(filename)

        self.writef = open(filename, "ab")

        for values in self.header.values():
            self.writef.write(values)

        self.writef.close()


MakeThumb()

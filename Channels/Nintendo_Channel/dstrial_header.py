import binascii
import collections
import struct
import sys

def u8(data):
    if not 0 <= data <= 255:
        log("u8 out of range: %s" % data, "INFO")
        data = 0
    return struct.pack(">B", data)


def u16(data):
    if not 0 <= data <= 65535:
        log("u16 out of range: %s" % data, "INFO")
        data = 0
    return struct.pack(">H", data)


def u32(data):
    if not 0 <= data <= 4294967295:
        log("u32 out of range: %s" % data, "INFO")
        data = 0
    return struct.pack(">I", data)


def u32_littleendian(data):
    if not 0 <= data <= 4294967295:
        log("u32 little endian out of range: %s" % data, "INFO")
        data = 0
    return struct.pack("<I", data)

if len(sys.argv) != 4:
    print("Usage: dstrial_header.py <nds file> <name> <title id>")
    sys.exit(1)
elif len(sys.argv[2]) > 98:
    print("Error: Name must be less than or equal to 98 characters.")
    sys.exit(1)
elif len(sys.argv[3]) != 4:
    print("Error: Title ID must be 4 characters.")
    sys.exit(1)

class make_rom():
    def __init__(self):
        self.open_rom()
        self.make_rom()
        self.write_file()

        print("Completed Successfully")

    def open_rom(self):
        self.rom = open(sys.argv[1], "rb").read()
        
    def make_rom(self):
        self.header = collections.OrderedDict()

        self.header["unknown"] = u16(0)
        self.header["version"] = u8(6)
        self.header["unknown_region"] = u8(2)
        self.header["filesize"] = u32(332 + len(self.rom))
        self.header["crc32"] = u32(0)
        self.header["country_code"] = u32(49)
        self.header["language_code"] = u32(1)
        self.header["rom_offset"] = u32(332)
        self.header["rom_size"] = u32(len(self.rom))
        self.header["game_title"] = sys.argv[2].encode("utf-16be").ljust(98, b"\0")
        self.header["game_description"] = "Nintendo Channel Demo".encode("utf-16be").ljust(194, b"\0")
        self.header["removal_year"] = u16(65535) # No removal year
        self.header["removal_month"] = u8(255) # No removal month
        self.header["removal_day"] = u8(255) # No removal day
        self.header["company_id"] = u32(1)
        self.header["title_id"] = sys.argv[3].encode()
    
    def write_file(self):
        self.writef = open(sys.argv[1] + "-output.bin", "wb")

        for values in self.header.values():
            self.writef.write(values)

        self.writef.write(self.rom)
        
        self.readf = open(sys.argv[1] + "-output.bin", "rb")

        self.writef.seek(8)
        self.writef.write(binascii.unhexlify(format(binascii.crc32(self.readf.read()) & 0xFFFFFFFF, '08x')))  

        self.writef.close()

make_rom()
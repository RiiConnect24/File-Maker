import binascii
import hashlib
import hmac
import json
import os
import struct
import subprocess
import sys

with open("./Channels/Check_Mii_Out_Channel/config.json", "rb") as f:
    config = json.load(f)

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

class Addition():
    def __init__():
        self.build()
        
        filename = "{}/addition/201.ces".format(config["file_path"])
        
        Write(filename)
    
    def build(self):
        self.addition = {}

        self.addition["type"] = "AD"
        self.addition["padding1"] = u8(0) * 2
        self.addition["id1"] = u32(0)
        self.addition["id2"] = u32(201)
        self.addition["padding2"] = u8(0) * 12
        self.addition["padding3"] = u8(255) * 8
        self.addition["adtag"] = "AD"
        self.addition["adtagsize"] = u8(48)
        self.addition["unk1"] = u32(1)
        self.addition["unk2"] = u32(1)
        self.addition["unk3"] = u32(1)
        self.addition["unk4"] = u32(1)
        self.addition["unk5"] = u32(1)
        self.addition["unk6"] = u32(1)
        self.addition["unk7"] = u32(1)


class ConDetail():
    def __init__():
        self.build()
        
        filename = "{}/contest/4294967295/con_detail0.ces".format(config["file_path"])
        
        Write(filename)
    
    def build(self):
        self.condetail = {}

        self.condetail["type"] = "CD"
        self.condetail["padding1"] = u8(0) * 2
        self.condetail["id1"] = u32(4294967295)
        self.condetail["id2"] = u8(0)
        self.condetail["padding2"] = u8(0) * 12
        self.condetail["padding3"] = u8(255) * 8
        self.condetail["cdtag"] = "CD"
        self.condetail["cdtagsize"] = u16(64)
        self.condetail["activecontest"] = u32(1)
        self.condetail["endtime"] = u32(4294967295)
        self.condetail["flags"] = 0x22000000
        self.condetail["unk4"] = 0x19191919
        self.condetail["unk5"] = 0x19191919
        self.condetail["unk6"] = 0x19191919
        self.condetail["unk7"] = 0x19191919

class First():
    def __init__():
        self.build()
        
        filename = "{}/first/49.ces".format(config["file_path"])
        
        Write(filename)

    def build(self):
        self.first = {}

        self.first["type"] = "FD"
        self.first["padding1"] = u8(0) * 2
        self.first["id1"] = u32(49) # country code
        self.first["id2"] = u32(0)
        self.first["padding2"] = u8(0) * 12
        self.first["padding3"] = u8(0) * 8
        self.first["fdtag"] = "FD"
        self.first["fdtagsize"] = u8(32)
        self.first["serveractive"] = u32(1)
        self.first["unk1"] = 0x96000001
        self.first["unk2"] = 0x41004100
        self.first["unk3"] = 0x41004100
        self.first["unk4"] = 0x41004100
        self.first["unk5"] = 0x41004100
        self.first["unk6"] = 0x41004100

class Write(filename):
    def __init__(filename):
        self.filename = filename

        self.compress()
        self.encrypt()
        self.hmac()
        self.write()

    def compress(self):
        self.writef = open(self.filename + "1"), "wb")

        for v in self.addition.values():
            self.writef.write(v)

        self.writef.close()

        subprocess.call(["{}/lzss".format(config["lzss_path"]), "-evf", self.filename + "1", self.filename + "2")
        
        os.remove(self.filename + "1")
        os.remove(self.filename + "2")

    def encrypt(self):
        self.key = binascii.unhexlify("8D22A3D808D5D072027436B6303C5B50")
        self.iv = binascii.unhexlify("BE5E548925ACDD3CD5342E08FB8ABFEC")

        self.data = open(self.filename, "rb").read()
        
        self.aes = pyaes.AESModeOfOperationCBC(self.key, iv=self.iv)
        self.processed = self.aes.encrypt(self.data)
        
    def hmac(self):
        self.sign = binascii.unhexlify("4CC08FA141DE2537AAA52B8DACD9B56335AFE467")

        self.digester = hmac.new(self.sign, self.processed, hashlib.sha1)
        self.hmacsha1 = digester.hexdigest()

    def write(self):
        self.filename = self.filename[:-1]

        self.writef = open(self.filename, "wb").read()

        self.writef.write("MC")
        self.writef.write(u16(1))
        self.writef.write(self.hmacsha1)
        self.writef.write(self.processed)

        self.writef.close()
import binascii
import hashlib
import hmac
import json
import os
import struct
import subprocess
import sys
from crc16 import crc16xmodem

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

class ResetList(): #removes all miis from a list
    def __init__(self, list_type):
        if list_type == b'SL': filename = 'spot_list.ces'
        elif list_type == b'PL': filename = 'pop_list.ces'
        elif list_type == b'RL': filename = 'bargain_list.ces'
        else: raise ValueError('Invalid list type!')

        self.list_type = list_type
        self.mii = {}
        self.reset()
        Write('write', filename, self.mii)

    def reset(self):
        self.mii['list_type'] = self.list_type
        self.mii['padding1'] = u8(0) * 2
        self.mii['countrycode'] = u32(150)
        self.mii['padding2'] = u32(0) * 5
        self.mii['end_header'] = b'\xFF\xFF\xFF\xFF'
        self.mii['pn_tag'] = b'PN'
        self.mii['pn_size'] = u16(12)
        self.mii['unk1'] = u32(1)
        self.mii['mii_count'] = u32(0)


class AddMii(): #adds mii to specified list_type
    def __init__(self, list_type, miidata, popularity, initials, craftsno, artisandata): #add entryno param once the database is ready
        
        if list_type == b'SL': filename = 'spot_list.ces'
        elif list_type == b'PL': filename = 'pop_list.ces'
        elif list_type == b'RL': filename = 'bargain_list.ces'
        else: raise ValueError('Invalid list type!')

        with open(filename[:-3] + 'dec', 'rb+') as file: 
            index = (int.from_bytes(file.read()[40:44], byteorder='big')) + 1 #gets the current mii count and index in PN, and increases it
            file.seek(40) #goes to 40th byte where the mii count begins
            file.write(u32(index))

        self.list_type = list_type #list type must be SL, NL, RL, or PL in bytes format
        self.index = index #used for mii count in PN section. mii and its artisan must have this same number
        self.entryno = index #unique entry number per mii. if two or more miis on the list have the same entry number, none of them will show
        self.miidata = miidata #mii binary data WITHOUT its crc16 at the end
        self.popularity = popularity #must be a binary hexadecimal with the popularity value
        self.initials = initials #if it doesn't have a second initial, replace it with 0x00
        self.craftsno = craftsno #mii artisan ID
        self.artisandata = artisandata #mii artisan face data
        self.mii = {}
        self.build()
        
        Write('append', filename, self.mii)

    def build(self):
        self.mii['pm_tag'] = b'PM'
        self.mii['pm_size'] = u16(96)
        self.mii['mii_index'] = u32(self.index)
        self.mii['entry_number'] = u32(self.entryno) 
        self.mii['mii'] = self.miidata
        self.mii['crc16'] = u16(crc16xmodem(self.miidata)) #crc functions can be removed if mii data already contains its CRC16
        self.mii['unk2'] = u16(0)
        self.mii['popularity'] = self.popularity
        self.mii['unk3'] = u8(0)
        self.mii['skill'] = u16(0)
        self.mii['initials'] = self.initials 
        self.mii['pc_tag'] = b'PC'
        self.mii['pc_size'] = u16(96)
        self.mii['creator_index'] = u32(self.index)
        self.mii['creator_number'] = u32(30)
        self.mii['mii_artisan'] = self.artisandata
        self.mii['crc162'] = u16(crc16xmodem(self.artisandata))
        self.mii['master_artisan'] = u8(0)
        self.mii['unk5'] = u16(0)
        self.mii['unk6'] = u16(0)
        self.mii['country_code2'] = u8(49)
        self.mii['unk7'] = u16(0)

class Addition():
    def __init__(self):
        self.build()
        
        filename = "{}/addition/201.ces".format(config["file_path"])
        
        Write('write', filename, self.addition)
    
    def build(self):
        self.addition = {}

        self.addition["type"] = b'AD'
        self.addition["padding1"] = u8(0) * 2
        self.addition["id1"] = u32(0)
        self.addition["id2"] = u32(201)
        self.addition["padding2"] = u8(0) * 12
        self.addition["padding3"] = u8(255) * 8
        self.addition["adtag"] = b'AD'
        self.addition["adtagsize"] = u8(48)
        self.addition["unk1"] = u32(1)
        self.addition["unk2"] = u32(1)
        self.addition["unk3"] = u32(1)
        self.addition["unk4"] = u32(1)
        self.addition["unk5"] = u32(1)
        self.addition["unk6"] = u32(1)
        self.addition["unk7"] = u32(1)


class ConDetail():
    def __init__(self):
        self.build()
        
        filename = "{}/contest/4294967295/con_detail0.ces".format(config["file_path"])
        
        Write('write', filename, self.condetail)
    
    def build(self):
        self.condetail = {}

        self.condetail["type"] = b'CD'
        self.condetail["padding1"] = u8(0) * 2
        self.condetail["id1"] = u32(4294967295)
        self.condetail["id2"] = u8(0)
        self.condetail["padding2"] = u8(0) * 12
        self.condetail["padding3"] = u8(255) * 8
        self.condetail["cdtag"] = b'CD'
        self.condetail["cdtagsize"] = u16(64)
        self.condetail["activecontest"] = u32(1)
        self.condetail["endtime"] = u32(4294967295)
        self.condetail["flags"] = 0x22000000
        self.condetail["unk4"] = 0x19191919
        self.condetail["unk5"] = 0x19191919
        self.condetail["unk6"] = 0x19191919
        self.condetail["unk7"] = 0x19191919

class First():
    def __init__(self, code):
        self.build()
        code = self.code
        filename = "{}/first/" + str(code) + ".ces".format(config["file_path"])
        
        Write('write', filename, self.first)

    def build(self):
        self.first = {}

        self.first["type"] = b'FD'
        self.first["padding1"] = u8(0) * 2
        self.first["id1"] = u32(code) # country code
        self.first["id2"] = u32(0)
        self.first["padding2"] = u8(0) * 12
        self.first["padding3"] = u8(0xFF) * 8
        self.first["fdtag"] = b'FD'
        self.first["fdtagsize"] = u16(32)
        self.first["serveractive"] = u32(1)
        self.first["unk1"] = u32(0x96000001)
        self.first["unk2"] = u32(0x41004100)
        self.first["unk3"] = u32(0x41004100)
        self.first["unk4"] = u32(0x41004100)
        self.first["unk5"] = u32(0x41004100)
        self.first["unk6"] = u32(0x41004100)

class Write():
    def __init__(self, mode, filename, data):
        self.filename = filename
        self.data = data
        if mode == 'append': self.mode = 'ab' #append adds to existing data, write clears and overwrites it all
        elif mode == 'write': self.mode = 'wb'
        with open(self.filename[:-3] + 'dec', self.mode) as f: #writes uncompressed and unencrypted data to .dec
            for v in self.data.values():
                f.write(v)

        self.compress()
        self.encrypt()
        self.hmac()
        self.write()

    def compress(self):
        with open(self.filename[:-3] + 'dec', 'rb') as decfile:
            self.decfile = decfile.read()

        with open(self.filename, 'wb') as writef:
            writef.write(self.decfile)

        subprocess.call(["{}/lzss".format(config["lzss_path"]), "-evf", self.filename])

    def encrypt(self):
        subprocess.call(["openssl", "enc", "-aes-128-cbc", "-e", "-in", self.filename, "-out", self.filename + "1", "-K", "8D22A3D808D5D072027436B6303C5B50", "-iv", "BE5E548925ACDD3CD5342E08FB8ABFEC"])

        with open(self.filename + "1", "rb") as readf:
            self.processed = readf.read()

        os.remove(self.filename + "1")
        
    def hmac(self):
        self.sign = binascii.unhexlify("4CC08FA141DE2537AAA52B8DACD9B56335AFE467")
        self.digester = hmac.new(self.sign, self.processed, hashlib.sha1)
        self.hmacsha1 = self.digester.digest()

    def write(self):
        with open(self.filename, "wb") as writef:
            writef.write(b'MC')
            writef.write(u16(1))
            writef.write(self.hmacsha1)
            writef.write(self.processed)

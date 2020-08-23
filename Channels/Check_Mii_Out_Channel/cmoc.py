import binascii
import hashlib
import hmac
import os
import struct
import subprocess
import sys
import nlzss
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from json import load
from base64 import b64encode, b64decode
import lz4.block
from random import randint
from datetime import datetime
from time import mktime
import sentry_sdk
from miikaitai import Mii

with open("/var/rc24/File-Maker/Channels/Check_Mii_Out_Channel/config.json", "r") as f:
        config = load(f)

sentry_sdk.init(config["sentry_url"])

def decToEntry(num: int) -> str: #takes decimal int, outputs 12 digit entry number string
	num ^= ((num << 0x1E) ^ (num << 0x12) ^ (num << 0x18)) & 0xFFFFFFFF
	num ^= (num & 0xF0F0F0F) << 4
	num ^= (num >> 0x1D) ^ (num >> 0x11) ^ (num >> 0x17) ^ 0x20070419

	crc = (num >> 8) ^ (num >> 24) ^ (num >> 16) ^ (num & 0xFF) ^ 0xFF
	if 232 < (0xd4a50fff < num) + (crc & 0xFF):
		crc &= 0x7F

	crc &= 0xFF
	return str(int((format(crc, '08b') + format(num, '032b')), 2)).zfill(12)

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
	
def decodeMii(data): #takes compressed and b64 encoded data, returns binary mii data
	return(lz4.block.decompress(b64decode(data), uncompressed_size = 76))

def encodeMii(data): #takes binary mii data, returns compressed and b64 encoded data
	return(b64encode(lz4.block.compress(data, store_size=False)).decode())


def wii2studio(mii_file):
    try:
        orig_mii = Mii.from_file(mii_file)
    except:
        return ""

    makeup = {
        1: 1,
        2: 6,
        3: 9,
        9: 10
    }

    wrinkles = {
        4: 5,
        5: 2,
        6: 3,
        7: 7,
        8: 8,
        10: 9,
        11: 11
    }

    studio_mii = {}

    studio_mii["facial_hair_color"] = orig_mii.facial_hair_color
    studio_mii["beard_goatee"] = orig_mii.facial_hair_beard
    studio_mii["body_weight"] = orig_mii.body_weight
    studio_mii["eye_stretch"] = 3
    studio_mii["eye_color"] = orig_mii.eye_color + 8
    studio_mii["eye_rotation"] = orig_mii.eye_rotation
    studio_mii["eye_size"] = orig_mii.eye_size
    studio_mii["eye_type"] = orig_mii.eye_type
    studio_mii["eye_horizontal"] = orig_mii.eye_horizontal
    studio_mii["eye_vertical"] = orig_mii.eye_vertical
    studio_mii["eyebrow_stretch"] = 3
    studio_mii["eyebrow_color"] = orig_mii.eyebrow_color
    studio_mii["eyebrow_rotation"] = orig_mii.eyebrow_rotation
    studio_mii["eyebrow_size"] = orig_mii.eyebrow_size
    studio_mii["eyebrow_type"] = orig_mii.eyebrow_type
    studio_mii["eyebrow_horizontal"] = orig_mii.eyebrow_horizontal
    studio_mii["eyebrow_vertical"] = orig_mii.eyebrow_vertical
    studio_mii["face_color"] = orig_mii.face_color
    if orig_mii.facial_feature in makeup:
        studio_mii["face_makeup"] = makeup[orig_mii.facial_feature]
    else:
        studio_mii["face_makeup"] = 0
    studio_mii["face_type"] = orig_mii.face_type
    if orig_mii.facial_feature in wrinkles:
        studio_mii["face_wrinkles"] = wrinkles[orig_mii.facial_feature]
    else:
        studio_mii["face_wrinkles"] = 0
    studio_mii["favorite_color"] = orig_mii.favorite_color
    studio_mii["gender"] = orig_mii.gender
    if orig_mii.glasses_color == 0:
        studio_mii["glasses_color"] = 8
    elif orig_mii.glasses_color < 6:
        studio_mii["glasses_color"] = orig_mii.glasses_color + 13
    else:
        studio_mii["glasses_color"] = 0
    studio_mii["glasses_size"] = orig_mii.glasses_size
    studio_mii["glasses_type"] = orig_mii.glasses_type
    studio_mii["glasses_vertical"] = orig_mii.glasses_vertical
    studio_mii["hair_color"] = orig_mii.hair_color
    studio_mii["hair_flip"] = orig_mii.hair_flip
    studio_mii["hair_type"] = orig_mii.hair_type
    studio_mii["body_height"] = orig_mii.body_height
    studio_mii["mole_size"] = orig_mii.mole_size
    studio_mii["mole_enable"] = orig_mii.mole_enable
    studio_mii["mole_horizontal"] = orig_mii.mole_horizontal
    studio_mii["mole_vertical"] = orig_mii.mole_vertical
    studio_mii["mouth_stretch"] = 3
    if orig_mii.mouth_color < 4:
        studio_mii["mouth_color"] = orig_mii.mouth_color + 19
    else:
        studio_mii["mouth_color"] = 0
    studio_mii["mouth_size"] = orig_mii.mouth_size
    studio_mii["mouth_type"] = orig_mii.mouth_type
    studio_mii["mouth_vertical"] = orig_mii.mouth_vertical
    studio_mii["beard_size"] = orig_mii.facial_hair_size
    studio_mii["beard_mustache"] = orig_mii.facial_hair_mustache
    studio_mii["beard_vertical"] = orig_mii.facial_hair_vertical
    studio_mii["nose_size"] = orig_mii.nose_size
    studio_mii["nose_type"] = orig_mii.nose_type
    studio_mii["nose_vertical"] = orig_mii.nose_vertical

    mii_data = b""
    n = r = 256
    mii_data += binascii.hexlify(u8(0))
    for v in studio_mii.values():
        eo = (7 + (v ^ n)) % 256
        n = eo
        mii_data += binascii.hexlify(u8(eo))

    return "https://studio.mii.nintendo.com/miis/image.png?data=" + mii_data.decode("utf-8") + "&type=face&width=512&instanceCount=1"

class ResetList(): #removes all miis from a list
	def __init__(self, list_type):
		if list_type == b'SL': filename = 'spot_list.ces'
		elif list_type == b'PL': filename = 'pop_list.ces'
		elif list_type == b'RL': filename = 'bargain_list.ces'
		elif list_type == b'NL': filename = 'new_list01.ces'
		elif list_type == b'RL': filename = 'bargain_list01.ces'

		else: raise ValueError('Invalid list type!')
		filename = '{}/150/{}'.format(config["file_path"], filename)

		self.list_type = list_type
		self.mii = {}
		self.reset()
		Write('write', filename, self.mii)

	def reset(self):
		self.mii['list_type'] = self.list_type
		self.mii['padding1'] = u8(0) * 2
		self.mii['countrycode'] = u32(150)
		if self.list_type in [b'NL', b'RL']:
			self.mii['padding2'] = u32(1) #same int as new_list01, 02 etc.
			self.mii['padding3'] = u32(0) * 4
		else:
			self.mii['padding2'] = u32(0) * 5
			
		self.mii['end_header'] = b'\xFF\xFF\xFF\xFF'
		self.mii['pn_tag'] = b'PN'
		self.mii['pn_size'] = u16(12)
		self.mii['unk1'] = u32(1)
		self.mii['mii_count'] = u32(0)


class AddMii(): #adds mii to specified list_type. used for static .ces lists
	def __init__(self, entryno, list_type, miidata, popularity, initials, country, craftsno, artisandata): #add entryno param once the database is ready
		
		if list_type == b'SL': filename = 'spot_list.ces'
		elif list_type == b'PL': filename = 'pop_list.ces'
		elif list_type == b'RL': filename = 'bargain_list.ces'
		elif list_type == b'NL': filename = 'new_list01.ces'
		elif list_type == b'RL': filename = 'bargain_list01.ces'
		else: raise ValueError('Invalid list type!')
		filename = '{}/150/{}'.format(config["file_path"], filename)

		if len(initials.decode('utf-8')) == 1: initials += b'\x00'
		
		with open(filename[:-3] + 'dec', 'rb+') as file: 
			index = (int.from_bytes(file.read()[40:44], byteorder='big')) + 1 #gets the current mii count and index in PN, and increases it
			file.seek(40) #goes to 40th byte where the mii count begins
			file.write(u32(index))
	   
		self.list_type = list_type #list type must be SL, NL, RL, or PL in bytes format
		self.index = index #used for mii count in PN section. mii and its artisan must have this same number
		self.entryno = entryno #unique entry number per mii. if two or more miis on the list have the same entry number, none of them will show
		self.miidata = miidata #mii binary data WITHOUT its crc16 at the end
		if popularity > 28: popularity = 28 #28 is the max popularity value possible on the client's side
		self.popularity = popularity #must be a binary hexadecimal with the popularity value
		self.initials = initials #if it doesn't have a second initial, replace it with 0x00
		self.country = country
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
		self.mii['unk2'] = u16(0)
		self.mii['popularity'] = self.popularity
		self.mii['unk3'] = u8(0)
		self.mii['skill'] = u16(0)
		self.mii['initials'] = self.initials 
		self.mii['pc_tag'] = b'PC'
		self.mii['pc_size'] = u16(96)
		self.mii['creator_index'] = u32(self.index)
		self.mii['creator_number'] = u32(self.craftsno)
		self.mii['mii_artisan'] = self.artisandata
		self.mii['unk4'] = u8(0)
		self.mii['master_artisan'] = u8(0)
		self.mii['unk5'] = u8(0)
		self.mii['unk6'] = u16(0)
		self.mii['country_code2'] = u8(self.country)
		self.mii['unk7'] = u16(0)

class OwnSearch(): #creates an ownsearch response given a craftsno
	def __init__(self): #__init__ cannot return any values, so SearchList.build() must be used in the driver
		self.miilist = []

	def build(self, miis, craftsno): #must be sent a 2 dimensional array containing entryno, initials likes, skill, country, miidata, artisandata and master artisan flag
		
		count = int(len(miis))
		beginning = bytes.fromhex('4F53000000000000') + u32(craftsno) + bytes.fromhex('000000000000000000000000FFFFFFFFFFFFFFFF')
		pntag = bytes.fromhex('504E000C00000001') + u32(count)
		self.header = beginning + pntag
		self.craftsno = craftsno
		
		for entry in miis:
			if len(entry[1]) == 1:
				initial = entry[1].encode() + b'\x00' #add 0x00 to 1 letter initials
			else:
				initial = entry[1].encode()

			miidata = decodeMii(entry[5]) #mii data is lz4 compressed and base64 encoded when retrieved from the SQL database

			self.mii = {}
			self.mii['pm_tag'] = b'PM'
			self.mii['pm_size'] = u16(96)
			self.mii['mii_index'] = u32(miis.index(entry) + 1) #add 1 to the index because it can't start at 0
			self.mii['entry_number'] = u32(entry[0]) 
			self.mii['mii'] = miidata
			self.mii['unk2'] = u16(0)

			if entry[2] > 28: #28 is the max popularity value possible on the client's side
				self.mii['popularity'] = u8(28)
			else:
				self.mii['popularity'] = u8(entry[2])

			self.mii['unk3'] = u8(0)
			self.mii['skill'] = u16(entry[3])
			self.mii['initials'] = initial

			self.miilist += self.mii.values()

		self.miilist.insert(0, self.header) #inserts the header before all the miis
		return self.miilist #returns a 2 dimensional array containing the header and all the miis

class Search(): #creates a search or namesearch response given an entryno
	def __init__(self): #__init__ cannot return any values, so SearchList.build() must be used in the driver
		self.miilist = []
	
	def build(self, searchtype, miis, entryno, craftsno): #must be sent a 2 dimensional array containing entryno, initials likes, skill, country, miidata, artisandata and master artisan flag
		#searchtype must be SR or NS
		count = int(len(miis))
		beginning = bytes.fromhex('000000000000') + u32(entryno) + bytes.fromhex('000000000000000000000000FFFFFFFFFFFFFFFF')
		pntag = bytes.fromhex('504E000C00000001') + u32(count)
		self.header = searchtype.encode() + beginning + pntag
		self.craftsno = craftsno
		
		for entry in miis:
			if len(entry[1]) == 1:
				initial = entry[1].encode() + b'\x00' #add 0x00 to 1 letter initials
			else:
				initial = entry[1].encode()

			miidata = decodeMii(entry[5]) #mii data is lz4 compressed and base64 encoded when retrieved from the SQL database
			artisan = decodeMii(entry[6])
			craftsno = entry[7]

			self.mii = {}
			self.mii['pm_tag'] = b'PM'
			self.mii['pm_size'] = u16(96)
			self.mii['mii_index'] = u32(miis.index(entry) + 1) #add 1 to the index because it can't start at 0
			self.mii['entry_number'] = u32(entry[0]) 
			self.mii['mii'] = miidata
			self.mii['unk2'] = u16(0)

			if entry[2] > 28: #28 is the max popularity value possible on the client's side
				self.mii['popularity'] = u8(28)
			else:
				self.mii['popularity'] = u8(entry[2])

			self.mii['unk3'] = u8(0)
			self.mii['skill'] = u16(entry[3])
			self.mii['initials'] = initial
			self.mii['pc_tag'] = b'PC'
			self.mii['pc_size'] = u16(96)
			self.mii['creator_index'] = u32(miis.index(entry) + 1)
			self.mii['creator_number'] = u32(craftsno)
			self.mii['mii_artisan'] = artisan
			self.mii['unk4'] = u8(0)
			self.mii['master_artisan'] = u8(entry[8])
			self.mii['unk5'] = u8(0)
			self.mii['unk6'] = u16(0)
			self.mii['country_code2'] = u8(entry[4])
			self.mii['unk7'] = u16(0)
			self.miilist += self.mii.values()

		self.miilist.insert(0, self.header) #inserts the header before all the miis
		return self.miilist #returns a 2 dimensional array containing the header and all the miis



class QuickList(): #returns a temporary unencrypted mii list for CGI scripts like ownsearch.cgi
	def __init__(self): #__init__ cannot return any values, so QuicKList.build() must be used in the driver
		self.miilist = []
		self.artisanlist = []

	def build(self, list_type, miis): #must be sent a 2 DIMENSIONAL array with each entry containing entryno, initials likes, skill, country, miidata, artisandata, craftsno and master artisan flag
		#list_type can be SL, NL, RL, PL etc.
		list_type = list_type.upper()			
		if list_type in ['SL', 'RL', 'PL', 'CL']: countrytag = u32(150) #this can be changed if we decide to use regional sorting

		count = int(len(miis))
		list_type = list_type.encode()

		beginning = bytes.fromhex('0000') + countrytag + bytes.fromhex('0000000000000000000000000000000000000000FFFFFFFF')

		pntag = bytes.fromhex('504E000C00000001') + u32(count)
		self.header = list_type + beginning + pntag
		
		for entry in miis:
			if len(entry[1]) == 1:
				initial = entry[1].encode() + b'\x00' #add 0x00 to 1 letter initials
			else:
				initial = entry[1].encode()

			miidata = decodeMii(entry[5]) #mii data is lz4 compressed and base64 encoded when retrieved from the SQL database
			artisan = decodeMii(entry[6])

			self.mii = {}
			self.mii['pm_tag'] = b'PM'
			self.mii['pm_size'] = u16(96)
			self.mii['mii_index'] = u32(miis.index(entry) + 1)
			self.mii['entry_number'] = u32(entry[0]) 
			self.mii['mii'] = miidata
			self.mii['unk2'] = u16(0)

			if entry[2] > 28: #28 is the max popularity value possible on the client's side
				self.mii['popularity'] = u8(28)
			else:
				self.mii['popularity'] = u8(entry[2])

			self.mii['unk3'] = u8(0)
			self.mii['skill'] = u16(entry[3])
			self.mii['initials'] = initial
			self.mii['pc_tag'] = b'PC'
			self.mii['pc_size'] = u16(96)
			self.mii['creator_index'] = u32(miis.index(entry) + 1)
			self.mii['creator_number'] = u32(entry[7])
			self.mii['mii_artisan'] = artisan
			self.mii['unk4'] = u8(0)
			self.mii['master_artisan'] = u8(entry[8])
			self.mii['unk5'] = u8(0)
			self.mii['unk6'] = u16(0)
			self.mii['country_code2'] = u8(entry[4])
			self.mii['unk7'] = u16(0)
			self.miilist += self.mii.values()

		self.miilist.insert(0, self.header) #inserts the header before all the miis

		data = b''
		for entry in self.miilist:
			data += entry

		return data #returns the formatted data, ready to be compressed and encrypted for CMOC

	def infoBuild(self, craftsno, entryno, miidata, initial, master, popularity, ranking): #must be sent craftsno, entryno, most popular mii, initials, master artisan flag, popularity and ranking

		self.header = bytes.fromhex('494E000000000000') + u32(int(craftsno)) + bytes.fromhex('000000000000000000000000FFFFFFFFFFFFFFFF')
		miidata = decodeMii(miidata)
		if len(initial) == 1:
			initial = initial.encode() + b'\x00' #add 0x00 to 1 letter initials
		else:
			initial = initial.encode()

		if int(popularity) > 28: popularity = 28 #28 is the max popularity value possible on the client's side

		self.mii = {}
		self.mii['header'] = self.header
		self.mii['im_tag'] = b'IM'
		self.mii['im_size'] = u16(96)
		self.mii['unk1'] = u32(1)
		self.mii['entry_number'] = u32(int(entryno))
		self.mii['mii'] = miidata
		self.mii['unk2'] = u16(1)
		self.mii['unk3'] = u32(0)
		self.mii['initials'] = initial
		self.mii['in_tag'] = b'IN'
		self.mii['in_size'] = u16(24)
		self.mii['unk4'] = u32(1)
		self.mii['unk5'] = u32(1)
		self.mii['unk6'] = u32(1)
		self.mii['master'] = u16(int(master))
		self.mii['popularity'] = u8(int(popularity))
		self.mii['unk7'] = u8(0)

		if int(ranking) == 0:
			self.mii['ranking'] = u8(0)
		else:
			self.mii['ranking'] = u8(int(ranking)+1)

		self.mii['unk8'] = u16(0)
		self.mii['unk9'] = u8(1)
		self.miilist += self.mii.values()

		data = b''
		for entry in self.miilist:
			data += entry

		return data #returns the formatted data, ready to be compressed and encrypted for CMOC

	def popcraftsBuild(self, artisans): #same as above but formatted for popcrafts_list
		#artisans must be 2 dimensional array containing craftsno, artisandata, master artisan flag, and popularity
		#master artisan also stores the new mii flag: 0 - no master artisan, 1 - master artisan, 2 - new mii, 3 - new mii and master artisan
		month = int(datetime.now().month)
		day = int(datetime.now().day)
		count = int(len(artisans))
		list_type = b'CL'
		countrytag = u32(150)
		beginning = bytes.fromhex('0000') + countrytag + bytes.fromhex('0000000000000000000000000000000000000000FFFFFFFF')
		self.header = list_type + beginning
		
		for entry in artisans:

			self.artisan = {}
			self.artisan['rc_tag'] = b'RC'
			self.artisan['pm_size'] = u16(96)
			self.artisan['artisan_index'] = u32(artisans.index(entry) + 1)
			self.artisan['craftsno'] = u32(entry[0]) 
			self.artisan['artisan'] = decodeMii(entry[1])
			self.artisan['unk1'] = u8(0)
			self.artisan['master_artisan'] = u8(entry[2])
			if entry[3] > 28: #28 is the max popularity value possible on the client's side
				self.artisan['popularity'] = u8(28)
			else:
				self.artisan['popularity'] = u8(entry[3])
			self.artisan['unk2'] = u8(0)
			self.artisan['country'] = u16(entry[4])
			self.artisan['unk3'] = u16(0)
			self.artisan['rk_tag'] = b'RK'
			self.artisan['rk_size'] = u16(16)
			self.artisan['unk4'] = u32(1)
			self.artisan['rk_index'] = u32(artisans.index(entry) + 1)
			self.artisan['day'] = u16(day)
			self.artisan['month'] = u8(month)
			self.artisan['unk5'] = u8(0)

			self.artisanlist += self.artisan.values()

		self.artisanlist.insert(0, self.header) #inserts the header before all the miis

		data = b''
		for entry in self.artisanlist:
			data += entry

		return data #returns the formatted data, ready to be compressed and encrypted for CMOC



class NumberedList(): #returns a temporary unencrypted mii list for new_list and bargain_list
	def __init__(self): 
		self.miilist = []

	def build(self, list_type, miis): #must be sent a 2 DIMENSIONAL array with each entry containing entryno, initials likes, skill, country, miidata, artisandata, craftsno and master artisan flag
		#list_type can be NL1, NL2, NL3, RL1, RL2, RL3 etc.

		list_number = u32(int(list_type[2:])) #get the number after NL or RL
		list_type = list_type[:2].upper() #remove the number from NL or RL		

		countrytag = u32(150)
		count = int(len(miis))
		list_type = list_type.encode()
		beginning = bytes.fromhex('0000') + countrytag + list_number + bytes.fromhex('00000000000000000000000000000000FFFFFFFF')

		pntag = bytes.fromhex('504E000C00000001') + u32(count)

		self.header = list_type + beginning + pntag
		
		for entry in miis:
			if len(entry[1]) == 1:
				initial = entry[1].encode() + b'\x00' #add 0x00 to 1 letter initials
			else:
				initial = entry[1].encode()

			miidata = decodeMii(entry[5]) #mii data is lz4 compressed and base64 encoded when retrieved from the SQL database
			artisan = decodeMii(entry[6])

			self.mii = {}
			self.mii['pm_tag'] = b'PM'
			self.mii['pm_size'] = u16(96)
			self.mii['mii_index'] = u32(miis.index(entry) + 1)
			self.mii['entry_number'] = u32(entry[0]) 
			self.mii['mii'] = miidata
			self.mii['unk2'] = u16(0)
			if entry[2] > 28: #28 is the max popularity value possible on the client's side
				self.mii['popularity'] = u8(28)
			else:
				self.mii['popularity'] = u8(entry[2])
			self.mii['unk3'] = u8(0)
			self.mii['skill'] = u16(entry[3])
			self.mii['initials'] = initial
			self.mii['pc_tag'] = b'PC'
			self.mii['pc_size'] = u16(96)
			self.mii['creator_index'] = u32(miis.index(entry) + 1)
			self.mii['creator_number'] = u32(entry[7])
			self.mii['mii_artisan'] = artisan
			self.mii['unk4'] = u8(0)
			self.mii['master_artisan'] = u8(entry[8])
			self.mii['unk5'] = u8(0)
			self.mii['unk6'] = u16(0)
			self.mii['country_code2'] = u8(entry[4])
			self.mii['unk7'] = u16(0)
			self.miilist += self.mii.values()

		self.miilist.insert(0, self.header) #inserts the header before all the miis

		data = b''
		for entry in self.miilist:
			data += entry

		return data #returns the formatted data, ready to be compressed and encrypted for CMOC

class WSR(): #returns an unencrypted mii list for wii sports resort
	def __init__(self):
		self.miilist = []

	def build(self, miis): #requires 2 dimensional array containing initials, miidata, artisan data, and entryno
		open = int(mktime(datetime.utcnow().timetuple())) - 946684800 #current time since 1/1/2000 in seconds
		close = int(mktime(datetime.utcnow().timetuple())) - 946512000 #current time since 1/1/2000 in seconds + 48 hours
		self.header = u32(open) + u32(close) + bytes.fromhex('000041A0000000A864000000000000000000000000000000')
		for entry in miis:
			if len(entry[0]) == 1:
				initial = entry[0].encode() + b'\x00' #add 0x00 to 1 letter initials
			else:
				initial = entry[0].encode()

			miidata = decodeMii(entry[1]) #mii data is lz4 compressed and base64 encoded when retrieved from the SQL database
			artisan = decodeMii(entry[2])

			self.mii = {}
			self.mii['index'] = u8(miis.index(entry) + 1)
			self.mii['initials'] = initial
			self.mii['country_code'] = u8(49) #country code doesn't matter or change anything
			self.mii['unk1'] = u32(0)
			#self.mii['entry_number1'] = u32(0) #this is actually a u64 for the 12 digit code
			#self.mii['entry_number2'] = u32(0) #except nobody knows how to convert it
			self.mii['entry_number'] = int(decToEntry(entry[3])).to_bytes(8, 'big')
			self.mii['miidata'] = miidata
			self.mii['mii_artisan'] = artisan

			self.miilist += self.mii.values()

		self.miilist.insert(0, self.header) #inserts the header before all the miis

		data = b''
		for entry in self.miilist:
			data += entry
		print(len(data))
		return(data)


class ConDetail():
	def build(self, id, start, end, status, entrycount, topic, description):
		def conStatus(status): #the status flag in condetail is strange and requires a number that determines whether its open, judging, or showing results
			if status == 'open':
				return(2)

			elif status == 'judging':
				return(8)

			elif status == 'results':
				return(32)

			else:
				print('Invalid status:', status)
				exit()

		self.condetail = {}
		self.condetail["type"] = b'CD'
		self.condetail["padding1"] = u8(0) * 2
		self.condetail["id1"] = u32(id)
		self.condetail["id2"] = u32(1)
		self.condetail["padding2"] = u32(0) * 2
		self.condetail["start"] = u32(start)
		self.condetail["end"] = u32(end)
		self.condetail["padding3"] = bytes.fromhex('FFFFFFFF')
		self.condetail["cdtag"] = b'CD'
		self.condetail["cdtagsize"] = u16(136)
		self.condetail["id3"] = u32(1)
		self.condetail["id4"] = u32(id)
		self.condetail["status"] = u8(conStatus(status))
		self.condetail["worldwide"] = u8(1)
		self.condetail["padding4"] = u16(0)
		self.condetail["entrycount"] = u32(entrycount)
		self.condetail["padding5"] = u32(0) * 5
		self.condetail["topic"] = topic[:16].encode()
		self.condetail["padding6"] = u8(0) * (32 - len(topic))
		self.condetail["description"] = description[:64].encode()
		self.condetail["padding7"] = u8(0) * (64 - len(description))

		data = b''
		for entry in self.condetail.values():
			data += entry
		return(data)

class ConInfo():
	def __init__(self):
		self.conlist = []

	def build(self, contests): #must be sent a 2 DIMENSIONAL array with each entry containing contest id and status
		def conStatus(status): #the status flag in condetail is strange and requires a number that determines whether its open, judging, or showing results
			if status == 'open':
				return(2)

			elif status == 'judging':
				return(8)

			elif status == 'results':
				return(32)

			else:
				print('Invalid status:', status)
				exit()
		
		
		self.header = bytes.fromhex('434900000000009600000000000000000000000000000000FFFFFFFFFFFFFFFF')

		for entry in contests:
			self.contest = {}
			self.contest['ci_tag'] = b'CI'
			self.contest['ci_size'] = u16(32)
			self.contest['contest_index'] = u32(contests.index(entry) + 1)
			self.contest['contest_id'] = u32(entry[0]) 
			self.contest['status'] = u8(conStatus(entry[1]))
			self.contest['worldwide'] = u8(1)
			self.contest['padding1'] = u8(0) * 18
			self.conlist += self.contest.values()

		self.conlist.insert(0, self.header) #inserts the header before all the contests

		data = b''
		for entry in self.conlist:
			data += entry

		return data #returns the formatted data, ready to be compressed and encrypted for CMOC

class EntryList(): #EntryList has no PN tag. each entry_list file has exactly 10 miis
	def build(self, id, miis): #must be sent contest ID and a 2 DIMENSIONAL array with each entry containing craftsno and miidata
		pages = []
		total = (len(miis) - len(miis)%10)//10 #removes the remainder to give each list exactly 10 miis (make sure to return randomized query from the database)
		for listNumber in range(total): 
			self.header = bytes.fromhex('454C0000') + u32(id) + u32(listNumber + 1) + bytes.fromhex('00000000000000000000000000000000FFFFFFFF')
			self.miilist = []

			for entry in range(1, 11):
				miidata = decodeMii(miis[entry + (listNumber * 10) - 1][1]) #600 IQ
				self.mii = {}
				self.mii['cm_tag'] = b'CM'
				self.mii['cm_size'] = u16(88)
				self.mii['mii_index'] = u32(entry + (listNumber * 10))
				self.mii['craftsno'] = u32(miis[entry + (listNumber * 10) - 1][0])
				self.mii['mii'] = miidata
				self.miilist += self.mii.values()
			
			self.miilist.insert(0, self.header) #inserts the header before all the miis
			
			data = b''
			for entry in self.miilist:
				data += entry

			pages.append((data))

		return pages #returns 2 dimensional array with the individual entry_list pages

class BestList(): #similar to a regular CMOC list, but miis have no initials, skill, or popularity
	def build(self, id, miis): #must be sent contest ID and a 2 DIMENSIONAL array with each entry containing entryno, craftsno, miidata, artisandata, country, and master artisan flag
		
		header = bytes.fromhex('424C0000') + u32(id) + bytes.fromhex('0000000000000000000000000000000000000000FFFFFFFF')
		cntag = bytes.fromhex('434E000C00000001') + u32(len(miis))
		self.header = header + cntag
		self.miilist = []

		for entry in miis:
			miidata = decodeMii(entry[2]) #mii data is base64 encoded when retrieved from the SQL database
			artisan = decodeMii(entry[3])

			self.mii = {}
			self.mii['cm_tag'] = b'CM'
			self.mii['cm_size'] = u16(88)
			self.mii['mii_index'] = u32(miis.index(entry) + 1)
			self.mii['entry_number'] = u32(entry[0]) 
			self.mii['mii'] = miidata
			self.mii['cc_tag'] = b'CC'
			self.mii['cc_size'] = u16(96)
			self.mii['creator_index'] = u32(miis.index(entry) + 1)
			self.mii['creator_number'] = u32(entry[1])
			self.mii['mii_artisan'] = artisan
			self.mii['unk4'] = u8(0)
			self.mii['master_artisan'] = u8(entry[5])
			self.mii['unk5'] = u8(0)
			self.mii['unk6'] = u16(0)
			self.mii['country_code'] = u8(entry[4])
			self.mii['unk7'] = u16(miis.index(entry) + 1) #dookie
			self.miilist += self.mii.values()

		self.miilist.insert(0, self.header) #inserts the header before all the miis

		data = b''
		for entry in self.miilist:
			data += entry

		return data #returns the formatted data, ready to be compressed and encrypted for CMOC

class ConResult(): #returns unencrypted list for conresult.cgi
	def __init__(self):
		self.miilist = []
	
	def build(self, id, miis): #must be sent contest ID and a 2 dimensional array containing craftsno and ranking
		self.header = bytes.fromhex('43520000') + u32(id) + bytes.fromhex('00000000000000000000000000000000FFFFFFFFFFFFFFFF')
		
		for i in range(len(miis)):
			self.mii = {}
			self.mii['cc_tag'] = b'CC'
			self.mii['cc_size'] = u16(96)
			self.mii['cc_index'] = u32(i + 1) #add 1 to the index because it can't start at 0
			self.mii['craftsno'] = u32(miis[i][0]) 
			self.mii['padding1'] = u8(0) * 82 #mii data can go here, but it isn't even needed
			self.mii['ranking'] = u8(miis[i][1] * 10)
			self.mii['unk1'] = u8(0)
			self.miilist += self.mii.values()

		self.miilist.insert(0, self.header) #inserts the header before all the miis
		data = b''
		for entry in self.miilist:
			data += entry

		return data

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

class Prepare(): #this is only used to compress and encrypt data by external scripts. any data can be used with this

    def __init__(self):
        self.filename = '/tmp/TMP{}.ces'.format(str(randint(1, 1000000)))

    def prepare(self, data): #takes only data and doesn't write it anywhere. returns the final data
        prepared = b''

        with open(self.filename, 'wb') as tempfile:
            tempfile.write(data)

        self.compress()
        self.encrypt()
        self.hmac()

        prepared += b'MC'
        prepared += u16(1)
        prepared += self.hmacsha1
        prepared += self.processed
        os.remove(self.filename)

        return prepared

    def compress(self):
        nlzss.encode_file(self.filename, self.filename)

    def encrypt(self):
        aes = AES.new(bytes.fromhex('8D22A3D808D5D072027436B6303C5B50'), AES.MODE_CBC, bytes.fromhex('BE5E548925ACDD3CD5342E08FB8ABFEC'))
        with open(self.filename, "rb") as readf:
            self.processed = aes.encrypt(pad(readf.read(), 16))
        
    def hmac(self):
        self.sign = bytes.fromhex("4CC08FA141DE2537AAA52B8DACD9B56335AFE467")
        self.digester = hmac.new(self.sign, self.processed, hashlib.sha1)
        self.hmacsha1 = self.digester.digest()

    def write(self):
        with open(self.filename, "wb+") as writef:
            writef.write(b'MC')
            writef.write(u16(1))
            writef.write(self.hmacsha1)
            writef.write(self.processed)

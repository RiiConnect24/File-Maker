import binascii
import os
import rsa
import struct
import subprocess
import sys
from config import *

def u8(data):
	return struct.pack(">B", data)


def u16(data):
	return struct.pack(">H", data)


def u32(data):
	return struct.pack(">I", data)


def u32_littleendian(data):
	return struct.pack("<I", data)

if (len(sys.argv) != 4):
	print "Usage: sign.py <mode> <input file> <output file>"
	print "\n"
	print "Mode can either be set to dec (not-encrypted file) or enc (encrypted file)."
	sys.exit(1)

input_file = sys.argv[2]
input_file2 = sys.argv[2] + "2"
output_file = sys.argv[3]

if os.path.exists(output_file):
	os.remove(output_file)

if (sys.argv[1] == "dec"):
	with open(input_file, "rb") as source_file:
		crc32 = format(binascii.crc32(source_file.read()) & 0xFFFFFFFF, '08x')

	filesize = u32(os.path.getsize(input_file) + 12)

	with open(input_file, "rb") as source_file:
		with open(input_file2, "w+") as dest_file:
			read = source_file.read()
			version = u32(0)
			dest_file.write(version)
			dest_file.write(filesize)
			dest_file.write(binascii.unhexlify(crc32))
			dest_file.write(read)

	lz77 = subprocess.call([lzss_path + "lzss", "-evf", input_file2, output_file])

	with open(output_file, "rb") as source_file:
		read = source_file.read()

	with open(rsa_key_path, "rb") as source_file:
		private_key_data = source_file.read()

	private_key = rsa.PrivateKey.load_pkcs1(private_key_data, "PEM")

	signature = rsa.sign(read, private_key, "SHA-1")

	with open(output_file, "w+") as dest_file:
		dest_file.write(binascii.unhexlify(hex(int(0))[2:].zfill(128)))
		dest_file.write(signature)
		dest_file.write(read)

	os.remove(input_file)

elif (sys.argv[1] == "enc"):
	with open(input_file, "rb") as source_file:
		read = source_file.read()

	with open(rsa_key_path, "rb") as source_file:
		private_key_data = source_file.read()

	private_key = rsa.PrivateKey.load_pkcs1(private_key_data, "PEM")

	signature = rsa.sign(read, private_key, "SHA-1")

	with open(aes_key_path, "rb") as source_file:
		key_data = binascii.hexlify(source_file.read())

	iv_data = binascii.b2a_hex(os.urandom(16))

	encrypt_aes = subprocess.call(["openssl", "enc", "-aes-128-ofb", "-in", input_file, "-out", output_file, "-K", key_data, "-iv", iv_data])

	with open(output_file, "rb") as source_file:
		read = source_file.read()

	with open(output_file, "w+") as dest_file:
		dest_file.write(binascii.unhexlify("574332340000000100000000010000000000000000000000000000000000000000000000000000000000000000000000"))
		dest_file.write(binascii.unhexlify(iv_data))
		dest_file.write(signature)
		dest_file.write(read)

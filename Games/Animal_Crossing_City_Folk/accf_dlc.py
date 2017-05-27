import binascii
import collections
import locale
import os
import struct
import subprocess
import sys
import textwrap

"""This will pack the integers."""

def u8(data):
    return struct.pack(">B", data)


def u16(data):
    return struct.pack(">H", data)


def u32(data):
    return struct.pack(">I", data)


def u32_littleendian(data):
    return struct.pack("<I", data)

def main():
	print "Animal Crossing: City Folk DLC Maker, by Larsenv."

	print "\n"

	item_bin = make_item_bin()
	write = write_dictionary()

def item_name(language):
	if (language == "Korean" or "Japanese"):
		name = raw_input("Please enter the item name in %s: " % language).decode(sys.stdin.encoding or locale.getpreferredencoding(True))

		return binascii.unhexlify(binascii.hexlify(name.encode("utf-16be")).ljust(68, "0"))
	else:
		while (name > 17):
			name = raw_input("Please enter the item name in %s: " % language)

		return binascii.unhexlify(binascii.hexlify(name.decode("utf-8").encode("utf-16be")).ljust(68, "0"))

"""This is a function used to count offsets."""

def offset_count():
	return sum(len(values) for dictionary in dictionaries for values in dictionary.values() if values)

dictionaries = []

"""Make the item.bin."""

def make_item_bin():
	item = collections.OrderedDict()
	dictionaries.append(item)

	item["fourcc"] = "BITM" # FourCC.
	item["bells"] = u32(int(raw_input("Please enter a number of Bells this item costs: "))) # The number of Bells this item costs.
	item["item_code"] = binascii.unhexlify(raw_input("Please enter an item code: ")) # Code for the item.
	item["icon_code"] = u16(int(raw_input("Please enter an icon code: "))) # Icon Code for the item.
	item["unknown_1"] = u32(0) # Unknown.
	item["unknown_2"] = u16(5889) # Unknown.

	print "\n"

	item["item_name_japanese"] = item_name("Japanese") # The name of the item in Japanese.
	item["item_name_north_american_english"] = item_name("North American English") # The name of the item in North American English.
	item["item_name_north_american_spanish"] = item_name("North American Spanish") # The name of the item in North American Spanish.
	item["item_name_north_american_french"] = item_name("North American French") # The name of the item in North American French.
	item["item_name_european_english"] = item_name("European English") # The name of the item in European English.
	item["item_name_european_german"] = item_name("European German") # The name of the item in European German.
	item["item_name_european_italian"] = item_name("European Italian") # The name of the item in European Italian.
	item["item_name_european_spanish"] = item_name("European Spanish") # The name of the item in European Spanish.
	item["item_name_european_french"] = item_name("European French") # The name of the item in European French.
	item["item_name_korean"] = item_name("Korean") # The name of the item in Korean.

	item["unknown_3"] = binascii.unhexlify("38D61D65100000000064002B00000000049A0000005313104213131081031042123000000000") # Unknown.

	print "\n"

	file_name_brres = raw_input("Please enter the file name of the BRRES: ")

	compress_ash = subprocess.call(["wine", "ashcompress.exe", file_name_brres])

	with open(file_name_brres + ".ash", "rb") as source_file:
		item["ash_compressed_brres"] = source_file.read() # This contains the 3D model of the item.

	if (offset_count() > 8188):
		print "This item file's too big."

		sys.exit(1)

	item["padding"] = binascii.unhexlify("00") * (8188 - offset_count()) # Padding.

def make_letter():
	letter_english = letter_name("North American English", "Dear ", "RiiConnect24 Team", "./rvforestdl_us.d/ltrue")

def write_dictionary():
	open("item.bin", "w+")

	for dictionary in dictionaries:
        for values in dictionary.values():
            with open("item.bin", "a+") as dest_file:
                    dest_file.write(values)

	with open("item.bin", "a+") as dest_file:
		dest_file.write(binascii.unhexlify(subprocess.check_output(["perl", "crc32.pl"])[:8]))

main()

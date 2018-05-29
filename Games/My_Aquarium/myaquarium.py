#!/usr/bin/python
# -*- coding: utf-8 -*-

# ===========================================================================
# MY AQUARIUM - AQUARIUM ATTACHMENT GENERATOR
# VERSION 1.0
# AUTHORS: JOHN PANSERA
# ****************************************************************************
# Copyright (c) 2015-2018 RiiConnect24, and it's (Lead) Developers
# ===========================================================================

import binascii
import collections
import io
import struct

bytes = 0

print("My Aquarium Custom Attachment Generator")
print("By John Pansera / Version 1.0\n")


def u8(data):
    if data < 0 or data > 255:
        print("[+] Invalid Entry: %s" % data)
        exit()
    return struct.pack(">B", data)


def u16(data):
    if data < 0 or data > 65535:
        print("[+] Invalid Entry: %s" % data)
        exit()
    return struct.pack(">H", data)


def u32(data):
    if data < 0 or data > 4294967295:
        print("[+] Invalid Entry: %s" % data)
        exit()
    return struct.pack(">I", data)


def pad(amnt):
    buffer = ""
    for _ in range(amnt): buffer += "\0"
    return buffer


print("AQUARIUM SIZE")
print("0 - Small")
print("1 - Medium")
print("2 - Large")
print("\n")
aquarium_size = input('Enter Selection: ')
print("GLASS TYPE")
print("0 - Normal")
print("1 - Gift 1")
print("2 - Gift 2")
print("3 - Special Date 1")
print("4 - Special Date 2")
print("5 - Special Date 3")
print("\n")
glass_type = input('Enter Selection : ')
print("FLOOR TYPE")
print("0 - River Bed")
print("1 - Sand")
print("2 - White Sand")
print("3 - Gravel 1")
print("4 - Gravel 2")
print("\n")
floor_type = input('Enter Selection : ')
print("BACKGROUND TYPE")
print("0 - Underwater Theme")
print("1 - Emerald Theme")
print("2 - Coral Theme")
print("3 - Quiet Ocean Theme")
print("4 - Riverbed Theme")
print("\n")
background_type = input('Enter Selection : ')
print("LIGHT TYPE")
print("0 - Normal")
print("1 - Brightly Lit")
print("2 - Very Bright")
print("3 - Blue")
print("4 - Green")
print("5 - Orange")
print("6 - Spotted")
print("\n")
light_type = input('Enter Selection : ')
print("\nSPECIAL DATE 1")
specialdate1_month = input('Enter Month Number : ')
specialdate1_day = input('Enter Day Number : ')
print("\nSPECIAL DATE 2")
specialdate2_month = input('Enter Month Number : ')
specialdate2_day = input('Enter Day Number : ')
print("\nSPECIAL DATE 3")
specialdate3_month = input('Enter Month Number : ')
specialdate3_day = input('Enter Day Number : ')
print("\n")
print("NOTE: This script does not currently generate objects in the tank")

header = collections.OrderedDict()
header["unknown"] = u8(0)  # Version?
header["aquarium_size"] = u8(int(aquarium_size))
header["glass_type"] = u8(int(glass_type))
header["floor_type"] = u8(int(floor_type))
header["background_type"] = u8(int(background_type))
header["light_type"] = u8(int(light_type))
header["unknown_1"] = u16(0)
header["breeding_date_counter"] = u32(0)
header["unknown_date_counter"] = u32(0)
header["special_date_1_padding"] = u8(0)
header["special_date_1_month"] = u8(int(specialdate1_month))
header["special_date_1_day"] = u8(int(specialdate1_day))
header["special_date_1_padding_1"] = u8(0)
header["special_date_2_padding"] = u8(0)
header["special_date_2_month"] = u8(int(specialdate2_month))
header["special_date_2_day"] = u8(int(specialdate2_day))
header["special_date_2_padding_2"] = u8(0)
header["special_date_3_padding"] = u8(0)
header["special_date_3_month"] = u8(int(specialdate3_month))
header["special_date_3_day"] = u8(int(specialdate3_day))
header["special_date_3_padding_1"] = u8(0)

if input('Would you like to add fish? [y/n] ') is 'y':
    amnt = int(input('Enter amount of fish to add [MAX 15]: '))
    if amnt <= 15:
        print("\n")
        print("FISH SELECTION [0-39]")
        print("Note: There are 40 different types of fish, however there are more listed here (found in the game's files - they may or may not be able to be used)")
        print("01 Achilles Tang")
        print("02 Asian Arowana")
        print("03 Red Asian Arowana")
        print("04 Blueface Angelfish")
        print("05 Emperor Angelfish")
        print("06 Yellow Piranha")
        print("07 Freshwater Angelfish")
        print("08 Ocellaris Clownfish")
        print("09 Blue Jellyfish")
        print("10 Clown Killifish")
        print("11 Clown Loach")
        print("12 Pakistani Loach")
        print("13 Sea Angel")
        print("14 Golden Gourami")
        print("15 Dwarf Hawkfish")
        print("16 Humpback Grouper")
        print("17 Coral Grouper")
        print("18 Killifish")
        print("19 Papuan Jellyfish")
        print("20 Checkered Barb")
        print("21 Jellyfish Choukurage")
        print("22 Tinkeri Butterfly")
        print("23 Corydoras Narcissus")
        print("24 Flagtail Surgeonfish")
        print("25 Neon Tetra")
        print("26 Cardinal Tetra")
        print("27 Pastaza Corydoras")
        print("28 Red Lionfish")
        print("29 Lyretail Hogfish")
        print("30 Wrasse")
        print("31 Blue Gourami")
        print("32 Black Molly")
        print("33 Blue Grass Guppy")
        print("34 Red Grass Guppy")
        print("35 Blue Discus")
        print("36 Betta")
        print("37 Argentine Pearlfish")
        print("38 Moon Jellyfish")
        print("39 Spotted Green Puffer")
        print("40 Sea Horse")
        print("41 Rainbow Rockfish")
        print("42 Archerfish")
        print("43 Jaw Characin")
        print("44 White Spotted Cichlid")
        print("45 Rainbow Fish")
        print("46 Leopard Bushfish")
        print("47 Redtail Catfish")
        print("48 Japanese Bullhead Shark")
        print("49 Lookdown Fish")
        print("\n")
        for i in range(amnt):
            sel = int(input('Selection %s: ' % i))
            if sel < 40:
                header["fish_amount_%s" % i] = u8(1)
                header["fish_id_%s" % i] = u8(sel)
                header["fish_growth_level_%s" % i] = u16(0)
                header["fish_hungry_degree_%s" % i] = u16(0)
                header["fish_padding_%s" % i] = u16(1)
                header["fish_birthday_%s" % i] = u32(1)  # Birthday is day 1
                header["current_day_%s" % i] = u32(1)  # Current day set to 1
            else:
                print("Error: Invalid selection")
    else:
        print("Error: Invalid amount, skipping")
        amnt = 0

header["fish_tables"] = pad(240 - (amnt * 16))
header["object_tables"] = pad(160)  # TODO: Add in object tables

print("Processing ...")

f = io.BytesIO()
for k, v in list(header.items()): f.write(v)
f.flush()
f.seek(0)
copy = f.read()
crc32 = format(binascii.crc32(copy) & 0xFFFFFFFF, '08x')
f.close()

file = open('a0014682.dat', 'wb')  # Not sure how the name is generated yet
file.write(binascii.unhexlify('08051400'))  # Magic Value
file.write(binascii.unhexlify(crc32))  # CRC32
file.write(copy)  # Rest of File
file.flush()
file.close()

print("\n")
print("Completed Successfully")

#!/usr/bin/python
# -*- coding = utf-8 -*-

import binascii # Used to write to stuff in hex.
import collections # Used to write stuff in dictionaries in order.
import epub # Used to read EPUBs.
import md5 # Used to calculate MD5s.
import os # Used to get file stuff.
import struct # Needed to pack u32s and other integers.
import subprocess # Needed to run DSDecmp, which is for LZ77 compression.
import sys # Used for arguments.
from bs4 import BeautifulSoup # Used to parse HTML.
from newspaper import * # Used to parse news articles.

"""This will pack the integers."""

def u8(data):
    return struct.pack("<B", data)

def u16(data):
    return struct.pack("<H", data)

def u32(data):
    return struct.pack("<I", data)
    
"""Run the functions to make the book."""

def make_book():
	header = make_header()
	main_data_table = make_main_data_table(header)
	book_text = make_book_text()
	book_data = make_book_data(main_data_table, header)
	write = write_dictionary()
	
"""This is a function used to count offsets."""

def offset_count():
	return u32(16 + sum(len(values) for dictionary in dictionaries for values in dictionary.values() if values))

dictionaries = []

def make_header():
	header = collections.OrderedDict()
	dictionaries.append(header)
	
	header["book_data_number"] = u32(15) # Number of the book's data.
	header["main_data_table_offset"] = u32(0) # Offset for the main data.
	header["cover_offset"] = u32(0) # Offset for the cover.
	header["books_pages_offset"] = u32(0) # Offset for a file with page offsets.
	header["outline_offset"] = u32(0) # Offset for outline data.
	header["book_data_offset"] = u32(0) # Offset for book data.
	
	for numbers in range(1, 4):
		header["book_data_offset_%s" % numbers] = u32(0) # Offset for book text.
	
	for numbers in range(1, 12):
		header["about_book_offset_%s" % numbers] = u32(0) # Offset for the text for "about book".
		
	header["about_author_offset"] = u32(0) # Offset for the text for "about the author".
	header["author_portrait_offset"] = u32(0) # Offset for the author's portrait.
	header["chapter_data_offset"] = u32(0) # Offset for the chapter data.
	header["end_of_file_offset"] = u32(0) # Offset for the end of the file.
	header["main_data_table_size"] = u32(0) # Size of the main data table.
	header["cover_size"] = u32(0) # Size of the cover.
	header["books_pages_size"] = u32(0) # Size of a file with page offsets.
	header["outline_size"] = u32(0) # Size of outline data.
	header["book_data_size"] = u32(0) # Size of book data.
	
	for numbers in range(1, 4):
		header["book_data_size_%s" % numbers] = u32(0) # Size of book text.
	
	for numbers in range(1, 12):
		header["about_book_size_%s" % numbers] = u32(0) # Size of the text for "about book".
		
	header["about_author_size"] = u32(0) # Size of the text for "about the author".
	header["author_portrait_size"] = u32(0) # Size of the author's portrait.
	header["chapter_data_size"] = u32(0) # Size of the chapter data.
	header["unknown"] = u32(0) # Unknown.
	
	return header
	
def make_main_data_table(header):
	main_data_table = collections.OrderedDict()
	dictionaries.append(main_data_table)
	
	header["main_data_table_offset"] = offset_count() # Offset for the main data table.
	header["main_data_table_size"] = u32(300) # Size of the main data table.
	
	main_data_table["unknown_1"] = u32(1) # Unknown.
	main_data_table["unknown_2"] = u32(76) # Unknown.
	main_data_table["unknown_3"] = u32(48) # Unknown.
	main_data_table["title_data_size"] = u32(131) # Size of the title data.
	main_data_table["unknown_4"] = u32(192) # Unknown.
	main_data_table["unknown_5"] = u32(76) # Unknown.
	main_data_table["unknown_6"] = u32(272) # Unknown.
	main_data_table["unknown_7"] = u32(7) # Unknown.
	main_data_table["unknown_8"] = u32(0) # Unknown.
	main_data_table["unknown_9"] = u32(109) # Unknown.
	main_data_table["unknown_10"] = u32(119) # Unknown.
	main_data_table["unknown_11"] = u32(0) # Unknown.
	main_data_table["title_data_1"] = "Little Women\0"
	main_data_table["title_data_2"] = "Louisa May Alcott\0"
	main_data_table["title_data_3"] = "LITTLE<br>WOMEN\0"
	main_data_table["title_data_4"] = "Louisa<br>May Alcott\0"
	main_data_table["title_data_5"] = "Little Women\0"
	main_data_table["title_data_6"] = "LITTLEWOMEN\0"
	main_data_table["title_data_7"] = "ALCOTTLOUISAMAY\0"
	main_data_table["title_data_8"] = "BookData_\0"
	main_data_table["title_data_9"] = "LittleWomen"
	main_data_table["unknown_12"] = binascii.unhexlify("0000000000000000000000000000") # Unknown.
	main_data_table["unknown_13"] = binascii.unhexlify("300000003D0000004F0000005F00000074000000810000008D00000001005C1D010200000100000000000001010001000000000000000100000000000000010100000000010000010001D0D000000000C0000000C4000000C8000000CC000000D0000000D4000000D8000000") # Unknown.
	
	return main_data_table
	
def make_book_text():
	book = epub.open_epub("book.epub")
	
	book_text = ""
	
	for item in book.opf.manifest.values():
		soup = book.read_item(item)
		
		url = ""
		
		data = Article(url, language="en")
		data.set_html(book.read_item(item))
		
		data.parse()
		
		book_text += data.text
		
	if not os.path.exists("Data_Input/5_Book_Text"):
		os.mkdir("Data_Input/5_Book_Text")
	
	with open("Data_Input/5_Book_Text/LittleWomen_00.bd", "wb") as dest_file:
		dest_file.write(book_text.encode("utf-8"))
		
	subprocess.call(["wine", "narctool.exe", "p", "Data_Input/5_Book_Text", "Data_Input/5_Book_Text.narc"])
	
def make_book_data(main_data_table, header):
	book_data = collections.OrderedDict()
	dictionaries.append(book_data)
	
	lz77_compress = subprocess.call(["mono", "DSDecmp.exe", "-c", "lz10", "Data_Input", "Data_Output"])
	
	with open("Data_Output/1_Cover.narc", "rb") as source_file:
		read = source_file.read()
		header["cover_offset"] = offset_count()
		header["cover_size"] = u32(len(read) + 2)
		book_data["cover"] = read
		book_data["padding_1"] = u16(0)
		
	with open("Data_Output/2_Books_Pages.narc", "rb") as source_file:
		read = source_file.read()
		header["books_pages_offset"] = offset_count()
		header["books_pages_size"] = u32(len(read) + 1)
		book_data["books_pages"] = read
		book_data["padding_2"] = u8(0)
		
	with open("Data_Output/3_Outline.narc", "rb") as source_file:
		read = source_file.read()
		header["outline_offset"] = offset_count()
		header["outline_size"] = u32(len(read) + 1)
		book_data["outline"] = read
		book_data["padding_3"] = u8(0)
		
	with open("Data_Output/4_Book_Data.narc", "rb") as source_file:
		read = source_file.read()
		header["book_data_offset"] = offset_count()
		header["book_data_size"] = u32(len(read) + 3)
		book_data["book_data"] = read
		book_data["padding_4"] = u8(0) * 3
		
	with open("Data_Output/5_Book_Text.narc", "rb") as source_file:
		read = source_file.read()
		header["book_data_offset_1"] = offset_count()
		header["book_data_size_1"] = u32(0)
		header["book_data_offset_2"] = offset_count()
		header["book_data_size_2"] = u32(len(read) + 3)
		book_data["book_data_1"] = read
		book_data["padding_5"] = u8(0) * 3
 		
	with open("Data_Output/6_Book_Text.narc", "rb") as source_file:
		read = source_file.read()
		header["book_data_offset_3"] = offset_count()
		header["book_data_size_3"] = u32(len(read) + 3)
		book_data["book_data_2"] = read
		book_data["padding_6"] = u8(0) * 3
		
	with open("Data_Output/7_About_Book.narc", "rb") as source_file:
		read = source_file.read()
		for numbers in range(1, 12):
			header["about_book_offset_%s" % numbers] = offset_count()
		header["about_book_size_11"] = u32(len(read))
		book_data["about_book"] = read
		
	with open("Data_Output/8_About_the_Author.narc", "rb") as source_file:
		read = source_file.read()
		header["about_author_offset"] = offset_count()
		header["about_author_size"] = u32(len(read) + 2)
		book_data["about_author"] = read
		book_data["padding_7"] = u16(0)
		
	with open("Data_Output/9_Author_Portrait.narc", "rb") as source_file:
		read = source_file.read()
		header["author_portrait_offset"] = offset_count()
		header["author_portrait_size"] = u32(len(read))
		book_data["author_portrait"] = read
		
	with open("Data_Output/10_Chapter_Data.narc", "rb") as source_file:
		read = source_file.read()
		header["chapter_data_offset"] = offset_count()
		header["chapter_data_size"] = u32(len(read) + 1)
		book_data["chapter_data"] = read
		book_data["padding_8"] = u8(0)
		
	header["end_of_file_offset"] = offset_count()

def write_dictionary():
	open("book_001.bin", "w+")
	
	for dictionary in dictionaries:
		for values in dictionary.values():
			with open("book_001.bin", "a+") as dest_file:
				dest_file.write(values)
				
	with open("book_001.bin", "rb") as source_file:
		read = source_file.read()
		
	m = md5.new()
	m.update(read)
	m = binascii.unhexlify(m.hexdigest())
	
	with open("book_001.bin", "w+") as dest_file:
		dest_file.write(m)
		dest_file.write(read)
			
book = make_book()
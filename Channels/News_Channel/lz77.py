import glob
import os
import subprocess

"""This is used to decompress the news.bin files."""

def decompress(file):
	with open(file, "rb") as source_file:
		read = source_file.read()

		tail = read[320:]

	with open(file + ".2", "w+") as dest_file:
		dest_file.write(tail)

	FNULL = open(os.devnull, "w+")

	decompress = subprocess.call(["mono", "--runtime=v4.0.30319", "DSDecmp.exe", "-d", file + ".2", file + ".3"], stdout=FNULL, stderr=subprocess.STDOUT)
	remove = os.remove(file + ".2")
	move = subprocess.call(["mv", file + ".3", file + ".2"], stdout=FNULL, stderr=subprocess.STDOUT)
	open_hex = subprocess.call(["open", "-a", "Hex Fiend", file + ".2"], stdout=FNULL, stderr=subprocess.STDOUT) # This is to open the news files in the Mac hex editor I use called Hex Fiend.

for file in glob.glob("news.bin.*"):
	if os.path.exists(file):
		decompress(file)

for file in glob.glob("*.bin"):
	if os.path.exists(file):
		decompress(file)

# Rewrote Mainichi in Python - TheMrIron2
import sys
import os
from bs4 import BeautifulSoup
os.chdir(r'C:\Python27') #insertyourpathere
html = open("page.html", 'r+') #changethehtmlfilenameifyouwant
soup = BeautifulSoup(html, 'html.parser')
with open("temp_mainichi.html", "w") as file:
    file.write(str(soup))

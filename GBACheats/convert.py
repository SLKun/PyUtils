#!/usr/bin/python3
#
# Author: SLKun <summerslyb@gmail.com>
# Website: https://github.com/SLKun/PyUtils/GBACheats/convert.py
#

import sys
import xml.dom.minidom

def convertData(data):
    datas = data.split(" ");
    if(datas[0][0] == '3'): # Half-Word
        return ("%s,%s" % (datas[0][3:], datas[1][2:4]))
    elif(datas[0][0] == '8'): # Full-Word
        return ("%s,%s,%s" % (datas[0][3:], datas[1][2:4], datas[1][0:2]))

# Parse command line
if(len(sys.argv) == 1):
    print("Help: python3 convert.py [My Boy! CHT]\n")
    print("You can get cht files from https://gamehacking.org/")
    print("Ignore CRC Check and Button Trigger.")
    quit()
else:
    filename = sys.argv[1]

# Parse XML
dicts = {}
DOMTree = xml.dom.minidom.parse(filename)
cheats = DOMTree.documentElement.getElementsByTagName("cheat")
for cheat in cheats:    
    name = cheat.getAttribute("name")
    if(name != "M"):
        codes = cheat.getElementsByTagName("code");
        for code in codes:
            if name not in dicts:
                dicts[name] = []

            data = convertData(code.firstChild.data)
            if(data):
                dicts[name].append(data)

# Generate EZ-Flash CHT
for name in dicts.keys():
    print("[%s]\nON=" % name, end='')
    print(";".join(dicts[name]) + "\n")

filename = filename[:-4]
print("[GameInfo]")
print("Name=%s" % filename)
print("System=GBA")
print("Text=%s" % filename)
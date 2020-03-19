#!/usr/bin/python3
#
# Convert My boy! CHT to EZ-Flash CHT
# Author: SLKun <summerslyb@gmail.com>
# Website: https://github.com/SLKun/PyUtils/blob/master/GBACheats/convert.py
#

import re
import sys
import xml.dom.minidom

def convertData(data):
    datas = data.split(" ");
    command = datas[0][0];
    if(command == '3'): # Half-Word RAM Write
        return ("%s,%s" % (datas[0][3:], datas[1][2:4]))
    elif(command == '8'): # Full-Word RAM Write
        return ("%s,%s,%s" % (datas[0][3:], datas[1][2:4], datas[1][0:2]))
    elif(command == '1' or command == 'D'): # Hook Code & Pad Read
        return # Ignore
    elif(command == '6'): # Math Operation
        return # Ignore
    elif(command == '7' or command == 'A' or command == 'F'): # Condition
        pass
    elif(command == '4' or command == '0' or command == 'E'): # Slide Code
        pass
    else:
        pass
        #print("Unknown Command: " + command)
    return "error"

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
    name = re.sub(r' \[.*\]', "", cheat.getAttribute("name")) # remove [] in name
    codes = cheat.getElementsByTagName("code")
    for code in codes:
        if name not in dicts:
            dicts[name] = []

        data = convertData(code.firstChild.data)
        if(data):
            if(data == "error"):
                dicts[name].clear()
                break
            else:
                dicts[name].append(data)

# Generate EZ-Flash CHT
for name in dicts.keys():
    if(len(dicts[name]) > 0):
        print("[%s]" % name)
        print("ON=" + ";".join(dicts[name]) + ";\n")

filename = filename[:-4]
print("[GameInfo]")
print("Name=%s" % filename)
print("System=GBA")
print("Text=%s" % filename)
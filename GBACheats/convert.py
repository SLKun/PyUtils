#!/usr/bin/python3
#
# Convert My boy! CHT (CodeBreaker) to EZ-Flash CHT
# Author: SLKun <summerslyb@gmail.com>
# Website: https://github.com/SLKun/PyUtils/blob/master/GBACheats/convert.py
# CodeBreaker Ref: http://www.sappharad.com/gba/codes/codebreaker-code-creation
# EZCheat Ref: https://wiki.bibanon.org/EZ_Flash/Cheats

import re
import sys
import xml.dom.minidom

# Convert Codebreaker/GameShark SP/Xploder to EZCheat
def convertData(data):
    datas = data.split(" ")
    command = datas[0][0]
    if(command == '3'): # 8bit RAM Write
        return ("%s,%s" % (datas[0][3:], datas[1][2:4]))
    elif(command == '8'): # 16bit RAM Write
        return ("%s,%s,%s" % (datas[0][3:], datas[1][2:4], datas[1][0:2]))
    elif(command == '4'): # Slide Code
        return "slide"
    elif(command == 'D'): # 16-bit Pad Read
        return # Ignore
    elif(command == '0'): # CRC Check
        return # Ignore
    elif(command == '1'): # Hook Code
        return # Ignore
    elif(command == '6'): # Math Operation
        return # Ignore
    elif(command == '7' or command == 'F' or command == 'A'): # Condition
        return "error"
    else:
        # print("Unknown Command: " + data)
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
    codes = cheat.getElementsByTagName("code") # codes for this name

    # if multiple identical name, choose first one
    if name not in dicts:
        dicts[name] = []
        slideCode = ""
        for code in codes:
            rawData = code.firstChild.data
            if(not slideCode):
                data = convertData(rawData)
                if(data):
                    if(data == "error"):
                        # Not support
                        dicts[name].clear()
                        break
                    if(data == "slide"):
                        # Slide Code
                        slideCode = rawData
                    else:
                        # Normal Code
                        dicts[name].append(data)
            else:
                # Process Slide Code
                # print("Slide Code: " + slideCode + " " + rawData)
                addr = slideCode.split(" ")[0][3:]
                addrCnt = int(rawData.split(" ")[0][4:], 16)
                addrInc = int(rawData.split(" ")[1], 16)
                val = slideCode.split(" ")[1]
                valInc = int(rawData.split(" ")[0][:4], 16)
                # print(addr, val, valInc, addrCnt, addrInc)

                if(addrInc == 2 and valInc == 0):
                    data = addr + ","
                    val = ("%s,%s" % (val[2:4], val[0:2]))
                    for i in range(0, int(addrCnt)):
                        data += val + ","
                    dicts[name].append(data[:-1])
                else:
                    # Not support
                    # print("NotSupported")
                    dicts[name].clear()
                    break

                slideCode = ""

        # Remove Empty Item
        if(len(dicts[name]) == 0):
            del dicts[name]

# Generate EZ-Flash CHT
for name in dicts.keys():
    print("[%s]" % name)
    print("ON=" + ";".join(dicts[name]) + ";\n")

print("[GameInfo]")
print("Name=" + filename[:-4])
print("System=GBA")
print("Text=" + filename[:-4])
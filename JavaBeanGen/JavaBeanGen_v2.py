#!/usr/bin/python2

import json
import os
import sys

def removeParams(item):
	for key in item.keys():
		if isinstance(item[key], unicode):
			gEnv.pop(key);
			
def storeParams(item):
	for key in item.keys():
		if isinstance(item[key], unicode):
			gEnv[key] = item[key];

def printDic(dic):
	if isinstance(dic, dict):
		print("{");
		for key in dic.keys():
			sys.stdout.write(indent + key + ": ");
			print(dic[key]);
		print("}");

def genIntent(level):
	i = 0;
	curIndent = "";
	while i < level:
		curIndent += indent;
		i += 1;
	return curIndent

def chkVar(var):
	if gEnv.has_key(var):
		return gEnv[var];
	return "";

# arugments
indent = "    ";
gEnv = dict();
gStack = list();

# init
gEnv["indentLevel"] = 0;
gEnv["stackPointer"] = 0;

# read json
filename = "params_v2.json";
if len(sys.argv) > 1:
	filename = sys.argv[1] + ".json";
gEnv["filename"] = filename;
f = open(filename);
paramJson = f.read();
f.close();

# parse json
paramData = json.loads(paramJson);
storeParams(paramData);
# parse classes
for classItem in paramData["Classes"]:
	storeParams(classItem);
	className = chkVar("class");
	modifier = chkVar("modifier");
	curIndent = genIntent(gEnv["indentLevel"]);

	if os.path.exists(className + ".java"):
		if os.path.exists(className + ".java.bak"):
			os.remove(className + ".java.bak");
		os.rename(className + ".java", className + ".java.bak");
	f = open(className + ".java", "w");

	f.write(curIndent + modifier + " class " + className +"{\n");

	# generate private field
	gEnv["indentLevel"] += 1;
	for var in classItem["varibles"]:
		storeParams(var);
		varType = chkVar("type");
		varName = chkVar("name");
		initVal = chkVar("initVal");
		curIndent = genIntent(chkVar("indentLevel"));

		f.write(curIndent + "private " + varType + " " + varName);
		if initVal != "":
			f.write(" = ");
			if varType == "String" :
				f.write('"' + initVal + '"');
			else :
				f.write(initVal);
		f.write(";\n");
		removeParams(var);
	f.write("\n");
	storeParams(classItem);
	gEnv["indentLevel"] -= 1;
	# generate getter
	for var in classItem["varibles"]:
		f.write(indent + "public " + var["type"] + " get");
		f.write(var["name"][0].upper() + var["name"][1:len(var["name"])]);
		f.write("(){\n");
		f.write(indent + indent + "return " + var["name"]);
		f.write(";\n" + indent + "}\n\n");
	# generate Setter
	for var in classItem["varibles"]:
		f.write(indent + "public void set");
		f.write(var["name"][0].upper() + var["name"][1:len(var["name"])]);
		f.write("(" + var["type"] + " " + var["name"] + "){\n");
		f.write(indent + indent + "this." + var["name"] + " = " + var["name"]);
		f.write(";\n" + indent + "}\n\n");
	f.write("}\n");
removeParams(paramData);
printDic(gEnv);
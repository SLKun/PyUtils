#!/usr/bin/python2

import json
import os
import sys

def removeParams(item):
	for key in item.keys():
		if not(isinstance(item[key], list) or isinstance(item[key], dict)):
			gEnv.pop(key);
			
def storeParams(item):
	for key in item.keys():
		if not(isinstance(item[key], list) or isinstance(item[key], dict)):
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

def push(item):
	gEnv["indentLevel"] += 1;
	global curIndent;
	curIndent = genIntent(chkVar("indentLevel"));
	gStack.append(item);
	storeParams(item);

def pop():
	gEnv["indentLevel"] -= 1;
	global curIndent;
	curIndent = genIntent(chkVar("indentLevel"));
	removeParams(gStack.pop());
	if len(gStack) != 0:
		storeParams(gStack[-1]);

# arugments
indent = "    ";
gEnv = dict();
gStack = list();

# init
gEnv["indentLevel"] = -1;

# read json
filename = "params.json";
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
	push(classItem);
	className = chkVar("class");
	modifier = chkVar("modifier");

	if os.path.exists(className + ".java"):
		if os.path.exists(className + ".java.bak"):
			os.remove(className + ".java.bak");
		os.rename(className + ".java", className + ".java.bak");
	f = open(className + ".java", "w");

	f.write(curIndent + modifier + " class " + className +"{\n");

	# generate private field
	for var in classItem["varibles"]:
		push(var);
		varType = chkVar("type");
		varName = chkVar("name");
		initVal = chkVar("initVal");

		f.write(curIndent + "private " + varType + " " + varName);
		if initVal != "":
			f.write(" = ");
			if varType == "String" :
				f.write('"' + initVal + '"');
			else :
				f.write(initVal);
		f.write(";\n");
		pop();
	# generate Getter
	for var in classItem["varibles"]:
		push(var);
		varType = chkVar("type");
		varName = chkVar("name");

		f.write("\n");
		f.write(curIndent + "public " + varType + " get");
		f.write(varName[0].upper() + varName[1:len(varName)]);
		f.write("(){\n");
		f.write(curIndent + indent + "return " + var["name"] + ";\n");
		f.write(curIndent + "}\n");
		pop();
	# generate Setter
	for var in classItem["varibles"]:
		push(var);
		varType = chkVar("type");
		varName = chkVar("name");

		f.write("\n");
		f.write(curIndent + "public void set");
		f.write(varName[0].upper() + varName[1:len(varName)]);
		f.write("(" + varType + " " + varName + "){\n");
		f.write(curIndent + indent + "this." + varName + " = " + varName + ";\n");
		f.write(curIndent + "}\n");
		pop();
	# generate Methods
	storeParams(classItem["method"]);
	for method in classItem["method"]["methods"]:
		push(method);
		modifier = chkVar("modifier");
		name = chkVar("name");
		retType = chkVar("retType");
		Exceptions = chkVar("Exceptions");
		retVal = chkVar("retVal");

		f.write("\n");
		f.write(curIndent + modifier + " " + retType + " " + name + "(");
		for arg in method["args"]:
			push(arg);
			arguName = chkVar("name");
			arguType = chkVar("type");

			f.write(arguType + " " + arguName + ", ");
			pop();
		f.write("\b\b");
		f.write(") throws " + Exceptions + "{\n");
		f.write(curIndent + indent + "return " + retVal + ";\n");
		f.write(curIndent + "}\n");
		pop();
	f.write("}\n");
	pop();

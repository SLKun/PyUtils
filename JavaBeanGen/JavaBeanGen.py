#!/usr/bin/python2

import json
import os
import sys


# helper function
def print_dic(dic):
    if isinstance(dic, dict):
        print("{")
        for key in dic.keys():
            sys.stdout.write(indent + key + ": ")
            print(dic[key])
        print("}")


def print_stack():
    print "====== Stack Information ======"
    for item in gStack:
        # print_dic(item)
        print(item)


# generate proper Indent
def generate_indent(level):
    i = 0
    global curIndent
    curIndent = ""
    while i < level:
        curIndent += indent
        i += 1
    return curIndent


def parse_list_with_value(alist):
    str = ""
    if isinstance(alist, list):
        for item in alist:
            if not (isinstance(item, dict) or isinstance(item, list)):
                str += item
                if item != alist[-1]:
                    str += ", "
    return str


def parse_list_with_dict(key, alist):
    s = ""
    args = dict()
    i = 0
    if isinstance(alist, list):
        for item in alist:
            if isinstance(item, dict):
                # get args dict
                for dicKey in item.keys():
                    if isinstance(item[dicKey], dict) or isinstance(item[dicKey], list):
                        return ""
                    split = dicKey.split("_")
                    if key.startswith(split[0]):
                        if (len(split) == 3):
                            args[split[2]] = item[dicKey]
                        else:
                            args[str(i)] = item[dicKey]
                            i += 1
                    else:
                        return s
                s += args["0"] + " " + args["1"]
            else:
                return s
            if item != alist[-1]:
                s += ", "
    return s


# update global Environment
def update_environment(item):
    for key in item.keys():
        if not (isinstance(item[key], list) or isinstance(item[key], dict)):
            gEnv[key] = item[key]
        if isinstance(item[key], list):
            gEnv[key] = parse_list_with_value(item[key])
            if gEnv[key] == "":
                gEnv[key] = parse_list_with_dict(key, item[key])


# get Var from Environment
# checking whether the var is exist
def get_var(var):
    if gEnv.has_key(var):
        return gEnv[var]
    return ""


def push(item):
    global gEnv
    newEnv = dict(gEnv)
    gStack.append(gEnv)
    gEnv = newEnv
    update_environment(item)


def pop():
    global gEnv
    if len(gStack) != 0:
        gEnv = gStack.pop()


# arugments
indent = "	"
gEnv = dict()
gStack = list()
curIndent = ""

# init
gEnv["indentLevel"] = -1

# read json
filename = "params.json"
if len(sys.argv) > 1:
    filename = sys.argv[1] + ".json"
gEnv["filename"] = filename
f = open(filename)
paramJson = f.read()
f.close()

# parse json
paramData = json.loads(paramJson)
update_environment(paramData)
# parse classes
for classItem in paramData["Classes"]:
    push(classItem)
    className = get_var("class")
    modifier = get_var("modifier")

    if os.path.exists(className + ".java"):
        if os.path.exists(className + ".java.bak"):
            os.remove(className + ".java.bak")
        os.rename(className + ".java", className + ".java.bak")
    f = open(className + ".java", "w")

    f.write(curIndent + modifier + " class " + className + "{\n")

    # generate private field
    for var in classItem["varibles"]:
        push(var)
        varType = get_var("type")
        varName = get_var("name")
        initVal = get_var("initVal")

        f.write(curIndent + "private " + varType + " " + varName)
        if initVal != "":
            f.write(" = ")
            if varType == "String":
                f.write('"' + initVal + '"')
            else:
                f.write(initVal)
        f.write(";\n")
        pop()
    # generate Getter
    for var in classItem["varibles"]:
        push(var)
        varType = get_var("type")
        varName = get_var("name")

        f.write("\n")
        f.write(curIndent + "public " + varType + " get")
        f.write(varName[0].upper() + varName[1:len(varName)])
        f.write("(){\n")
        f.write(curIndent + indent + "return " + var["name"] + ";\n")
        f.write(curIndent + "}\n")
        pop()
    # generate Setter
    for var in classItem["varibles"]:
        push(var)
        varType = get_var("type")
        varName = get_var("name")

        f.write("\n")
        f.write(curIndent + "public void set")
        f.write(varName[0].upper() + varName[1:len(varName)])
        f.write("(" + varType + " " + varName + "){\n")
        f.write(curIndent + indent + "this." + varName + " = " + varName + ";\n")
        f.write(curIndent + "}\n")
        pop()
    # generate Methods
    update_environment(classItem["method"])
    for method in classItem["method"]["methods"]:
        push(method)
        modifier = get_var("modifier")
        name = get_var("name")
        retType = get_var("retType")
        Exceptions = get_var("Exceptions")
        retVal = get_var("retVal")
        args = get_var("args")

        f.write("\n")
        f.write(curIndent + modifier + " " + retType + " " + name + "(")
        f.write(gEnv["args"])
        f.write("\b\b")
        f.write(") throws " + Exceptions + "{\n")
        f.write(curIndent + indent + "return " + retVal + ";\n")
        f.write(curIndent + "}\n")
        pop()
    f.write("}\n")
    pop()

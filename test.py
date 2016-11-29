import json
import os
import sys

# read argument
print sys.argv;

# read json
f = open("params.json");
content = f.read();
f.close();

# parse json
data = json.loads(content);
for classItem in data:
	# generate File
	className = classItem["class"];
	if os.path.exists(className + ".java") and os.path.isfile(className + ".java") :
		if os.path.exists(className + ".java.bak"):
			os.remove(className + ".java.bak");
		os.rename(className + ".java", className + ".java.bak");
	f = open(className + ".java", "w");
	# write to the file
	f.write("public class " + className +"{\n");
	# generate private field
	for var in classItem["varible"]:
		f.write("\tprivate " + var["type"] + " " + var["varName"]);
		if var.has_key("initVal") :
			f.write(" = ");
			if var["type"] == "String" :
				f.write('"' + var["initVal"] + '"');
			else :
				f.write(var["initVal"]);
		f.write(";\n");
	f.write("\n");
	# generate getter
	for var in classItem["varible"]:
		f.write("\tpublic " + var["type"] + " get");
		f.write(var["varName"][0].upper() + var["varName"][1:len(var["varName"])]);
		f.write("(){\n");
		f.write("\t\treturn " + var["varName"]);
		f.write(";\n\t}\n\n");
	# generate Setter
	for var in classItem["varible"]:
		f.write("\tpublic void set");
		f.write(var["varName"][0].upper() + var["varName"][1:len(var["varName"])]);
		f.write("(" + var["type"] + " " + var["varName"] + "){\n");
		f.write("\t\tthis." + var["varName"] + " = " + var["varName"]);
		f.write(";\n\t}\n\n");
	f.write("}\n");

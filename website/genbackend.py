from GeneralPythonCopy.General import General
import os
import sys


path = "C:\\Users\\Xaos\\Desktop\\Web App\\uploaded_files"
directory = os.listdir(path)

list_of_files = []
if len(directory) != 0:
	for file in directory:
		list_of_files.append(file)
else:
	exit()

print("there are files in the uploaded_files")



dict_of_regression = {}
for file in list_of_files:
	dict_of_regression[f'{file}'] = General.gp_symbolic_regression(file, )
	pass



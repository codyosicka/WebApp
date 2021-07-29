from GeneralPythonCopy.General import General # stored in C:\Users\Xaos\AppData\Roaming\Python\Python39\site-packages
import os
import sys


path = "C:\\Users\\Xaos\\Desktop\\Web App\\uploaded_files"
directory = os.listdir(path)

files_in_directory = []
if len(directory) != 0:
	for file in directory:
		files_in_directory.append(file)
else:
	exit()

print("There are files in the uploaded_files: ", files_in_directory)


txt_list = []
csv_xlsx_list = []
for file in files_in_directory:
	if ".csv" in file:
		csv_xlsx_list.append(file)
	elif ".xlsx" in file:
		csv_xlsx_list.append(file)
	elif ".txt" in file:
		txt_list.append(file)

print(files_in_directory)
print(txt_list)
print(csv_xlsx_list)


#dict_of_regression = {}
#for file in :
	#dict_of_regression[f'{file}'] = General.gp_symbolic_regression(file, )
	#pass



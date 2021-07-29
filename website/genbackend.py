from GeneralPythonCopy.General import General # stored in C:\Users\Xaos\AppData\Roaming\Python\Python39\site-packages
import os
import sys


path = "C:\\Users\\Xaos\\Desktop\\Web App\\uploaded_files"
directory = os.listdir(path)
directory_sorted = sorted(directory) # sorts files and subdirectories within the current directory in alphabetic order

files_in_directory = []
if len(directory) != 0:
	for file in directory_sorted:
		files_in_directory.append(file)
else:
	exit()

print("There are files in the uploaded_files: ", files_in_directory)
print()


txt_list = []
csv_xlsx_list = []
for file in files_in_directory:
	if ".csv" in file:
		csv_xlsx_list.append(file)
	elif ".xlsx" in file:
		csv_xlsx_list.append(file)
	elif ".txt" in file:
		txt_list.append(file)


dict_of_files = {csv_xlsx_list[i]: txt_list[i] for i in range(len(csv_xlsx_list))}


print(txt_list)
print()
print(csv_xlsx_list)
print()
print(dict_of_files)


dict_of_regression = {}
#for key in dict_of_files:
	#dict_of_regression['{}'.format(key)] = General.gp_symbolic_regression(file, )
	#pass



# stored in C:\Program Files\Python39\Lib\site-packages 
# or stored in C:\Users\Xaos\AppData\Roaming\Python\Python39\site-packages
from GeneralPythonCopy.General import General
import os
import sys


#path = "C:\\Users\\Buff14\\Desktop\\Web App\\uploaded_files"
path = "C:\\Users\\Xaos\\Desktop\\Web App\\uploaded_files"
directory = os.listdir(path)
directory_sorted = sorted(directory) # sorts files and subdirectories within the current directory in alphabetic order

files_in_directory = []
if len(directory) != 0:
	for file in directory_sorted:
		files_in_directory.append(file)
else:
	exit()

print()
print("There are files in the uploaded_files: ", files_in_directory)
print()


txt_list = []
csv_xlsx_list = []
object_list = []
for file in files_in_directory:
	if file.endswith(".csv"):
		#csv_xlsx_list.append("C:\\Users\\Buff14\\Desktop\\Web App\\uploaded_files\\"+file)
		csv_xlsx_list.append("C:\\Users\\Xaos\\Desktop\\Web App\\uploaded_files\\"+file)
	elif file.endswith(".xlsx"):
		#csv_xlsx_list.append("C:\\Users\\Buff14\\Desktop\\Web App\\uploaded_files\\"+file)
		csv_xlsx_list.append("C:\\Users\\Xaos\\Desktop\\Web App\\uploaded_files\\"+file)
	elif file.endswith(".txt"):
		txt_list.append(file)
		object_list.append(file.replace(".txt", ""))

read_variables = []
for file in directory_sorted:
	if file.endswith(".txt"):
		#open_file = open("C:\\Users\\Buff14\\Desktop\\Web App\\uploaded_files\\"+file)
		open_file = open("C:\\Users\\Xaos\\Desktop\\Web App\\uploaded_files\\"+file)
		read_variables.append(open_file.read())
		open_file.close()

dict_of_files = {csv_xlsx_list[i]: txt_list[i] for i in range(len(csv_xlsx_list))}


dict_of_regression = {object_list[i]: General.gp_symbolic_regression(data=csv_xlsx_list[i], y_variable=read_variables[i]) for i in range(len(csv_xlsx_list))}

for regression in dict_of_regression:
	General.uploadto_equations_database(dict_of_regression[regression])

for file in directory_sorted:
	#os.remove("C:\\Users\\Buff14\\Desktop\\Web App\\uploaded_files\\"+file)
	os.remove("C:\\Users\\Xaos\\Desktop\\Web App\\uploaded_files\\"+file)


connection = General.create_engine("mysql+pymysql://unwp2wrnzt46hqsp:b95S8mvE5t3CQCFoM3ci@bh10avqiwijwc8nzbszc-mysql.services.clever-cloud.com/bh10avqiwijwc8nzbszc")
table = General.pd.read_sql_query("SELECT * FROM equations_table", connection)
print(table)
connection.dispose()



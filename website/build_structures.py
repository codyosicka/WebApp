from GeneralPythonCopy.General import General


# If equations database was updated:

total_structures = General.complete_structures()
print(total_structures)

constructed_matrices = {}
for structure in range(len(total_structures)):
	if total_structures[structure].shape[0] != total_structures[structure].shape[1]: # if the number of function is not equal to the number of variables
		continue
	else:
		#constructed_matrices[structure] = General.static_self_contained_causal_structure(total_structures[structure])
		pass
		
print(constructed_matrices)


#constructed_matrices = General.static_matrix_constructor()
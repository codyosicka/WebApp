from GeneralPythonCopy.General import General


# If equations database was updated:

total_structures, total_names = General.complete_structures()[0], General.complete_structures()[1]
print(total_names)
print(total_structures)

causal_results = {}
for structure in range(len(total_structures)):
	# Requires that the structure is self-contained (number of functions = number of variables)
	if total_structures[structure].shape[0] != total_structures[structure].shape[1]: # if the number of functions is not equal to the number of variables
		continue
	else:
		causal_results[structure] = General.static_causal_order(total_structures[structure])
		pass
		
print(causal_results)
print(causal_results[0])


#constructed_matrices = General.static_matrix_constructor()
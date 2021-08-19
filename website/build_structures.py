from GeneralPythonCopy.General import General


# If equations database was updated:

total_structures, total_names = General.complete_structures()[0], General.complete_structures()[1]
#print(total_names)
#print(total_structures)

causal_results = {}
causal_executed = []
for structure in range(len(total_structures)):
	# Requires that the structure is self-contained (number of functions = number of variables)
	if total_structures[structure].shape[0] != total_structures[structure].shape[1]: # if the number of functions is not equal to the number of variables
		continue
	else:
		causal_executed.append(structure) # causal_executed creates a list of the keys (here, structure) of the total_structures (and total_names) that were executed because they were self-contained
		causal_results[structure] = General.static_causal_order(total_structures[structure]) # this is a dict of dict of causal results
	structure+=1

new_causal_results_keys = list(range(len(list(causal_results.keys()))))
causal_results = dict(zip(new_causal_results_keys, causal_results.values())) # rekey the dictionary
		
print('causal_executed: ', causal_executed)
print('causal_results: ', causal_results)


total_names_executed = {} # equals total_names but only the executed ones
total_structures_executed = {} # equals total_structures but only the executed ones
for i in range(len(causal_executed)):
	total_names_executed[i] = total_names[causal_executed[i]] # now total_names_executed index will line up with causal_results
	total_structures_executed[i] = total_structures[causal_executed[i]] # now total_structures_executed index will line up with causal_results

print('total_names_executed: ', total_names_executed)
print('total_structures_executed: ', total_structures_executed)

#print(total_names_executed)
#print(total_structures_executed)

# Now total_names_executed, total_structures_executed, and causal_results should all have equal lengths

for i in range(len(list(causal_results.keys()))):
	General.initialize_mini_network(total_structures_executed[list(causal_results.keys())[i]], causal_results[list(causal_results.keys())[i]], total_names_executed[list(causal_results.keys())[i]])

General.build_causal_network()
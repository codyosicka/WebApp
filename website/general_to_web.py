from GeneralPythonCopy.General import General


'''

Process for User uploading data:

1. User: uploads files to Website (discrete occurance)
2. Backend: uploaded files go to uploaded_files which is accessible to the Web App py files 
3. Backend: performs gp_symbolic_regression on the information uploaded (discrete occurance)
4. Backend: uploads equation results to equations database (discrete occurance)
5. Backend: creates complete structures out of the equations database whenever the database is updated (discrete occurance)
6. Backend: for each key in complete_structures resultant dictionary:
			static_matrix_constructure(key) (discrete occurance)
7. Backend: static_self_contained_causal_structure(5) (discrete occurance)
8. Backend: static_causal_order(5) (discrete occurance)
9. Backend: initialize_mini_network(5, 7, name)
			if the name (of the network) already exists, modify_mini_network(5, 7, prev_network gexf graph, name) (discrete occurance)
10. Backend: build_causal_network() (discrete occurance)
11. Backend: when the AI is finished using the User's uploaded files, the AI deletes the files from the uploaded_files directory


Process for User performing a simulation

1. User: chooses equation name from menu; chooses variable from selected equation; inputs variable values of the equation; selects target variable from menu (discrete occurance)
2. Backend: 


Process for User performing an optimization

1. User: chooses an equation name from menu; chooses variable from selected equation; chooses objective to min or max; inputs contraints; inputs variable bounds; 
		 inputs initial condition (discrete occurance)
2. Backend: 


'''
from flask import Blueprint, render_template, request, flash, jsonify, current_app, redirect, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField, SelectField
from .models import Note
from . import db
import json
import os
import paypalrestsdk
import time
from GeneralPythonCopy.General import General


global list_of_files
list_of_files = []

equations_conn = General.create_engine()
sql = "SELECT * FROM equations_table"
read_sql = General.pd.read_sql(sql, equations_conn)



views = Blueprint('views', __name__, template_folder="templates")

#---------------------------------------------------------------------------------------------------------------------------------------------------------------

# Home Section

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
	return render_template("home.html", user=current_user)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------

# Upload Files Section

@views.route('/upload_files', methods=["GET", "POST"])
def upload_files():
	if request.method == 'POST':
		#list_of_files = request.files.getlist('file_name')
		for f in request.files.getlist('file_name'):
			list_of_files.append(f.filename)
			f.save(os.path.join(current_app.config["UPLOAD_PATH"], f.filename))
		#return render_template("upload-files.html", msg="Files have been uploaded successfully")
		return redirect(url_for('views.yvariables'))
	return render_template("upload-files.html", msg="Please Choose a file", user=current_user)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------

# Y Variables Section

@views.route('/yvariables', methods=["GET", "POST"])
def yvariables():

	class B(FlaskForm):
		list_of_files=list_of_files
		#path = "C:\\Users\\Buff14\\Desktop\\Web App\\uploaded_files"
		path = "C:\\Users\\Xaos\\Desktop\\Web App\\uploaded_files" # When the website is launched, this path will have to change
		directory = os.listdir(path)
		global listf
		listf = []
		if len(directory) != 0:
			for file in directory:
				listf.append(file)
		global list_to_use
		list_to_use = list(set(list_of_files).intersection(listf))
		global clist_to_execute
		clist_to_execute = []
		blist = []
		for file in range(len(list_to_use)):
			blist.append('b{}'.format(file))
			file+=1
		for file in range(len(list_to_use)):
			clist_to_execute.append('{} = StringField("{}")'.format(blist[file], list_to_use[file]))
			file+=1
		for exe in clist_to_execute:
			exec(exe)

	class A(FlaskForm):
		a2 = FieldList(FormField(B), min_entries=1)
		s = SubmitField("Submit Y Variables")

	form = A()
	if request.method == "POST":

		print("POSTED")

		b = request.form
		br = {x:b[x] for x in b if "a2-" in x} # b[x] are the y_variables
		#print(br)
		del br['a2-0-csrf_token']
		newkey = []
		for r in range(len(br)):
			newkey.append(r)
		oldkey = []
		for a in br:
			oldkey.append(a)
		for r in range(len(oldkey)):
			br[newkey[r]] = br.pop(oldkey[r])
		newlist = []
		for l in list_to_use:
			if ".csv" in l:
				newlist.append(l.replace(".csv", ""))
			elif ".xlsx" in l:
				newlist.append(l.replace(".xlsx", ""))
		text_list = []
		for r in range(len(newlist)):
			text_list.append("{}.txt".format(newlist[r]))
		#print(text_list)
		for text in range(len(text_list)):
			#saveFile = open("C:\\Users\\Buff14\\Desktop\\Web App\\uploaded_files\\"+text_list[text], 'w')
			saveFile = open("C:\\Users\\Xaos\\Desktop\\Web App\\uploaded_files\\"+text_list[text], 'w') # store the text files with y_variables in uploaded_files
			saveFile.write(br[text])
			saveFile.close()


		# begin reg_and_upload.py stuff here:

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

		#print()
		#print("There are files in the uploaded_files: ", files_in_directory)
		#print()

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

		#connection = General.create_engine()
		#table = General.pd.read_sql_query("SELECT * FROM equations_table", connection)
		#print(table)
		#connection.dispose()

		# end reg_and_upload.py stuff


		# begin build_structures.py stuff here

		total_structures, total_names = General.complete_structures()[0], General.complete_structures()[1]

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

		# Now total_names_executed, total_structures_executed, and causal_results should all have equal lengths
		for i in range(len(list(causal_results.keys()))):
			General.initialize_mini_network(total_structures_executed[list(causal_results.keys())[i]], causal_results[list(causal_results.keys())[i]], total_names_executed[list(causal_results.keys())[i]])
		General.build_causal_network()
		print("build network is done!")

		# end build_structures.py stuff here

		return redirect(url_for("views.home"))
		#return render_template('yvariables.html', msg="Upload Successful", form=form)
	else:
		print("NOT POSTED")
	return render_template('yvariables.html', msg="Please Input the Y Variables for each file uploaded", form=form, user=current_user)

@views.route("/r", methods=["POST"])
def r():
	b = request.form
	br = {x:b[x] for x in b if "a2-" in x}
	#return render_template("yvresult.html", b=br)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------

# Optimizer Section


class Form(FlaskForm):
	equation = SelectField('equation', choices=[])
	variable = SelectField('variable', choices=[])
	objective = SelectField('objective', choices=[("Maximize", "Maximize"), ("Minimize", "Minimize"), ('','')])


@views.route("/optimizer", methods=["GET", "POST"])
def optimizer():
	form = Form()
	form.equation.choices = [(y, y) for y in read_sql['equation_name']]
	form.equation.choices.append(('',''))

	variables_ = read_sql['x_variables'].values.tolist()
	variables_ = [','.join(variables_)]
	variables_ = list(set(variables_[0].split(",")))
	form.variable.choices = [(x, x) for x in variables_]
	form.variable.choices.append(('',''))
	

	if request.method == "POST":
		if form.variable.data == 'Self':
			self_results = General.self_optimizer(equation_name=form.equation.data, objective=form.objective.data)
			return '<h1 align="center">Results: {}</h1>'.format(self_results)
		else:
			try:
				other_results = General.variable_optimizer(chosen_variable=form.variable.data, equation_name=form.equation.data, objective=form.objective.data)
				return '<h1 align="center">Results: {}</h1>'.format(other_results)
			except:
				return'<h1 align="center">Sorry, this particular function or variable cannot be optimized</h1>'
		#return '<h1 align="center">Equation: {}, Variable: {}, Objective: {}</h1>'.format(form.equation.data, form.variable.data, form.objective.data)

	form.equation.default = ''
	form.variable.default = ''
	form.objective.default = ''
	form.process()

	return render_template('optimizer.html', form=form, user=current_user)


@views.route("/variable/<equation>")
def variable(equation):
	variables = read_sql[read_sql['equation_name']==equation]['x_variables'].values.tolist()[0].split(",")

	actual = read_sql[read_sql['equation_name']==equation]['equation'].values.tolist()[0]
	actual = General.sympify(actual)
	actual_symbols = list(actual.free_symbols)
	actual_symbols = list(map(str, actual_symbols))
	actual_symbols = [a.replace("X","") for a in actual_symbols]
	actual_symbols = list(set(map(int, actual_symbols)))

	actual_variables = []
	for a in actual_symbols:
		actual_variables.append(variables[a])
	actual_variables.append('Self')
	variables = actual_variables

	variableArray = []

	for v in variables:
		vObj = {}
		vObj['id'] = v
		vObj['var'] = v
		variableArray.append(vObj)

	return jsonify({"variables": variableArray})


#---------------------------------------------------------------------------------------------------------------------------------------------------------------

# Simulator Section

whole_graph = General.nx.read_gexf('C:\\Users\\Xaos\\Desktop\\Web App\\G_causal_network.gexf')
#whole_graph = General.nx.read_gexf('C:\\Users\\Buff14\\Desktop\\Web App\\G_causal_network.gexf')
nodes = whole_graph.nodes

class SimForm(FlaskForm):
	variablename = SelectField('variablename', choices=[])
	variablevalue = StringField('variablevalue')
	target = SelectField('target', choices=[])

@views.route("/simulator", methods=["GET", "POST"])
def simulator():
	form = SimForm()
	form.variablename.choices = [(x, x) for x in nodes]
	form.variablename.choices.append(('',''))
	form.target.choices = [(x, x) for x in nodes]
	form.target.choices.append(('',''))
	if request.method == "POST":
		sim_results = General.variable_simulator(variable_name=form.variablename.data, variable_value=form.variablevalue.data, 
				target_variable=form.target.data)
		return '<h1 align="center">Results: {}</h1>'.format(sim_results)
		#return '<h1 align="center">Results: {}</h1>'.format(read_sql)
		#try:
			#sim_results = General.variable_simulator(variable_name=form.variablename.data, variable_value=form.variablevalue.data, 
				#target_variable=form.target.data)
			#return '<h1 align="center">Results: {}</h1>'.format(sim_results)
		#except:
			#return'<h1 align="center">Sorry, there was an error in solving for {}</h1>'.format(form.target.data)
		
	form.variablename.default = ''
	form.target.default = ''
	form.process()

	return render_template('simulator.html', form=form, user=current_user)

@views.route("/target/<variablename>")
def target(variablename):
	new_nodes = [i for i in nodes]
	new_nodes.remove(variablename)

	targetArray = []

	for t in new_nodes:
		tObj = {}
		tObj['id'] = t
		tObj['tar'] = t
		targetArray.append(tObj)

	return jsonify({"targets": targetArray})

#---------------------------------------------------------------------------------------------------------------------------------------------------------------

# Paypal Section

paypalrestsdk.configure({
		"mode": "sandbox", # sandbox or live
		})

@views.route('/payment_required')
def payment_required():
	return render_template('payment-required.html')


@views.route('/payment', methods=['POST'])
def payment():

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "testitem",
                    "sku": "12345",
                    "price": "500.00",
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": "500.00",
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID' : payment.id})


@views.route('/execute', methods=['POST'])
def execute():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id' : request.form['payerID']}):
        print('Execute success!')
        success = True
    else:
        print(payment.error)

    return jsonify({'success' : success})

#---------------------------------------------------------------------------------------------------------------------------------------------------------------

equations_conn.dispose()

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

views = Blueprint('views', __name__, template_folder="templates")

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
	return render_template("upload-files.html", msg="Please Choose a file")

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
		br = {x:b[x] for x in b if "a2-" in x}
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
		for text in range(len(text_list)):
			#saveFile = open("C:\\Users\\Buff14\\Desktop\\Web App\\uploaded_files\\"+text_list[text], 'w')
			saveFile = open("C:\\Users\\Xaos\\Desktop\\Web App\\uploaded_files\\"+text_list[text], 'w')
			saveFile.write(br[text])
			saveFile.close()

		return redirect(url_for("views.home"))
		#return render_template('yvariables.html', msg="Upload Successful", form=form)
	else:
		print("NOT POSTED")
	return render_template('yvariables.html', msg="Please Input the Y Variables for each file uploaded", form=form)

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
	
@views.route("/optimizer", methods=["GET", "POST"])
def optimizer():

	equations_conn = General.create_engine("mysql+pymysql://unwp2wrnzt46hqsp:b95S8mvE5t3CQCFoM3ci@bh10avqiwijwc8nzbszc-mysql.services.clever-cloud.com/bh10avqiwijwc8nzbszc")
	sql = "SELECT * FROM equations_table"
	read_sql = General.pd.read_sql(sql, equations_conn)
	
	form = Form()
	form.equation.choices = [(x, x) for x in read_sql['equation_name']]
	form.variable.choices = [()]

	equations_conn.dispose()

	return render_template('optimizer.html', form=form)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------


# Paypal Section

paypalrestsdk.configure({
		"mode": "sandbox", # sandbox or live
		"client_id": "AYbnfU8Pj_yiF8ULPsCiU_R7vqDvIZfFP1s0qWUrokJM5W5ON9ypx56X4mqqzcrUKmrT_eZmvTqkGpop",
		"client_secret": "EE6mphrPS35PzRXwE1ZtsWWHMznLhBxrKh5vIxHtuxcCChGc0PpD9SELqpZgmenoGuLEDGR-CxvyRZ6W"
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
from flask import Blueprint, render_template, request, flash, jsonify, current_app, redirect, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField
from .models import Note
from . import db
import json
import os
import paypalrestsdk
import time

global list_of_files
list_of_files = []

views = Blueprint('views', __name__, template_folder="templates")

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
	return render_template("home.html", user=current_user)


@views.route('/upload_files', methods=["GET", "POST"])
def upload_files():
	#global list_of_files
	#list_of_files = []
	if request.method == 'POST':
		#list_of_files = request.files.getlist('file_name')
		for f in request.files.getlist('file_name'):
			list_of_files.append(f.filename)
			f.save(os.path.join(current_app.config["UPLOAD_PATH"], f.filename))
		#return render_template("upload-files.html", msg="Files have been uploaded successfully")
		#time.sleep(2)
		return redirect(url_for('views.yvariables'))
	return render_template("upload-files.html", msg="Please Choose a file")




@views.route('/yvariables', methods=["GET", "POST"])
def yvariables():
	class B(FlaskForm):
		list_of_files=list_of_files
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
	if request.method == 'POST':
		#yvariable = request.form["yvar"]
		#save_path = current_app.config["UPLOAD_PATH"]
		#file_text_name = "data.txt"
		#completeName = os.path.join(save_path, file_text_name)
		#outfile = open(completeName, 'w')
		#outfile.write(yvariable)
		#outfile.close()
		#return redirect(url_for("upload_files"))
		return render_template('yvariables.html', msg="Input Successful!", form=form)
	return render_template('yvariables.html', msg="Please Input the Y Variables for each file uploaded", form=form)
	#return f"{clist_to_execute}"
	#return f"{list_of_files}"
	#return f"{list_to_use}"

def r():
	b = request.form
	br = {x:b[x] for x in b if "a2-" in x}
	return render_template(b=br)



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


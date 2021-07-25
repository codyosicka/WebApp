from flask import Blueprint, render_template, request, flash, jsonify, current_app
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField
from .models import Note
from . import db
import json
import os
import paypalrestsdk


views = Blueprint('views', __name__, template_folder="templates")


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
	if request.method == 'POST':
		note = request.form.get('note')

		if len(note) < 1:
			flash('Note is too short!', category='error')
		else:
			new_note = Note(data=note, user_id=current_user.id)
			db.session.add(new_note)
			db.session.commit()
			flash('Note added!', category='success')

	return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
	note = json.loads(request.data) # request data is str from index.js and turns it into a python dictionary object so we can access the note id and then note is found
	noteId = note['noteId']
	note = Note.query.get(noteId)
	if note: # if note exists
		if note.user_id == current_user.id: # if user that is signed in owns this note...
			db.session.delete(note) # ...then note is deleted
			db.session.commit()
			
	return jsonify({})


@views.route('/upload_files', methods=["GET", "POST"])
def upload_files():
	files_list = []
	if request.method == 'POST':
		#yvariable = request.form["yvar"]
		#save_path = current_app.config["UPLOAD_PATH"]
		#file_text_name = "data.txt"
		#completeName = os.path.join(save_path, file_text_name)
		#outfile = open(completeName, 'w')
		#outfile.write(yvariable)
		#outfile.close()
		for f in request.files.getlist('file_name'):
			files_list.append(f.filename)
			f.save(os.path.join(current_app.config["UPLOAD_PATH"], f.filename))
		return render_template("upload-files.html", msg="Files has been uploaded successfully")
	return render_template("upload-files.html", msg="Please Choose a file")
	# NEED TO REDIRECT TO '/yvariables' AFTER SUBMIT



class B(FlaskForm):
	path = "C:\\Users\\Xaos\\Desktop\\Web App\\uploaded_files"
	directory = os.listdir(path)
	list_of_files = []
	if len(directory) != 0:
		for file in directory:
			list_of_files.append(file)
	#list_of_files_copy = list_of_files
	#for file in range(len(list_of_files)):
		#if ".csv" in list_of_files[file]:
			#list_of_files[file] = list_of_files[file].replace(".csv", "")
			#list_of_files[file] = list_of_files[file].replace("-", "_")
			#list_of_files[file] = list_of_files[file].replace("+", "_")
			#list_of_files[file] = list_of_files[file].replace("/", "_")
			#list_of_files[file] = list_of_files[file].replace("*", "_")
			#list_of_files[file] = list_of_files[file].replace("=", "_")
			#list_of_files[file] = list_of_files[file].replace("~", "_")
			#list_of_files[file] = list_of_files[file].replace(".", "_")
			#list_of_files[file] = list_of_files[file].replace(",", "_")
			#list_of_files[file] = list_of_files[file].replace(";", "_")
			#list_of_files[file] = list_of_files[file].replace(":", "_")
			#list_of_files[file] = list_of_files[file].replace("`", "_")
		#elif ".xlsx" in list_of_files[file]:
			#list_of_files[file] = list_of_files[file].replace(".xlsx", "")
			#list_of_files[file] = list_of_files[file].replace("-", "_")
			#list_of_files[file] = list_of_files[file].replace("+", "_")
			#list_of_files[file] = list_of_files[file].replace("*", "_")
			#list_of_files[file] = list_of_files[file].replace("=", "_")
			#list_of_files[file] = list_of_files[file].replace("~", "_")
			#list_of_files[file] = list_of_files[file].replace(".", "_")
			#list_of_files[file] = list_of_files[file].replace(",", "_")
			#list_of_files[file] = list_of_files[file].replace(";", "_")
			#list_of_files[file] = list_of_files[file].replace(":", "_")
			#list_of_files[file] = list_of_files[file].replace("`", "_")
		#file+=1
	clist_to_execute = []
	blist = []
	for filecopy in range(len(list_of_files)):
		blist.append('b{}'.format(filecopy))
		#clist_to_execute.append('{} = 0'.format(list_of_files[filename]))
		#clist_to_execute.append('{} = StringField({})'.format(list_of_files[filename], list_of_files_copy[filecopy]))
		#clist_to_execute.append('b1 = 0')
		#clist_to_execute.append('b1 = StringField({})'.format(list_of_files_copy[filecopy]))
		filecopy+=1
	for filecopy in range(len(list_of_files)):
		clist_to_execute.append('{} = StringField("{}")'.format(blist[filecopy], list_of_files[filecopy]))
		filecopy+=1
	for exe in clist_to_execute:
		exec(exe)
	#for file in list_of_files_copy:
		#b1 = StringField("{}".format(file))
	#b2 = StringField("B2 Label")
	#b3 = StringField("B3 Label")

'''class B(FlaskForm):
	b1 = StringField("B1 Label")'''

class A(FlaskForm):
	a1 = StringField("A1 Label")
	a2 = FieldList(FormField(B), min_entries=1)
	s = SubmitField("Submit Y Variables")



@views.route('/yvariables', methods=["GET", "POST"])
def yvariables():
	form = A()
	if request.method == 'POST':
		#yvariable = request.form["yvar"]
		#save_path = current_app.config["UPLOAD_PATH"]
		#file_text_name = "data.txt"
		#completeName = os.path.join(save_path, file_text_name)
		#outfile = open(completeName, 'w')
		#outfile.write(yvariable)
		#outfile.close()
		return render_template('yvariables.html', msg="Y Variables Input has been uploaded successfully")
	return render_template('yvariables.html', msg="Please Input the Y Variables for each file uploaded", form=form)

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


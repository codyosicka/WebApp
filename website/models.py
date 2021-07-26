from . import db
from flask_login import UserMixin
from sqlalchemy import func
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField
import os


class Note(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	data = db.Column(db.String(10000))
	date = db.Column(db.DateTime(timezone=True), default=func.now())
	user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # one to many relationship so one user has many notes


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True) # sets a key
	email = db.Column(db.String(150), unique=True) # unique makes it so that no two Users can have the same email
	password = db.Column(db.String(150))
	first_name = db.Column(db.String(150))
	notes = db.relationship('Note') # everytime a note is created, add into a User-notes relationship that note ID; this relationship field will be like a list


class B(FlaskForm):
	path = "C:\\Users\\Xaos\\Desktop\\Web App\\uploaded_files"
	directory = os.listdir(path)
	global listf
	listf = []
	if len(directory) != 0:
		for file in directory:
			listf.append(file)
	global list_to_use
	#list_to_use = list(set(list_of_files).intersection(listf))
	global clist_to_execute
	clist_to_execute = []
	blist = []
	for file in range(len(listf)):
		blist.append('b{}'.format(file))
		file+=1
	for file in range(len(listf)):
		clist_to_execute.append('{} = StringField("{}")'.format(blist[file], listf[file]))
		file+=1
	for exe in clist_to_execute:
		exec(exe)


class A(FlaskForm):
	a2 = FieldList(FormField(B), min_entries=1)
	s = SubmitField("Submit Y Variables")
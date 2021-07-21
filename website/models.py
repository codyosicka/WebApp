from . import db
from flask_login import UserMixin
from sqlalchemy import func


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

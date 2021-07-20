from flask import Blueprint, render_template, request, flash, jsonify, current_app
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import os

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
	if request.method == 'POST':
		for f in request.files.getlist('file_name'):
			#f = request.files['file_name']
			f.save(os.path.join(current_app.config["UPLOAD_PATH"], f.filename))
		return render_template("upload-files.html", msg="Files has been uploaded successfully")
	return render_template("upload-files.html", msg="Please Choose a file")



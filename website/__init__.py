import flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import paypalrestsdk

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'a'
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
	app.config["UPLOAD_PATH"] = 'C:\\Users\\Buff14\\Desktop\\uploaded_files'
	db.init_app(app)

	paypalrestsdk.configure({
	"mode": "sandbox", # sandbox or live
	"client_id": "AYbnfU8Pj_yiF8ULPsCiU_R7vqDvIZfFP1s0qWUrokJM5W5ON9ypx56X4mqqzcrUKmrT_eZmvTqkGpop",
	"client_secret": "EE6mphrPS35PzRXwE1ZtsWWHMznLhBxrKh5vIxHtuxcCChGc0PpD9SELqpZgmenoGuLEDGR-CxvyRZ6W"
	})

	from .views import views
	from .auth import auth

	app.register_blueprint(views, url_prefix='/')
	app.register_blueprint(auth, url_prefix='/')

	from .models import User, Note

	create_database(app)

	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))

	return app

def create_database(app):
	if not path.exists('website/' + DB_NAME):
		db.create_all(app=app)
		print('Created Database!')
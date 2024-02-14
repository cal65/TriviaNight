from flask import Flask, render_template, request, jsonify, Blueprint
import requests


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
from application.data import db
db.init_app(app)

app.register_blueprint(Blueprint)


if __name__ == '__main__':
	app.run(port=9999)
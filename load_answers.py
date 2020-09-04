from flask import Flask, render_template, request, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__) 

app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
db = SQLAlchemy(app)

@app.route("/hi") 
def welcome(): 
    return "Hey whatsup" 

@app.route("/")
def home():
  return render_template("base.html")

@app.route('/json-example', methods=['POST']) #GET requests will be blocked
def json_example():
    return 'Todo...'

#res = requests.post('http://127.0.0.1:9999/create-question/s9x93/what-is-the-country-code-of-switzerland', 
#	json={"question_id":"s9x93", "round_id":"hgj394zl02", "question": "what is the country code of switzerland?",
#	"author_id": "n92ne8s0x1"})

@app.route("/create-question/", methods=['POST', 'GET'])
def add_question():
	content = request.get_json()
	print (content['question'], flush=True)
	question = content['question']
	name = content['name']
	#return str(question_id)
	return (f'The question is {question} from {name}')


class questions(db.Model):
   round_id = db.Column('round_id', db.String(8), primary_key = True)
   question_id = db.Column(db.String(8), unique = True)
   question = db.Column(db.String(2000))  
   author_id = db.Column(db.String(8))

class responses(db.Model):
   response_id = db.Column('response_id', db.Integer, primary_key = True)
   session_id = db.Column(db.String(8))
   question_id = db.Column(db.String(8))  
   team_id = db.Column(db.String(8))
   round_id = db.Column(db.String(10))
   response = db.Column(db.String(1000))

class answers(db.Model):
   answer_id = db.Column('answer_id', db.Integer, primary_key = True)
   question_id = db.Column(db.String(8), unique = False)
   answer = db.Column(db.String(100))

class game(db.Model):
	gameid = db.Column('game_id', db.String, primary_key = True)

def __init__(self, name, city, addr,pin):
   self.name = name
   self.city = city
   self.addr = addr
   self.pin = pin

app.run(port=9999)
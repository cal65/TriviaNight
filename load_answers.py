from flask import Flask, render_template, request, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
import logging
from db import Questions, Responses
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__) 


@app.route("/hi") 
def welcome(): 
    return "Hey whatsup" 

@app.route("/")
def home():
  	return render_template("landing.html")

@app.route("/question-form")
def question_form():
  	return render_template("form-page.html")

@app.route('/return-all')
def return_all():
	all_questions = Questions.query.all()
	return '\n'.join([q.question for q in all_questions])    

@app.route('/<user_id>')
def user(user_id):
	return f'<h1>{user_id}</h1>'

@app.route('/load-question', methods=['POST'])
def load_questions():
	user = request.form['user']
	#session.query(user).filter(user.author_id==user)
	return jsonify({'question': "Question by " + user + ": What is this?"})

@app.route("/create-question", methods=['POST', 'GET'])
def add_question():
	if request.method == 'POST':
		# print ("HI", flush=True)
		content = request.get_json(force=True)
		question = content['question']
		author_id = content['author_id']
		question_id = content['question_id']
		round_id = content['round_id']
		new_question = Questions(question_id=question_id, 
			question=question, 
			author_id=author_id,
			round_id=round_id,
			)
		db.session.add(new_question)
		db.session.commit()
		return author_id + ": " + question
	else:
		return 'Sorry: ' + str(request)

app.run(port=9999)
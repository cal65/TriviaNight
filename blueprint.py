from flask import Blueprint, render_template, request, abort, Flask, jsonify
from jinja2 import TemplateNotFound
from flask_sqlalchemy import SQLAlchemy


blueprint = Blueprint('simple_page', __name__,
                        template_folder='templates')

@blueprint.route('/', defaults={'page': 'index'})
@blueprint.route('/<page>')
def show(page):
    try:
        return render_template('pages/%s.html' % page)
    except TemplateNotFound:
        abort(404)

@blueprint.route("/hi") 
def welcome(): 
    return "Hey whatsup" 

@blueprint.route("/")
def home():
  	return render_template("landing.html")

@blueprint.route("/question-form")
def question_form():
  	return render_template("form-page.html")

@blueprint.route('/return-all')
def return_all():
	all_questions = Questions.query.all()
	return '\n'.join([q.question for q in all_questions])    

@blueprint.route('/<user_id>')
def user(user_id):
	return f'<h1>{user_id}</h1>'

@blueprint.route('/load-question', methods=['POST'])
def load_questions():
	#session.query(user).filter(user.author_id==user)
	user = request.form['user']
	if type(user) == str and len(user) > 0:
			return jsonify({'question': "Question by " + user + ": What is this?"})
		
	return jsonify({'error' : 'Missing data!'})

@blueprint.route("/create-question", methods=['POST', 'GET'])
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



if __name__ == '__main__':
	app = Flask(__name__)
	app.register_blueprint(blueprint)
	app.run(port=9999)
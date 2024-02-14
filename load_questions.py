from flask import Flask, render_template, request, jsonify
import requests

def load_questions():
	"""
	Load questions from the API
	:return:
	"""
	return render_template('q.html', question= "What is this?")
from flask import Flask, jsonify
from app import app

@app.route('/indbetaling', methods=['POST'])
def create_indbetaling():
	hello_response = {
		'response' : 1
	}

	return jsonify(hello_response)
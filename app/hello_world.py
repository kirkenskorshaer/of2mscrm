from flask import Flask, jsonify
from app import app

@app.route('/hello_world', methods=['GET'])
def hello_world():
	hello_response = {
		'response' : 1
	}

	return jsonify(hello_response)
from flask import Flask, jsonify, request
from app import app

@app.route('/echo', methods=['GET'])
def echo_get():
	hello_response = {
		'response' : 1
	}

	return jsonify(hello_response)

@app.route('/echo', methods=['POST','PATCH','PUT', 'DELETE'])
def echo():

	return jsonify(request.json)


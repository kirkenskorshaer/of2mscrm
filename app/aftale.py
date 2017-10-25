from flask import jsonify
from app import app


@app.route('/aftale', methods=['POST'])
def create_aftale():
	aftale_response = {
		'contact_id': '',
		'aftale_id': '',
		'error': None
	}

	return jsonify(aftale_response)


@app.route('/aftale', methods=['PUT'])
def update_aftale():
	aftale_response = {
		'error': None
	}

	return jsonify(aftale_response)

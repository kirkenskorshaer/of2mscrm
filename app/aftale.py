from flask import jsonify, request
from app import app
from .schema import schema_validation, aftale_post_schema, aftale_put_schema


@app.route('/aftale', methods=['POST'])
def create_aftale():
	aftale_response = {
		'contact_id': '',
		'aftale_id': '',
		'error': None
	}

	error, aftale_request = schema_validation.validate_json_schema(aftale_post_schema.get_schema(), request)
	if error is not None:
		aftale_response['error'] = error
		return jsonify(aftale_response)
	return jsonify(aftale_response)


@app.route('/aftale', methods=['PUT'])
def update_aftale():
	aftale_response = {
		'error': None
	}

	error, aftale_request = schema_validation.validate_json_schema(aftale_put_schema.get_schema(), request)

	if error is not None:
		aftale_response['error'] = error
		return jsonify(aftale_response)

	return jsonify(aftale_response)

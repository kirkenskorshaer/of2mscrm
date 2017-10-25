from flask import jsonify, request
from .schema import schema_validation, indbetaling_post_schema, indbetaling_patch_schema
from app import app
from app import config_data
from app import oauth_connect


@app.route('/indbetaling', methods=['POST'])
def create_indbetaling():
	config = config_data.ConfigData()

	indbetaling_response = {
		'indbetaling_id': None,
		'error': None
	}

	error, indbetaling_request = schema_validation.validate_json_schema(indbetaling_post_schema.get_schema(), request)
	if error is not None:
		indbetaling_response['error'] = error
		return jsonify(indbetaling_response)

	indbetaling_response['indbetaling_id'], error = _create_indbetaling(indbetaling_request, config)

	return jsonify(indbetaling_response)


@app.route('/indbetaling', methods=['PATCH'])
def update_indbetaling():
	config = config_data.ConfigData()

	indbetaling_response = {
		'error': None
	}

	error, indbetaling_request = schema_validation.validate_json_schema(indbetaling_patch_schema.get_schema(), request)
	if error is not None:
		indbetaling_response['error'] = error
		return jsonify(indbetaling_response)

	returned_id, indbetaling_response['error'] = _update_indbetaling(indbetaling_request, config)

	if returned_id != indbetaling_request['indbetaling_id']:
		indbetaling_response['error'] = 'id (' + indbetaling_request['indbetaling_id'] + ') is not (' + repr(returned_id) + ')'

	return jsonify(indbetaling_response)


def _create_indbetaling(indbetaling_request, config):
	query = "new_indbetalings?$select=new_indbetalingid"

	crm_indbetaling = {
		'nrq_tekst': indbetaling_request['indbetaling']['status']
	}

	result_json, error = oauth_connect.connector.execute_post_query(query, crm_indbetaling, config)

	if error is not None:
		return None, error

	try:
		return result_json['new_indbetalingid'], None
	except KeyError:
		return None, repr(result_json)


def _update_indbetaling(indbetaling_request, config):
	query = 'new_indbetalings(' + indbetaling_request['indbetaling_id'] + ')?$select=new_indbetalingid'

	crm_indbetaling = {
		'nrq_tekst': indbetaling_request['status']
	}

	result_json, error = oauth_connect.connector.execute_patch_query(query, crm_indbetaling, config)

	if error is not None:
		return None, error

	try:
		return result_json['new_indbetalingid'], None
	except KeyError:
		return None, repr(result_json)

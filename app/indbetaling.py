from flask import jsonify, request
from .schema import schema_validation, indbetaling_post_schema
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


def _create_indbetaling(indbetaling_request, config):
	query = "new_indbetalings?$select=new_indbetalingid"

	crm_indbetaling = {
		'nrq_tekst': indbetaling_request['indbetaling']['status']
		# 'aftale_id': indbetaling_request['aftale']['aftale_id']
	}

	result_json, error = oauth_connect.connector.execute_post_query(query, crm_indbetaling, config)

	if error is not None:
		return None, error

	try:
		return result_json['new_indbetalingid'], None
	except KeyError:
		return None, repr(result_json)

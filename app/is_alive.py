import requests
from app import app
from app import config_data
from app import oauth_connect
from flask import jsonify
from json.decoder import JSONDecodeError


@app.route('/is_alive', methods=['GET'])
def is_alive():
	query = "/contacts?$select=contactid&$top=1"
	config = config_data.ConfigData()
	connector = oauth_connect.OauthConnect()

	headers, header_error = connector.make_request_headers(config)

	is_alive_response = {
		'is_alive': False,
		'error': header_error,
		'proof': ''
	}

	if headers is None:
		return jsonify(is_alive_response)

	crm_response = requests.get(config.api_url + query, headers=headers)

	try:
		crm_results = crm_response.json()
		is_alive_response['proof'] = 'there is a contact with id = ' + crm_results['value'][0]['contactid']
		is_alive_response['is_alive'] = True
	except JSONDecodeError as message:
		is_alive_response['is_alive'] = False
		is_alive_response['error'] = repr(crm_response)
	except KeyError as message:
		is_alive_response['is_alive'] = False
		is_alive_response['error'] = repr(crm_response)

	return jsonify(is_alive_response)

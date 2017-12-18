from flask import jsonify, request
from app import app
from .schema import schema_validation, aftale_post_schema, aftale_patch_schema
from app import config_data
from app import oauth_connect


@app.route('/aftale', methods=['POST'])
def create_aftale():
	config = config_data.ConfigData()

	aftale_response = {
		'contact_id': '',
		'aftale_id': '',
		'error': None
	}

	error, aftale_request = schema_validation.validate_json_schema(aftale_post_schema.get_schema(), request)
	if error is not None:
		aftale_response['error'] = error
		return jsonify(aftale_response)

	aftale_response['contact_id'], error = _get_contact_id_from_crm(aftale_request, config)
	if error is not None:
		aftale_response['error'] = error
		return jsonify(aftale_response)

	if aftale_response['contact_id'] is None:
		aftale_response['contact_id'], aftale_response['error'] = _create_new_contact(aftale_request, config)

	if aftale_response['error'] is None:
		aftale_response['aftale_id'], aftale_response['error'] = _create_aftale(aftale_request, config)

	if aftale_response['error'] is None:
		oauth_connect.connector.associate('nrq_bidragsaftales', aftale_response['aftale_id'], 'nrq_contact_nrq_bidragsaftale_Bidragyder', 'contacts', aftale_response['contact_id'], config)

	return jsonify(aftale_response)


@app.route('/aftale', methods=['PATCH'])
def update_aftale():
	config = config_data.ConfigData()

	aftale_response = {
		'error': None
	}

	error, aftale_request = schema_validation.validate_json_schema(aftale_patch_schema.get_schema(), request)
	if error is not None:
		aftale_response['error'] = error
		return jsonify(aftale_response)

	returned_id, aftale_response['error'] = _update_aftale(aftale_request, config)

	if returned_id != aftale_request['aftale_id']:
		aftale_response['error'] = 'id (' + aftale_request['aftale_id'] + ') is not (' + repr(returned_id) + ')'

	return jsonify(aftale_response)


def _update_aftale(aftale_request, config):
	query = 'nrq_bidragsaftales(' + aftale_request['aftale_id'] + ')?$select=nrq_bidragsaftaleid'

	crm_aftale = {
		'nrq_frekvens': 'changed'
	}

	result_json, error = oauth_connect.connector.execute_patch_query(query, crm_aftale, config)
	if error is not None:
		return None, repr(result_json)

	try:
		return result_json['nrq_bidragsaftaleid'], None
	except KeyError:
		return None, repr(result_json)


def _get_contact_id_from_crm(aftale_request, config):
	query = "contacts?$select=contactid&$filter=firstname eq '" + aftale_request['contact']['firstname'] + "' and emailaddress1 eq '" + aftale_request['contact']['email'] + "'&$top=1"

	result_json, error = oauth_connect.connector.execute_get_query(query, config)

	if error is not None:
		return None, error

	if len(result_json['value']) == 0:
		return None, None

	return result_json['value'][0]['contactid'], None


def _create_new_contact(aftale_request, config):
	query = "contacts?$select=contactid"

	crm_contact = {
		'firstname': aftale_request['contact']['firstname'],
		'mobilephone': aftale_request['contact']['phone'],
		'address1_line1': aftale_request['contact']['address'],
		'address1_line2': aftale_request['contact']['address_line_2'],
		'address1_city': aftale_request['contact']['city'],
		'address1_country': aftale_request['contact']['country'],
		'new_cprnr': aftale_request['contact']['cpr'],
		'emailaddress1': aftale_request['contact']['email'],
		'lastname': aftale_request['contact']['lastname'],
		'middlename': aftale_request['contact']['middlename'],
		# 'permissions': aftale_request['contact']['permissions'],
		'address1_postalcode': aftale_request['contact']['postcode']
	}

	result_json, error = oauth_connect.connector.execute_post_query(query, crm_contact, config)

	if error is not None:
		return None, error

	try:
		return result_json['contactid'], None
	except KeyError:
		return None, repr(result_json)


def _create_aftale(aftale_request, config):
	query = "nrq_bidragsaftales?$select=nrq_bidragsaftaleid"
	# query = "nrq_bidragsaftale"

	crm_aftale = {
		# 'accountno': aftale_request['aftale']['accountno'],
		'nrq_startdato': _get_date_from_value(aftale_request['aftale']['agreement_start']),
		'nrq_beloeb': aftale_request['aftale']['amount'],
		'nrq_type': aftale_request['aftale']['amount_type'],
		# 'currency': aftale_request['aftale']['currency'],
		# 'date': aftale_request['aftale']['date'],
		'nrq_slutdato': _get_date_from_value(aftale_request['aftale']['date_end']),
		'nrq_frekvens': aftale_request['aftale']['frequency'],
		# 'gateway': aftale_request['aftale']['gateway'],
		# 'media': aftale_request['aftale']['media'],
		# 'message': aftale_request['aftale']['message'],
		'nrq_betalingsform': aftale_request['aftale']['paymenttype'],
		# 'phone': aftale_request['aftale']['phone'],
		# 'project': aftale_request['aftale']['project'],
		# 'sms_keyword': aftale_request['aftale']['sms_keyword']
		# 'sortno': aftale_request['aftale']['sortno'],
		# 'state': aftale_request['aftale']['state'],
		# 'subscriptionid': aftale_request['aftale']['subscriptionid'],
	}

	result_json, error = oauth_connect.connector.execute_post_query(query, crm_aftale, config)

	if error is not None:
		return None, error

	try:
		return result_json['nrq_bidragsaftaleid'], None
	except KeyError:
		return None, repr(result_json)


def _get_date_from_value(input):
	if input is None or input == '':
		return None

	return input


def _update_aftale_state(aftale_request, aftale_response):
	pass

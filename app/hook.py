from flask import jsonify
from app import app
from app import config_data
from app import oauth_connect


@app.route('/hook/<action>/<of_id>/', methods=['GET'])
def receive_hook_aftale(action, of_id):
	config = config_data.ConfigData()
	#entity_id, error_entity_id = get_entity_id(config, entity_name, crm_id_name, of_id_name, of_id)
	
	#hook_response = {
	#	'entity_id' : repr(entity_id)
	#}

	hook_response = {}

	# if entity_id is None:
	#	return jsonify(hook_response)
	
	error = activate_action(config, hook_response, action, of_id)

	if error is not None:
		hook_response['error'] = repr(error)

	return jsonify(hook_response)

def activate_action(config, hook_response, action, of_id):
	# query = 'workflows(' + workflow + ')/Microsoft.Dynamics.CRM.ExecuteWorkflow'
	# query = entity_name + '(' + entity_id + ')/Microsoft.Dynamics.CRM.' + action
	query = action

	crm_hook = {
		'of_aftale': of_id
	}
	
	if config.production is False:
		hook_response['activate_action_query'] = repr(query)
	
	result_json, error = oauth_connect.connector.execute_post_query(query, crm_hook, config)
	
	if config.production is False:
		hook_response['activate_action_result'] = repr(result_json)
	
	return error

def get_entity_id(config ,entity_name, crm_id_name, of_id_name, of_id):
	query = entity_name + "?$select=" + crm_id_name + "&$filter=" + of_id_name + " eq '" + of_id + "'&$top=1"
	
	result_json, error = oauth_connect.connector.execute_get_query(query, config)
	
	if error is not None:
		return None, error
	
	if 'value' not in result_json:
		return None, None
	
	if len(result_json['value']) == 0:
		return None, None
	
	return result_json['value'][0][crm_id_name], None












	
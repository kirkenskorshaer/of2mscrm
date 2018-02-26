from flask import jsonify
from app import app
from app import config_data
from app import oauth_connect


@app.route('/hook/<action>/<of_id>/', methods=['GET'])
def receive_hook_aftale(action, of_id):
	config = config_data.ConfigData()

	hook_response = {}

	error = activate_action(config, hook_response, action, of_id)

	if error is not None:
		hook_response['error'] = repr(error)

	return jsonify(hook_response)


def activate_action(config, hook_response, action, of_id):
	query = action

	crm_hook = {
		'of_id': of_id
	}

	if config.production is False:
		hook_response['activate_action_query'] = repr(query)

	result_json, error = oauth_connect.connector.execute_post_query(query, crm_hook, config)

	if config.production is False:
		hook_response['activate_action_result'] = repr(result_json)

	return error

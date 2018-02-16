from flask import request


class ConfigData():
	production = None
	token_endpoint = "https://login.microsoftonline.com/867f533d-343a-47e6-a16c-1e928b5763d6/oauth2/token"
	authorization_endpoint = 'https://login.microsoftonline.com/867f533d-343a-47e6-a16c-1e928b5763d6'
	application_id = '0330c4fe-6dd8-4766-b0fa-6efe5afaa615'
	api_url = None
	base_url = None

	def __init__(self):
		self.production = False
		self.workflow_test = '31339296-EDB7-4913-A5B3-B1A71794E072'

		if request.headers is not None and 'environment' in request.headers and request.headers['environment'] == 'prod':
			self.production = True

		if self.production is True:
			self.api_url = "https://kkh.api.crm4.dynamics.com/api/data/v8.2/"
			self.base_url = "https://kkh.crm4.dynamics.com"
		else:
			self.api_url = "https://kkhdev.api.crm4.dynamics.com/api/data/v8.2/"
			self.base_url = "https://kkhdev.crm4.dynamics.com"

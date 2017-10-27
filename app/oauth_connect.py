from adal import AuthenticationContext
from flask import request


class OauthConnect(object):

	def make_request_headers(self, config):
		if request.headers is None:
			return None, 'No Headers'

		if 'authorization' in request.headers:
			authorization = request.headers['authorization']
		else:
			return None, 'No authorization header'

		if authorization.count(';') != 1:
			return None, 'Invalid authorization header'

		authorization_split = authorization.split(';')

		username = authorization_split[0]
		password = authorization_split[1]

		auth_context = AuthenticationContext(config.authorization_endpoint, api_version=None)
		token_response = auth_context.acquire_token_with_username_password(config.base_url, username, password, config.application_id)

		access_token = ''

		try:
			access_token = token_response['accessToken']
		except(KeyError):
			return None, repr(token_response)

		if(access_token != ''):
			crm_request_headers = {
				'Authorization': 'Bearer ' + access_token,
				'OData-MaxVersion': '4.0',
				'OData-Version': '4.0',
				'Accept': 'application/json',
				'Content-Type': 'application/json; charset=utf-8',
				'Prefer': 'odata.maxpagesize=500',
				'Prefer': 'odata.include-annotations=OData.Community.Display.V1.FormattedValue'
			}

			return crm_request_headers, None

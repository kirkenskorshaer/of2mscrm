from adal import AuthenticationContext
from flask import request
from datetime import datetime, timedelta


class OauthConnect(object):
	expires_on = None
	access_token = None
	token_in_returned_header_is_valid_for_at_least_this_many_seconds = 10

	def get_request_headers(self, config):
		max_alowed_datetime = datetime.now() - timedelta(seconds=self.token_in_returned_header_is_valid_for_at_least_this_many_seconds)
		if self.expires_on is not None and max_alowed_datetime < self.expires_on:
			return self._create_header_from_token(), None

		return self._make_request_headers(config)

	def _make_request_headers(self, config):
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

		try:
			self.access_token = token_response['accessToken']
			self.expires_on = datetime.strptime(token_response['expiresOn'], '%Y-%m-%d %H:%M:%S.%f')
		except(KeyError):
			return None, repr(token_response)

		return self._create_header_from_token(), None

	def _create_header_from_token(self):
		return {
			'Authorization': 'Bearer ' + self.access_token,
			'OData-MaxVersion': '4.0',
			'OData-Version': '4.0',
			'Accept': 'application/json',
			'Content-Type': 'application/json; charset=utf-8',
			'Prefer': 'odata.maxpagesize=500',
			'Prefer': 'odata.include-annotations=OData.Community.Display.V1.FormattedValue'
		}

connector = OauthConnect()

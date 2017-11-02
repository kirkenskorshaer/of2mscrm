import requests
from adal import AuthenticationContext
from flask import request
from datetime import datetime, timedelta
import json.decoder


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
			'Prefer': 'odata.include-annotations=OData.Community.Display.V1.FormattedValue',
			'Prefer': 'return=representation'
		}

	def execute_get_query(self, query, config):
		return self._execute_query(query, data=None, config=config, method=requests.get)

	def execute_post_query(self, query, data, config):
		return self._execute_query(query, data=data, config=config, method=requests.post)

	def execute_put_query(self, query, data, config):
		return self._execute_query(query, data=data, config=config, method=requests.put)

	def _execute_query(self, query, data, config, method):
		headers, header_error = self.get_request_headers(config)

		if headers is None:
			None, header_error

		url = config.api_url + query
		crm_response = None
		if data is None:
			crm_response = method(url, headers=headers)
		else:
			crm_response = method(url, json=data, headers=headers)

		crm_json = None
		try:
			crm_json = crm_response.json()
		except json.decoder.JSONDecodeError as message:
			return None, repr(crm_response)

		return crm_json, None

connector = OauthConnect()

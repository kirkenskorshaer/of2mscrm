import os
import unittest

#from config import basedir
from app import app


class TestCase(unittest.TestCase):
	def setUp(self):
		#app.config['Testing'] = True
		self.app = app.test_client()

	def tearDown(self):
		pass

	def test_fail(self):
		print('fail')
		assert 1 == 2

	def test_success(self):
		assert 3 == 3

	def test_create_url(self):
		client_id = '0e44ba55-f56e-4c9c-a952-3a0d600be6e6'
		tenant_id = '867f533d-343a-47e6-a16c-1e928b5763d6'
		redirect_url = 'https%3A%2F%2Fof2mscrmtest.azurewebsites.net%2F'
		url = 'https://login.microsoftonline.com/' + tenant_id + '/oauth2/authorize?client_id=' + client_id + '&redirect_uri=' + redirect_url + '&response_type=code&prompt=admin_consent'
		print(url)


if __name__ == '__main__':
	unittest.main()

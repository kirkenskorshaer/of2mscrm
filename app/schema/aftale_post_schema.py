def get_schema():
	return {
		'type': 'object',
		'properties': {
			'aftale':
			{
				'type': 'object',
				'properties':
				{
					'accountno': {'type': 'integer'},
					'agreement_start': {'type': 'string'},
					'amount': {'type': 'integer'},
					'amount_type': {'type': 'string'},
					'currency': {'type': 'string'},
					'date': {'type': 'string'},
					'date_end': {'type': 'string'},
					'frequency': {'type': 'string'},
					'gateway': {'type': 'string'},
					'media': {'type': 'string'},
					'message': {'type': 'string'},
					'paymenttype': {'type': 'string'},
					'phone': {'type': 'string'},
					'project': {'type': 'string'},
					'sms_keyword': {'type': 'string'},
					'sortno': {'type': 'string'},
					'state': {'type': 'string'},
					'subscriptionid': {'type': 'string'}
				},
				'required': ['accountno', 'agreement_start', 'amount', 'amount_type', 'currency', 'date', 'date_end', 'frequency', 'gateway', 'media', 'message', 'paymenttype', 'phone', 'project', 'sms_keyword', 'sortno', 'state', 'subscriptionid']
			},
			'contact':
			{
				'type': 'object',
				'properties':
				{
					'phone': {'type': 'string'},
					'address': {'type': 'string'},
					'address_line_2': {'type': 'string'},
					'city': {'type': 'string'},
					'country': {'type': 'string'},
					'cpr': {'type': 'string'},
					'email': {'type': 'string'},
					'firstname': {'type': 'string'},
					'lastname': {'type': 'string'},
					'middlename': {'type': 'string'},
					'permissions': {'type': 'string'},
					'postcode': {'type': 'string'}
				},
				'required': ['phone', 'address', 'address_line_2', 'city', 'country', 'cpr', 'email', 'firstname', 'lastname', 'middlename', 'permissions', 'postcode']
			}
		},
		'required': ['aftale', 'contact']
	}

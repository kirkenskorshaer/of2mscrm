def get_schema():
	return {
		'type': 'object',
		'properties':
		{
			'aftale_id': {'type': 'string'},
			'state': {'type': 'string'},
			'gateway_fejlkode': {'type': 'string'}
		},
		'required': ['aftale_id', 'gateway_fejlkode']
	}

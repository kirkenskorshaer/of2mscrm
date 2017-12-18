def get_schema():
	return {
		'type': 'object',
		'properties': {
			'aftale':
			{
				'type': 'object',
				'properties':
				{
					'aftale_id': {'type': 'string'},
					'charge_ts': {'type': 'string'},
					'gateway_fejlkode': {'type': 'string'}
				},
				'required': ['aftale_id', 'charge_ts', 'gateway_fejlkode']
			},
			'indbetaling':
			{
				'type': 'object',
				'properties':
				{
					'status': {'type': 'string'}
				},
				'required': ['status']
			}
		},
		'required': ['aftale', 'indbetaling']
	}

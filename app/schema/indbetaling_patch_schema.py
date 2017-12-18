def get_schema():
	return {
		'type': 'object',
		'properties':
		{
			'indbetaling_id': {'type': 'string'},
			'status': {'type': 'string'},
			'gateway_fejlkode': {'type': 'string'},
			'dato': {'type': 'string'}
		},
		'required': ['indbetaling_id', 'status', 'gateway_fejlkode', 'dato']
	}

from jsonschema import validate
from jsonschema.exceptions import ValidationError


def validate_json_schema(schema, request):
	try:
		current_request = request.json
	except KeyError:
		return 'not json document', None

	try:
		validate(current_request, schema)
	except ValidationError as error:
		return repr(error), current_request

	return None, current_request

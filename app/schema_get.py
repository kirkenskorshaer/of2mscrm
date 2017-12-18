from app import app
from .schema import *
from flask import jsonify


@app.route('/schema/indbetaling/post', methods=['GET'])
def get_indbetaling_post_schema():
	schema_response = indbetaling_post_schema.get_schema()
	return jsonify(schema_response)


@app.route('/schema/indbetaling/patch', methods=['GET'])
def get_indbetaling_patch_schema():
	schema_response = indbetaling_patch_schema.get_schema()
	return jsonify(schema_response)


@app.route('/schema/aftale/post', methods=['GET'])
def get_aftale_post_schema():
	schema_response = aftale_post_schema.get_schema()
	return jsonify(schema_response)


@app.route('/schema/aftale/patch', methods=['GET'])
def get_aftale_put_schema():
	schema_response = aftale_patch_schema.get_schema()
	return jsonify(schema_response)

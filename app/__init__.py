from flask import Flask, jsonify

app = Flask(__name__)

wsgi_app = app.wsgi_app

from app import views

if __name__ == '__main__':
	app.run()

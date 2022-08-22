import os
from flask import Flask
from flask_cors import CORS
from database.config import configDatabase, createTables
from routers import setupRouters
from middlewares.auth import AuthMiddleware
from middlewares.manager import MiddlewareManager

port = int(os.environ.get('PORT', 5000))
debug = eval(os.environ.get('DEBUG', "False"))


app = Flask(__name__, instance_relative_config=True)
CORS(app)


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response


app.wsgi_app = MiddlewareManager(app)
app.wsgi_app.add_middleware(AuthMiddleware)

createTables(configDatabase(app))
setupRouters(app)

app.run(debug=debug, host='0.0.0.0', port=port)

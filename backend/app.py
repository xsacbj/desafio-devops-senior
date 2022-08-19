import os
from flask import Flask
from flask_cors import CORS
from database.config import configDatabase, createTables
from routers import setupRouters
from middlewares.auth import AuthMiddleware
from middlewares.manager import MiddlewareManager

port = int(os.environ.get('PORT', 5000))
debug = eval(os.environ.get('DEBUG', "False"))
# origins = [
#   'http://localhost:3000',  # React
#   'http://127.0.0.1:3000',  # React
#   'http://0.0.0.0:3000',  # React
# ]


app = Flask(__name__, instance_relative_config=True)
# app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
# app.config['CORS_HEADERS'] = ['Content-Type', 'Authorization']
# CORS(app, supports_credentials=True, resources={r"/*": {"origins": origins}})
CORS(app)
app.wsgi_app = MiddlewareManager(app)
app.wsgi_app.add_middleware(AuthMiddleware)

createTables(configDatabase(app))
setupRouters(app)

app.run(debug=debug, host='0.0.0.0', port=port)

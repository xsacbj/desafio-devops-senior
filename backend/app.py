import os
from flask import Flask
from database.config import configDatabase, createTables
from routers import setupRouters
from middlewares.auth import AuthMiddleware
from middlewares.manager import MiddlewareManager

port = int(os.environ.get('PORT', 5000))
debug = eval(os.environ.get('DEBUG', "False"))

app = Flask(__name__, instance_relative_config=True)

app.wsgi_app = MiddlewareManager(app)
app.wsgi_app.add_middleware(AuthMiddleware)

createTables(configDatabase(app))
setupRouters(app)

app.run(debug=debug, host='0.0.0.0', port=port)

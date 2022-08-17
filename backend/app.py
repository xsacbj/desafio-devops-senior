import os
from flask import Flask
from database.config import configDatabase, createTables
from routers import setupRouters

port = int(os.environ.get('PORT', 5000))
debug = eval(os.environ.get('DEBUG', "False"))

app = Flask(__name__, instance_relative_config=True)

createTables(configDatabase(app))
setupRouters(app)

app.run(debug=debug, host='0.0.0.0', port=port)

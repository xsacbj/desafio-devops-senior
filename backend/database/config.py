import json
from flask_sqlalchemy import SQLAlchemy
from .models.__init__ import createModels

def configDatabase(app):
    with open('settings.json') as f:
        settings = json.load(f)
    user, password, host, port, dbname = settings['db']['user'], settings['db']['password'], settings['db']['host'], settings['db']['port'], settings['db']['dbname']

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{user}:{password}@{host}:{int(float(port))}/{dbname}'
    return SQLAlchemy(app)

def createTables(db):
    createModels(db)

    db.create_all()
    db.session.commit()
    return True
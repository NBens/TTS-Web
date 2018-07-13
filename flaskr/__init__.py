from flask import Flask
import flaskr.settings
import flaskr.auth
import flaskr.search
import flaskr.main
import flaskr.manage

from flaskr.db import Database


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.config['UPLOAD_FOLDER'] = "uploads/"
app.register_blueprint(flaskr.main.mod)
app.register_blueprint(flaskr.settings.mod)
app.register_blueprint(flaskr.auth.mod)
app.register_blueprint(flaskr.search.mod)
app.register_blueprint(flaskr.manage.mod)


database = Database(
    app.config['DATABASE_NAME'],
    app.config['DATABASE_USER'],
    app.config['DATABASE_PASSWORD'],
    app.config['DATABASE_HOST'])

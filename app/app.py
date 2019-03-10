import os
import uuid
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

SECRET_KEY = os.environ.get('SECRET_KEY') or str(uuid.uuid4())
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'postgres+psycopg2://postgres@pg/scregdb'

app = Flask(__name__)

db.init_app(app)
login_manager.init_app(app)
migrate.init_app(app, db)


from app.main import mainbp as main_blueprint
app.register_blueprint(main_blueprint, url_prefix='/')


if __name__ == '__main__':
    app.run()
import os
import uuid
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
admin = Admin()

POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or str(uuid.uuid4())
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:{}@pg/scregdb' \
    .format(POSTGRES_PASSWORD)
app.config['SQLALCHEMY_BINDS'] = {}

db.init_app(app)
login_manager.init_app(app)
migrate.init_app(app, db)
admin.init_app(app)

from app.main import mainbp as main_blueprint
from .main.models import *

app.register_blueprint(main_blueprint, url_prefix='/')

admin.add_views(ModelView(User, db.session, category='users'))
admin.add_views(ModelView(UserProfile, db.session, category='users'))
admin.add_views(ModelView(Project, db.session, category='cells & projects'))
admin.add_views(ModelView(ApprovalStatus, db.session, category='cells & projects'))
admin.add_views(ModelView(Institution, db.session, category='institutions'))

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run()

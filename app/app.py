import os
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
admin = Admin()
ma = Marshmallow()

DATABASE_URL = os.environ.get('DATABASE_URL')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_BINDS'] = {}

db.init_app(app)
login_manager.init_app(app)
migrate.init_app(app, db)
admin.init_app(app)
ma.init_app(app)

login_manager.login_view = 'main.log_user_in'

from app.main import mainbp as main_blueprint
from .main.models import *

app.register_blueprint(main_blueprint, url_prefix='/')

admin.add_views(ModelView(User, db.session, category='users'))
admin.add_views(ModelView(UserProfile, db.session, category='users'))
admin.add_views(ModelView(Project, db.session, category='cells & projects'))
admin.add_views(ModelView(ApprovalStatus, db.session, category='cells & projects'))
admin.add_views(ModelView(Cell, db.session, category='cells & projects'))
admin.add_views(ModelView(Institution, db.session, category='institutions'))
admin.add_views(ModelView(Event, db.session, category='events'))

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

@app.template_filter('shortdate')
def format_shortdate(value):
    if value is None:
        return ""
    return value.strftime('%-d %B %Y')


@app.template_filter('shortdatetime')
def format_shortdatetime(value):
    if value is None:
        return ""
    return value.strftime('%-d %B %Y at %H:%m')


if __name__ == '__main__':
    app.run()

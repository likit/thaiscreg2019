from ..app import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'main_users'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    email = db.Column('email', db.String(255), nullable=False)
    password = db.Column('password', db.String(255), nullable=False)
    activated = db.Column('activated', db.Boolean(), default=False)
    activated_at = db.Column('activated_at', db.DateTime(timezone=True))
    signup_at = db.Column('signup_at', db.DateTime(timezone=True), default=datetime.utcnow())

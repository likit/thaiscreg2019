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

    def __str__(self):
        return self.email


class UserProfile(db.Model):
    __tablename__ = 'main_user_profiles'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    public_email = db.Column('public_email', db.String(255), nullable=False)
    title_th = db.Column('title_th', db.String(32))
    academic_title_th = db.Column('academic_title_th', db.String(128))
    first_name_en = db.Column('first_name_en', db.String(255))
    last_name_en = db.Column('last_name_en', db.String(255))
    first_name_th = db.Column('first_name_th', db.String(255))
    last_name_th = db.Column('last_name_th', db.String(255))
    phone = db.Column('phone', db.String(32))
    street = db.Column('street', db.Text())
    user_id = db.Column('user_id', db.ForeignKey('main_users.id'))
    user = db.relationship('User', backref=db.backref('profile', uselist=False))
    affil_id = db.Column('affil_id', db.ForeignKey('main_institutions.id'))
    affil = db.relationship('Institution',
                            backref=db.backref('affiliates'))


class Institution(db.Model):
    __tablename__ = 'main_institutions'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name_th = db.Column('name_th', db.String(255), nullable=False)
    name_en = db.Column('name_en', db.String(255), nullable=False)
    campus = db.Column('campus', db.String(255))
    adder_id = db.Column('adder_id', db.ForeignKey('main_users.id'))
    adder = db.relationship('User')

    def __str__(self):
        return self.name_th


class ApprovalStatus(db.Model):
    __tablename__ = 'main_approval_statuses'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    status = db.Column('status', db.String(32))


class Project(db.Model):
    __tablename__ = 'main_projects'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    title = db.Column('title', db.String(255), nullable=False)
    acronym = db.Column('acronym', db.String(255))
    summary = db.Column('summary', db.Text())
    website = db.Column('website', db.String(255))
    startdate = db.Column('startdate', db.Date())
    enddate = db.Column('enddate', db.Date())
    sponsor_name = db.Column('sponsor_name', db.String(255))
    inst_id = db.Column('inst_id', db.ForeignKey('main_institutions.id'))
    creator_id = db.Column('creator_id', db.ForeignKey('main_users.id'))
    creator = db.relationship('User', backref=db.backref('created_projects'))
    status_id = db.Column('status_id', db.ForeignKey('main_approval_statuses.id'))
    status = db.relationship('ApprovalStatus')

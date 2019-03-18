from ..app import db, ma
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql.json import JSONB
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = 'main_users'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    email = db.Column('email', db.String(255), nullable=False)
    password_hash = db.Column('password', db.String(255), nullable=False)
    activated = db.Column('activated', db.Boolean(), default=False)
    activated_at = db.Column('activated_at', db.DateTime(timezone=True))
    signup_at = db.Column('signup_at', db.DateTime(timezone=True), default=datetime.utcnow())

    def __str__(self):
        return self.email

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


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

    def __str__(self):
        return self.status

    def __repr__(self):
        return self.__str__()


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
    institution = db.relationship('Institution')
    creator_id = db.Column('creator_id', db.ForeignKey('main_users.id'))
    creator = db.relationship('User', backref=db.backref('created_projects'))
    status_id = db.Column('status_id', db.ForeignKey('main_approval_statuses.id'))
    status = db.relationship('ApprovalStatus')
    view_count = db.Column('view_count', db.Integer(), default=0)
    last_view = db.Column('last_view', db.DateTime(timezone=True))
    cell_id = db.Column('cell_id', db.ForeignKey('main_cells.id'))
    cell = db.relationship('Cell', backref=db.backref('projects'))


class Cell(db.Model):
    __tablename__ = 'main_cells'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    institution_id = db.Column('institution_id', db.ForeignKey('main_institutions.id'))
    institution = db.relationship('Institution', backref=db.backref('affiliated_cells'))
    cell_type = db.Column('cell_type', db.String(64))
    user_id = db.Column('user_id', db.ForeignKey('main_users.id'))
    user = db.relationship('User', backref=db.backref('own_cells'))
    status_id = db.Column('status_id', db.ForeignKey('main_approval_statuses.id'))
    status = db.relationship('ApprovalStatus', backref=db.backref('cells'))
    register_datetime = db.Column('register_datetime', db.DateTime(timezone=True),
                                  default=datetime.utcnow())
    update_datetime = db.Column('update_datetime', db.DateTime(timezone=True))
    data = db.Column('data', JSONB)
    view_count = db.Column('view_count', db.Integer(), default=0)
    last_view = db.Column('last_view', db.DateTime(timezone=True))


class Event(db.Model):
    __tablename__ = 'main_events'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(255))
    venue = db.Column('venue', db.String(255))
    description = db.Column('description', db.Text())
    max_participants = db.Column('max_participants', db.Integer())
    start = db.Column('start', db.DateTime(timezone=True))
    end = db.Column('end', db.DateTime(timezone=True))
    creator_id = db.Column('creator_id', db.ForeignKey('main_users.id'))
    creator = db.relationship('User', backref=db.backref('created_events'))
    closed = db.Column('closed', db.Boolean(), default=False)
    view_count = db.Column('view_count', db.Integer(), default=0)


class InstitutionSchema(ma.ModelSchema):
    class Meta:
        model = Institution


class CellSchema(ma.ModelSchema):
    class Meta:
        model = Cell

from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, PasswordField,
                     RadioField, SelectField, BooleanField, DateField)
from wtforms.widgets import TextArea
from wtforms.validators import Email, DataRequired, Length, EqualTo


class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    password1 = PasswordField('Password',
                              validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Confirm password',
                              validators=[DataRequired(),
                                          EqualTo('password1',
                                                  message="Passwords do not match.")])
    submit = SubmitField('Submit')


class LogInForm(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Submit')


class ProfileForm(FlaskForm):
    public_email = StringField('Public Email', validators=[Email()])
    title_th = StringField('Title', validators=[Length(max=128)])
    academic_title_th = StringField('Academic Title', validators=[Length(max=128)])
    firstname_en = StringField('English First Name')
    lastname_en = StringField('English Last Name')
    firstname_th = StringField('Thai First Name')
    lastname_th = StringField('Thai Last Name')
    phone = StringField('Phone')
    street = StringField('Street', widget=TextArea())
    submit = SubmitField('Submit')


class RegisterCellForm(FlaskForm):
    cell_type = RadioField('Cell Type',
                           choices=[('hiPSC', 'hiPSC'), ('hESC', 'hESC'), ('MSC', 'MSC')],
                           validators=[DataRequired()])
    institution = SelectField('Institution',
                              validators=[DataRequired(), ])
    code_name = StringField('Code Name', validators=[DataRequired()])
    comment = StringField('Comment', widget=TextArea())
    alternative_names = StringField('Alternative Name(s)')
    available = SelectField('Availability', choices=[
        ('0', 'Available'),
        ('1', 'Available for Non-commercial Research')
    ])
    karyotyped = SelectField('Has the cell line been karyotyped?',
                             choices=[(False, 'No'), (True, 'Yes')])
    karyotype = StringField('Karyotype')
    donor_gender = SelectField('Sex', choices=[('male', 'Male'), ('female', 'Female')])
    donor_diseases = StringField('Diseases')
    donor_disease_assoc_phenotypes = StringField('Disease associated phenotypes')
    donor_karyotyped = SelectField('Has the donor karyotype been analyzed?',
                                   choices=[(False, 'No'), (True, 'Yes')])
    donor_gws = SelectField('Is there genome-wide genotyping or functional data available?',
                            choices=[(False, 'No'), (True, 'Yes')])
    submit = SubmitField('Submit')


class RegisterProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    acronym = StringField('acronym')
    summary = StringField('summary')
    website = StringField('website')
    startdate = DateField('Start Date', validators=[DataRequired()])
    enddate = DateField('End Date', validators=[DataRequired()])
    sponsor_name = StringField('Sponsor Name')
    institution = StringField('Institution Name')
    submit = SubmitField('Submit')

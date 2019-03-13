from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
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

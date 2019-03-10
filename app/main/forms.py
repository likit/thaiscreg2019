from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Email, DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    password1 = PasswordField('Password',
                              validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Confirm password',
                              validators=[DataRequired(),
                                          EqualTo('password1',
                                                  message="Passwords do not match.")])
    submit = SubmitField('Submit')
import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField, TelField
from wtforms.validators import DataRequired, Email, Regexp

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password')


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired(), Email()])
    phone_number = TelField('phone_number', validators=[DataRequired(), Regexp(r'^((\+7|7|8)+([0-9]){10})$', re.IGNORECASE, 'Телефон может начинаться с +7, 7, 8 и иметь формат 9992223344')])
    first_name = StringField('first_name', validators=[DataRequired()])
    middle_name = StringField('middle_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
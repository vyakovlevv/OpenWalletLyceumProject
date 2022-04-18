from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
    mnemo = StringField('Mnemonic phrase')
    password = PasswordField('Password', validators=[DataRequired(), Length(8)])
    password_again = PasswordField('Password again', validators=[DataRequired(), Length(8)])
    submit = SubmitField('Войти')

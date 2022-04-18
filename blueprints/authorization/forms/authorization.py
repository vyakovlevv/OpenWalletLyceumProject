from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class AuthorizationForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(8)])
    submit = SubmitField('Войти')

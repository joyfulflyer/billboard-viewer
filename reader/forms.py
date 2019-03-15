from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()],
                             default="login")
    submit = SubmitField('Submit')

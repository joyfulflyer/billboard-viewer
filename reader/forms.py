from flask_wtf import FlaskForm
from wtfforms import PasswordField, SubmitField
from wtfforms.validators import DataRequired

class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

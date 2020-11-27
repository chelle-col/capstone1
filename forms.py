from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional

class UserAddForm(FlaskForm):
    """Form for adding users."""

    title = 'Sign Up!'
    button_title = 'Sign me up!'
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')

class UserLoginForm(FlaskForm):
    """Form for Logging in"""

    title = 'Log in'
    button_title = 'Log me in!'
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
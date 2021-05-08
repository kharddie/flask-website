"""
Login Form
"""
# Import 'FlaskForm' from 'flask_wtf', NOT 'wtforms'
from flask_wtf import FlaskForm
# Fields and validators from 'wtforms'  
from wtforms import StringField, PasswordField
from wtforms.fields.core import BooleanField
from wtforms.validators import InputRequired, Length

# Define the 'LoginForm' class by sub-classing 'Form'
class LoginForm(FlaskForm):
    # This form contains two fields with input validators
    username = StringField('username:', validators=[InputRequired(), Length(max=20)])
    password = PasswordField('Password:', validators=[Length(min=4, max=16)])
    remember_me = BooleanField('remember_me:',default = False)  
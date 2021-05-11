"""
Register Form
"""
# Import 'FlaskForm' from 'flask_wtf', NOT 'wtforms'
from flask_wtf import FlaskForm
# Fields and validators from 'wtforms'  
from wtforms import StringField, PasswordField
from wtforms.fields.core import BooleanField
from wtforms.validators import Email, InputRequired, Length

# Define the 'LoginForm' class by sub-classing 'Form'
class RegisterForm(FlaskForm):
    # This form contains two fields with input validators
    username = StringField('Uuername:', validators=[InputRequired(), Length(max=20)])
    email = StringField('Email:', validators=[InputRequired(), Email()])
    password = PasswordField('Password:', validators=[Length(min=4, max=16)])
    password_repeat = PasswordField('Repeat Password:', validators=[InputRequired(),Length(min=4, max=16)])
    accept_terms = BooleanField('accept_terms:',default = False,validators=[InputRequired()])  
    accept_rules = BooleanField('I accept the site rules',validators=[InputRequired()])
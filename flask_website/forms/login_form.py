from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    ### -- By defining class variables which are instantiations of the fields.
    username = StringField('Username', validators=[DataRequired()], filters=tuple(), description='description',)
    password = PasswordField('password', validators=[DataRequired()], filters=tuple(), description='', widget=None, render_kwargs=None,)
    email = StringField('Email', validators=[DataRequired()], filters=tuple(), description='description', default="None", )
    password = PasswordField('Password', validators=[DataRequired()], description='description',)
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log In')
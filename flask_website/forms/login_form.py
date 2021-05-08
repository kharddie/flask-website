from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    # -- By defining class variables which are instantiations of the fields.
    username = StringField('username', validators=[DataRequired()], filters=tuple(), description='description',  )

    password = PasswordField('password', validators=[DataRequired(
    )], filters=tuple(), description='', widget=None, render_kwargs=None,)

    remember_me = BooleanField('Remember Me', filters=tuple(
    ), description='',  default=None, widget=None, render_kwargs=None,)

    email = StringField('Email', validators=[DataRequired()], filters=tuple(), description='description',default="None", )
    password = PasswordField('Password', validators=[DataRequired()],description='description',)

    remember_me = BooleanField('Keep me logged in')

    accept_rules = BooleanField(
        'I accept the site rules', validators=[DataRequired()])
    submit = SubmitField('Log In')



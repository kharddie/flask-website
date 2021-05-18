from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class Contact(FlaskForm):
    ### -- By defining class variables which are instantiations of the fields.
    username = StringField('Username', validators=[DataRequired()], filters=tuple(), description='description',)
    email = StringField('Email', validators=[DataRequired()], filters=tuple(), description='description', default="None", )
    address = StringField('Address', validators=[DataRequired()], filters=tuple(), description='description',)
    city = StringField('City', validators=[DataRequired()], filters=tuple(), description='description',)
    state = StringField('State', validators=[DataRequired()], filters=tuple(), description='description',)
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log In')
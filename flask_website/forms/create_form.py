from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
from wtforms.validators import DataRequired
import pdb

class CreateForm(FlaskForm):
    ### -- By defining class variables which are instantiations of the fields.
    #pdb.set_trace()
    title = StringField('Title', validators=[DataRequired()], filters=tuple(), description='description',)
    body = TextAreaField('Body',  validators=[DataRequired()], filters=tuple(), description='description',)
    submit = SubmitField('Save')






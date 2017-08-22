from flask_wtf import FlaskForm
from wtforms import StringField, validators, SelectField, SelectMultipleField, FileField
from flask_wtf.file import FileAllowed, FileRequired


class FileInputForm(FlaskForm):
    # DATA
    openfile = FileField('Input txt file', validators=[FileAllowed(['txt'], 'Only text files are valid input!'), FileRequired()])


class InputForm(FlaskForm):
    # DATA SYNTH
    site_codes = [('', ''), ('UM', 'UM Copath NLSIIa'), ('JHS', 'JHS Copath NLSIIa')]
    # DATA
    out_dir = StringField('Name of project', validators=[validators.DataRequired()])
    choice_site = SelectField(label='Site', choices=site_codes, validators=[validators.Length(min=1)])
    choice_spec = SelectMultipleField(label='Specimen classes', choices=[], validators=[validators.required()])
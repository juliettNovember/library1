from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired


class MovieForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    year = StringField('year', validators=[DataRequired()])
    species = TextAreaField('species', validators=[DataRequired()])   
    watch = BooleanField('watch')
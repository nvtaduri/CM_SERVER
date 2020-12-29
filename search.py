from wtforms import StringField, SubmitField, IntegerField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()])
    submit = SubmitField('search')
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from app.models import Track

class SearchForm(FlaskForm):
    search_key = StringField('search key', validators=[DataRequired(), Length(2, 100)])
    submit = SubmitField('search')

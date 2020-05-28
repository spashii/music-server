from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import Playlist

class SearchForm(FlaskForm):
    search_key = StringField('search key', validators=[DataRequired(), Length(2, 100)])
    submit = SubmitField('search')

class NewPlaylistForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    submit = SubmitField('create')
    
    def validate_title(self, title):
        playlist = Playlist.query.filter_by(title=title.data).first()
        if playlist:
            raise ValidationError('please use another title')

from app import app, db
from app.models import Track
from app.forms import SearchForm
from flask import render_template, redirect, url_for, request

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    search_tracks = []
    if form.validate_on_submit():
        search_tracks = Track.get_search_result(form.search_key.data)
    return render_template('home.html', form=form, tracks=search_tracks) 

@app.route('/library')
def library():
    tracks = Track.query.order_by(Track.title.asc())
    return render_template('library.html', tracks=tracks)

@app.route('/track/cache/<id>')
def track_cache(id):
    if id == 'all':
        Track.cache_all()
    else:
        track = Track.query.get(id)
        if track is not None:
            track.cache()
    return redirect(request.referrer or url_for('home'))

@app.route('/track/add/<id>')
def track_add(id):
    if id == 'all':
        Track.index_all()
    else:
        track = Track(id=id).index()  
    return redirect(request.referrer or url_for('home'))

@app.route('/track/delete/<id>')
def track_delete(id):
    track = Track.query.get(id)
    if track is not None:
        track.delete_index()
    return redirect(request.referrer or url_for('home'))

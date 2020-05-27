from app import app, db
from app.models import Track
from flask import render_template, redirect, url_for

@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html') 

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
    return redirect(url_for('library'))

@app.route('/track/add/<id>')
def track_add(id):
    if id == 'all':
        Track.index_all()
    else:
        track = Track(id=id).index()  
    return redirect(url_for('library'))

@app.route('/track/delete/<id>')
def track_delete(id):
    track = Track.query.get(id)
    if track is not None:
        track.delete_index()
    return redirect(url_for('library'))

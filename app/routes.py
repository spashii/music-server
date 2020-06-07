import threading
from app import app, db
from app.models import Track, Playlist
from app.forms import SearchForm, NewPlaylistForm
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
    sort_by = request.args.get('sort_by', default='date_added', type=str)
    if sort_by == 'title':
        tracks = Track.query.order_by(Track.title.asc())
    else:
        tracks = Track.query.order_by(Track.date_added.desc())
    playlists = Playlist.query.order_by(Playlist.title.asc())
    return render_template('library.html', tracks=tracks, are_cached=Track.are_cached(), playlists=playlists)

@app.route('/track/cache/<id>', methods=['POST'])
def track_cache(id):
    if id == 'all':
        Track.cache_all()
    else:
        track = Track.query.get(id)
        if track is not None:
            track.cache()
    return redirect(request.referrer or url_for('index'))

@app.route('/track/add/<id>', methods=['POST'])
def track_add(id):
    if id == 'all':
        Track.index_all()
    else:
        track = Track(id=id).index()  
    return redirect(request.referrer or url_for('index'))

@app.route('/track/delete/<id>', methods=['POST'])
def track_delete(id):
    track = Track.query.get(id)
    if track is not None:
        track.delete_index()
    return redirect(request.referrer or url_for('index'))

@app.route('/track/play/<id>')
def track_play(id):
    track = Track.query.get_or_404(id)
    return render_template('track_play.html', track=track)

@app.route('/options')
def options():
    return render_template('options.html')

@app.route('/playlist')
def playlist_all():
    playlists = Playlist.query.all()
    return render_template('playlist_all.html', playlists=playlists) 

@app.route('/playlist/new', methods=['GET', 'POST'])
def playlist_new():
    form = NewPlaylistForm()
    if form.validate_on_submit():
         playlist = Playlist(title=form.title.data)
         db.session.add(playlist)
         db.session.commit()
         return redirect(url_for('playlist_all'))
    return render_template('playlist_new.html', form=form)

@app.route('/playlist/delete/<int:id>', methods=['POST'])
def playlist_delete(id):
     playlist = Playlist.query.get_or_404(id)
     db.session.delete(playlist)
     db.session.commit()
     return redirect(request.referrer or url_for('playlist_all'))

@app.route('/playlist/<int:id>')
def playlist(id):
    playlist = Playlist.query.get_or_404(id)
    return render_template('playlist.html', playlist=playlist) 

@app.route('/playlist/<int:id>/add/<track_id>', methods=['POST'])
def playlist_add(id, track_id):
    track = Track.query.get(track_id)
    playlist = Playlist.query.get(id)
    if track and playlist:
        track.add_to_playlist(playlist)
        db.session.commit()
    return redirect(request.referrer or\
                    url_for('playlist', id=id) or\
                    url_for('playlists'))

@app.route('/playlist/<int:id>/remove/<track_id>', methods=['POST'])
def playlist_remove(id, track_id):
    track = Track.query.get(track_id)
    playlist = Playlist.query.get(id)
    if track and playlist:
        track.remove_from_playlist(playlist)
        db.session.commit()
    return redirect(request.referrer or\
                    url_for('playlist', id=id) or\
                    url_for('playlists'))
                
                

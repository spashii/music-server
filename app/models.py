import os
from datetime import datetime
from app import db
from app.config import Config
import youtube_dl
import urllib
import requests
from bs4 import BeautifulSoup

track_cache_path = os.path.join(Config.BASE_DIR, 'static', 'track_cache')

ydl_opts = {
    'verbose':  False,
    'format': 'bestaudio',
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',    
        },
        ],
    'outtmpl': os.path.join(track_cache_path, '%(id)s.%(ext)s'),
    'restrictfilenames': True,
    'nooverwrites': True,
}

class Track(db.Model):
    id = db.Column(db.String(16), primary_key=True)
    title = db.Column(db.String(128))
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # playlists = db.relationship(
    #             'Playlist',
    #             secondary=playlist_tracks,
    #             )
    
    def __repr__(self):
        return self.id

    def is_indexed(self):
        track = Track.query.get(self.id)
        if track is None:
            return False
        return True

    def is_cached(self):
        path = os.path.join(track_cache_path, self.id+'.mp3')
        return os.path.exists(path)

    def index(self):
        track = Track.query.get(self.id)
        if track is None:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.id, download=False)
                self.title = info.get('title')
                db.session.add(self)
                db.session.commit()

    def delete_index(self):
        track = Track.query.get(self.id)
        if track is not None:
            db.session.delete(track)
            db.session.commit()
        

    def cache(self):
        if not self.is_cached():
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.id, download=True)
                self.title = info.get('title')
                track = Track.query.get(self.id)
                if track is None:
                    db.session.add(self)
                    db.session.commit()
                else:
                    track.title = self.title
                    db.session.commit()

    @staticmethod
    def are_cached():
        for track in Track.query.all():
            if not track.is_cached():
                return False
        return True

    @staticmethod
    def index_all():
        path = os.path.join(track_cache_path)
        for track_filename in os.listdir(path):
            if track_filename.endswith('.mp3'):
                id = track_filename.split(sep='.')[0]
                track = Track.query.get(id)
                if track is None:
                    with youtube_dl.YoutubeDL() as ydl:
                        try:
                            info = ydl.extract_info(id, download=False)
                        except:
                            title = id
                        else:
                            title = info.get('title')
                        track = Track(id=id, title=title)
                        db.session.add(track)
                        db.session.commit()

    @staticmethod
    def cache_all():
        tracks = Track.query.all()
        for track in tracks:
            track.cache()

    @staticmethod
    def get_search_result(search_key):
        encoded_key = urllib.parse.quote(search_key)
        base = 'https://youtube.com'
        url = f'{base}/results?search_query={encoded_key}'
        response = requests.get(url).text
        soup = BeautifulSoup(response, 'html.parser')
        tracks = []
        results = soup.select('.yt-uix-tile-link', limit=5)
        for result in results:
            if result['href'].startswith('/watch?v='):
                track = Track(id = result['href'][-11:],
                              title = result['title'])
                tracks.append(track)
        return tracks

    def add_to_playlist(self, playlist):
        playlist.tracks.append(self)
        print(f'[music server] {self.id} added to {playlist.title}')

    def remove_from_playlist(self, playlist):
        playlist.tracks.remove(self)
        print(f'[music server] {self.id} removed from {playlist.title}')

playlist_tracks = db.Table(
                   'playlist_tracks',
                   db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id')),
                   db.Column('track_id', db.String(16), db.ForeignKey('track.id')))

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(32), unique=True)
    tracks = db.relationship(
            'Track',
            secondary=playlist_tracks,
            lazy='dynamic',
            backref=db.backref('playlists', lazy=True))

    def __repr__(self):
        return f"[title: {self.title}, tracks: {','.join([str(i) for i in self.tracks])}]"
        
    @staticmethod
    def all():
        playlist = Playlist()
        playlist.id = -1
        playlist.title = 'all'
        playlist.tracks = Track.query.all()
        return playlist

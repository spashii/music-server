import os
from app import db
from app.config import Config
import youtube_dl
import urllib
import requests
from bs4 import BeautifulSoup

cache_path = Config.TRACK_CACHE_PATH

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
    'outtmpl': os.path.join(cache_path, '%(id)s.%(ext)s'),
    'restrictfilenames': True,
    'nooverwrites': True,
}

class Track(db.Model):
    id = db.Column(db.String(16), primary_key=True)
    title = db.Column(db.String(128))
    
    def __repr__(self):
        return self.id

    def is_cached(self):
        path = os.path.join(cache_path, self.id+'.mp3')
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
    def index_all():
        path = os.path.join(cache_path)
        for track_filename in os.listdir(path):
            if track_filename.endswith('.mp3'):
                id = track_filename.split(sep='.')[0]
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(id, download=False)
                title = info.get('title')
                track = Track.query.get(id)
                if track is None:
                    track = Track(id=id, title=title)
                    db.session.add(track)
                    db.session.commit()
                else:
                    track.title = title
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
                track = Track(id = link[-11:],
                              title = result['title'])
                tracks.append(track)
        return tracks


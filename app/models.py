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
        path = os.path.join(cache_path, self.id+'.'+ydl_opts.get('postprocessors')[0].get('preferredcodec'))
        return os.path.exists(path)

    def cache_track(self):
        if not self.is_cached():
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.id, download=True)
                self.title = info.get('title')
                track = db.session.query(Track).get(self.id)
                if track is None:
                    db.session.add(self)
                    db.session.commit()
                else:
                    track.title = self.title
                    db.session.commit()

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

from app import app, db
from app.models import Track

@app.route('/')
@app.route('/home')
def index():
    return 'hello' 

@app.route('/library')
def library():
    # Track(id='CiTqVvcMB6o').cache_track()
    tracks = Track.query.order_by(Track.title.asc())
    count = 0
    for track in tracks:
        count += 1
    return f'{count}'

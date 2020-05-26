from app import app, db
from app.models import Track


@app.route('/')
@app.route('/home')
def index():
    return 'Hello World'

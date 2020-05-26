from app import db

class Track(db.Model):
    id = db.Column(db.String(11), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(128), unique=True)
    
    def __repr__(self):
        return self.id


from flask import Flask
from app.config import Config 

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    return app

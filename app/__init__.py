from flask import Flask
from .config import Config
from .database import db
from .models import Customer, Product, Order
from .routes import setup_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    setup_routes(app)

    return app

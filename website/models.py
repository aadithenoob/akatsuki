from website import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    discord_id = db.Column(db.String(30), unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    discriminator = db.Column(db.String(10))
    avatar = db.Column(db.String(100))

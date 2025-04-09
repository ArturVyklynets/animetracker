from db import db
from datetime import datetime
from slugify import slugify


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name
        self.slug = slugify(name)

class PopularAnime(db.Model):
    __tablename__ = 'popular_anime'

    id = db.Column(db.Integer, primary_key=True)
    mal_id = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(500))
    synopsis = db.Column(db.Text, nullable=True) 
    score = db.Column(db.Float)
    rank = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, mal_id, title, image_url, synopsis, score, rank):
        self.mal_id = mal_id
        self.title = title
        self.image_url = image_url
        self.synopsis = synopsis
        self.score = score
        self.rank = rank
        self.updated_at = datetime.utcnow()
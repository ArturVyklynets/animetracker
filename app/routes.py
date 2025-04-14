from flask import Blueprint, render_template
from flask import redirect, url_for
from .config import Config

main = Blueprint("main", __name__)

if Config.DB_ENABLED:
    from .models import Category, PopularAnime, db
else:
    from .fake_data import fake_categories, fake_anime

@main.route('/')
def index():
    if Config.DB_ENABLED:
        categories = Category.query.all()
        popular_anime = PopularAnime.query.all()
    else:
        categories = fake_categories
        popular_anime = fake_anime

    return render_template('index.html', categories=categories, popular_anime=popular_anime)

@main.route('/test-db')
def test_db():
    if Config.DB_ENABLED:
        try:
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            return "Database connection is working!"
        except Exception as e:
            return f"Error: {str(e)}"
    return "Ця функція недоступна без бази даних."

@main.route('/404')
def page_not_found():
    return render_template('404.html'), 404

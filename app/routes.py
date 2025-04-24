import requests
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

@main.route('/userpage')
def get_user_page():
    return render_template('userPage.html')

@main.route('/category/<slug>')
def category_anime(slug):
    if Config.DB_ENABLED:
        category = Category.query.filter_by(slug=slug).first_or_404()
        genre_name = category.slug
    else:
        category = next((c for c in fake_categories if c["slug"] == slug), None)
        if not category:
            return redirect(url_for('main.page_not_found'))
        genre_name = category["name"]

    query = """
    query ($genre: String) {
      Page(perPage: 10) {
        media(genre_in: [$genre], type: ANIME) {
          id
          title {
            romaji
          }
          coverImage {
            large
          }
          averageScore
        }
      }
    }
    """

    variables = {"genre": genre_name}
    print("Genre sent to AniList:", genre_name)
    response = requests.post("https://graphql.anilist.co", json={"query": query, "variables": variables})

    if response.status_code != 200:
        return render_template('error.html', message="Помилка при запиті до API")

    anime_list = response.json()["data"]["Page"]["media"]
    print("Отримано:", anime_list)

    return render_template('category_anime.html', category=category, anime_list=anime_list)

import os
from flask import Flask, render_template

app = Flask(__name__)

uri = os.getenv('DATABASE_URL')
if uri and uri.startswith('postgres://'):
    uri = uri.replace('postgres://', 'postgresql://', 1)

db_enabled = bool(uri)

if db_enabled:
    from db import db
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    from flask_migrate import Migrate
    migrate = Migrate(app, db)
    from models import Category 
else:
    fake_categories = [
        {"id": 1, "name": "Екшн", "slug": "екшн"},
        {"id": 2, "name": "Пригоди", "slug": "пригоди"},
        {"id": 3, "name": "Фентезі", "slug": "фентезі"},
    ]

@app.route("/")
def index():
    if db_enabled:
        categories = Category.query.all()
    else:
        categories = fake_categories

    return render_template("index.html", categories=categories)

@app.route("/test-db")
def test_db():
    if db_enabled:
        try:
            from sqlalchemy import text
            result = db.session.execute(text('SELECT 1'))
            return "Database connection is working!"
        except Exception as e:
            return f"Error: {str(e)}"
    return "Ця функція недоступна без бази даних."

if __name__ == '__main__':
    if db_enabled:
        with app.app_context():
            db.create_all()
    app.run(debug=True)
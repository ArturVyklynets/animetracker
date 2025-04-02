from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://animetracker_db:123456789@localhost:5433/animeTracker"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from models import Category

migrate = Migrate(app, db)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/test-db")
def test_db():
    try:
        result = db.session.execute(text('SELECT 1'))
        return "Database connection is working!"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    with app.app_context():
      db.create_all()
    app.run(debug=True)

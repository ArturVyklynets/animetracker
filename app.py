import os
from flask import Flask, render_template, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    scope=[
        "https://www.googleapis.com/auth/userinfo.email", 
        "https://www.googleapis.com/auth/userinfo.profile", 
        "openid"
    ]
)
app.register_blueprint(google_bp, url_prefix="/login")

uri = os.getenv('DATABASE_URL')
if uri and uri.startswith('postgres://'):
    uri = uri.replace('postgres://', 'postgresql://', 1)

db_enabled = bool(uri)

# from db import db
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://animetracker_db:123456789@localhost:5433/animeTracker"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db.init_app(app)
# from flask_migrate import Migrate
# migrate = Migrate(app, db)
# from models import Category, PopularAnime 
db_enabled = False
if db_enabled:
    from db import db
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    from flask_migrate import Migrate
    migrate = Migrate(app, db)
    from models import Category, PopularAnime 
else:
    fake_categories = [
      {"id": 1, "name": "Екшн", "slug": "екшн"},
      {"id": 2, "name": "Пригоди", "slug": "пригоди"},
      {"id": 3, "name": "Фентезі", "slug": "фентезі"},
      {"id": 4, "name": "Ісекай", "slug": "ісєкай"},
      {"id": 5, "name": "Наукова фантастика", "slug": "наукова-фантастика"},
      {"id": 6, "name": "Хорор", "slug": "хорор"},
      {"id": 7, "name": "Детектив", "slug": "детектив"},
      {"id": 8, "name": "Психологічний", "slug": "психологічний"},
      {"id": 9, "name": "Романтика", "slug": "романтика"},
      {"id": 10, "name": "Комедія", "slug": "комедія"},
      {"id": 11, "name": "Драма", "slug": "драма"},
      {"id": 12, "name": "Спортивне", "slug": "спортивне"},
      {"id": 13, "name": "Шкільне", "slug": "шкільне"},
      {"id": 14, "name": "Музичне", "slug": "музичне"},
      {"id": 15, "name": "Еччі", "slug": "еччі"},
      {"id": 16, "name": "Яой", "slug": "яой"},
      {"id": 17, "name": "Юрі", "slug": "юрі"},
      {"id": 18, "name": "Повсякденність", "slug": "повсякденність"},
      {"id": 19, "name": "Історичне", "slug": "історичне"},
      {"id": 20, "name": "Військове", "slug": "військове"},
      {"id": 21, "name": "Пародія", "slug": "пародія"},
    ]

    fake_anime = [
        {"id": 1, "title": "Гінтама 2 сезон", "synopsis": "Після річної перерви Шінпачі Шімура повертається до Едо, аби наштовхнутися на шокуючу несподіванку: Гінтокі та Кагура, його товариші по \"Йорозуя\", стали зовсім іншими персонажами! Тікаючи зі штаб-квартири Йорозуя, Шинпачі в розгубленості виявляє, що всі мешканці Едо зазнали неймовірно сильних змін, як у зовнішності, так і в характері. Неймовірно, але його сестра Отае вийшла заміж за ватажка Шинсенґумі та безсоромного переслідувача Ісао Кондо і вагітна їхньою першою дитиною. Спантеличений, Шинпачі погоджується приєднатися до Шинсенґумі на прохання Отае та Кондоу і виявляє ще більш вражаючі трансформації як у лавах організації, так і поза ними. Однак, виявивши, що віце-голова Тошіроу Хіджіката залишився незмінним, Шінпачі та його малоймовірний союзник Шінсенґумі вирішують повернути місто Ед", "image_url": "/static/images/Ghintama.jpg"},
        
        {"id": 2, "title": "Лист до фанатів", "synopsis": "Хоча золотий вік піратства ось-ось досягне нових висот, більшість людей не прагне слави віднайдення невловимого One Piece - скарбу, що означає нового підкорювача всіх морів, якого колись уособлював легендарний Король піратів Гол Д. Роджер. Однак, навіть якщо цивільні зневажають піратів, вони таємно вболівають принаймні за одного з них. Одна рудоволоса дівчина з архіпелагу Сабаоді не є винятком: Вона шанує Намі, геніальну жінку-штурмана з екіпажу \"Солом'яного капелюха\" Мавпи Д. Луффі. Вирішивши доставити фанатського листа своєму кумиру, дитина з Сабаоді готова кинути виклик владі, яка прагне перешкодити Луффі та його друзям відправитися до наступного пункту призначення - Нового Світу. Але щоб досягти успіху, прихильниці Намі, можливо, доведеться ризикувати своїм життям і втрутитися в плани...", "image_url": "/static/images/LetterTo.jpg"}
    ]

@app.route("/")
def index():
    # if not google.authorized:
    #     return redirect(url_for("google.login"))
    
    # resp = google.get("/oauth2/v2/userinfo")
    # user_info = resp.json()
    # user_email = user_info["email"]

    if db_enabled:
        categories = Category.query.all()
        popular_anime = PopularAnime.query.all()
    else:
        categories = fake_categories
        popular_anime = fake_anime

    return render_template("index.html", categories=categories, popular_anime=popular_anime)
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

@app.route('/404') 
def page_not_found():
    return render_template('404.html'), 404
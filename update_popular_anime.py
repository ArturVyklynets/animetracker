import requests
from datetime import datetime
from app import app
from db import db
from models import PopularAnime
from translate import translate_text

def update_popular_anime():
    url = "https://api.jikan.moe/v4/top/anime"
    response = requests.get(url, params={"limit": 10})

    if response.status_code != 200:
        print("Помилка при запиті до Jikan API")
        return

    data = response.json().get("data", [])

    with app.app_context():
        for anime in data:
            english_title = next((title["title"] for title in anime["titles"] if title["type"] == "English"), None)

            if not english_title:
                english_title = anime["title"]

            translated_title = translate_text(english_title, "uk")
            translated_synopsis = translate_text(anime.get("synopsis", ""), "uk")

            existing = PopularAnime.query.filter_by(mal_id=anime["mal_id"]).first()

            if existing:
                existing.title = translated_title
                existing.image_url = anime["images"]["jpg"]["image_url"]
                existing.synopsis = translated_synopsis
                existing.updated_at = datetime.utcnow()
            else:
                new_anime = PopularAnime(
                    mal_id=anime["mal_id"],
                    title=translated_title,
                    image_url=anime["images"]["jpg"]["image_url"],
                    synopsis=translated_synopsis,
                )
                db.session.add(new_anime)

        db.session.commit()
        print("Топ аніме успішно оновлено!")

if __name__ == "__main__":
    update_popular_anime()

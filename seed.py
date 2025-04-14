from app import db, app
from app.models import Category

def seed_categories():
    categories = [
        "Екшн", "Пригоди", "Фентезі", "Ісекай", "Наукова фантастика", "Хорор", "Детектив",
        "Психологічний", "Романтика", "Комедія", "Драма", "Спортивне", "Шкільне", "Музичне",
        "Еччі", "Яой", "Юрі", "Повсяденність", "Історичне", "Військове", "Пародія"
    ]
    
    for name in categories:
        category = Category(name=name)
        db.session.add(category)
    
    db.session.commit()
    print("Categories seeded successfully!")

if __name__ == "__main__":
    with app.app_context():
        seed_categories()
from app import create_app
from app.models import db
from slugify import slugify

app = create_app()

def seed_categories():
    from app.models import Category
    categories = [
        "Екшн", "Пригоди", "Фентезі", "Ісекай", "Наукова фантастика", "Хорор", "Детектив",
        "Психологічний", "Романтика", "Комедія", "Драма", "Спортивне", "Шкільне", "Музичне",
        "Еччі", "Яой", "Юрі", "Повсяденність", "Історичне", "Військове", "Пародія"
    ]
    for name in categories:
        slug = slugify(name)
        category = Category(name=name, slug=slug) 
        db.session.add(category)
    
    db.session.commit()
    print("Categories seeded successfully!")

if __name__ == "__main__":
    with app.app_context():
        seed_categories()
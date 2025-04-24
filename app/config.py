import os

uri = os.getenv("DATABASE_URL") or "postgres://u6mcj67k662hjg:pce7faeb7ed90e726c97bf6772ee7975a053396e15cc47aafb393465c6361acf6@c67okggoj39697.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/deiqmb1se9nph"
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_ENABLED = bool(uri)
    DB_ENABLED = False

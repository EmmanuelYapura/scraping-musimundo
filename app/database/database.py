from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine

DATABASE_URL = 'mysql+pymysql://root:123456@localhost:3306/test'

engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False , bind=engine)

Base = declarative_base()

def get_base():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

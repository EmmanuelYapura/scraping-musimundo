from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///./productos.db'

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread" : False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False , bind=engine)

Base = declarative_base()

def get_base():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

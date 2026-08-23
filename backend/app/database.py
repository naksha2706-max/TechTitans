from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

db_url = settings.DATABASE_URL.strip() if settings.DATABASE_URL else ""

# Fallback to local SQLite database if no database URL is set
if not db_url:
    db_url = "sqlite:///./scamcheck.db"

is_sqlite = db_url.startswith("sqlite")

if is_sqlite:
    engine = create_engine(
        db_url, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

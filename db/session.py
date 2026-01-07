from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./ecommerce.db"
# or your mysql/postgres url

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # sqlite only
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# ✅ THIS IS IMPORTANT
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

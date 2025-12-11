from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()


# try:
#     with engine.connect() as conn:
#         conn.execute(text("SELECT 1"))
#     print("Database connection successful!")
# except Exception as e:
#     print("Database connection failed:", e)

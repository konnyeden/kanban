from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# DATABASE_URL examples:
#   postgresql://user:pass@localhost:5432/kanban
#   For docker-compose, env var DATABASE_URL can be:
#   postgresql://postgres:postgres@db:5432/kanban

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/kanban")

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

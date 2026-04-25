from .database import engine
from .models import Base


def main():
    # Создать все таблицы в БД, если их еще нет
    Base.metadata.create_all(bind=engine)
    print("Database tables created (if not exist).")


if __name__ == "__main__":
    main()

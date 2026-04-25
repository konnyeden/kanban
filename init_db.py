from database import engine
from models import Base
def main():
    Base.metadata.create_all(bind=engine)
    print("Database tables created (if not exist).")
if __name__ == "main":
    main()
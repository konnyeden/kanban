from server.database import engine
from server.models import Base
def main():
    Base.metadata.create_all(bind=engine)
    print("Database tables created (if not exist).")
if name == "main":
    main()
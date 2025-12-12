from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Define the Database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./safeflow.db"

# 2. Create the Engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Create SessionLocal (This fixes the ImportError)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create Base
Base = declarative_base()

# 5. DB Dependency
def get_conn():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
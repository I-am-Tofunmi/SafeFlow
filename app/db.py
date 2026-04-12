from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import os

# 1. Define the Database URL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./safeflow.db")

# 2. Create the Engine
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    # If using postgresql schema, sqlalchemy sometimes requires postgresql:// instead of postgres://
    if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)
        
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

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
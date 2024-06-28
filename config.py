from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

db_url = 'postgresql://postgres:root123@127.0.0.1:5432/fastapi'
engine = create_engine(db_url, echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Session = sessionmaker()

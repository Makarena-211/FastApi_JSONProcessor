from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



db_url = "postgresql+psycopg2://postgres:password@127.0.0.1:5433/postgres"
engine = create_engine(db_url)
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = Sessionlocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

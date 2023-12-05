from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

port = settings.SQLALCHEMY_DATABASE_URI
engine = create_engine(port)

Base = declarative_base()
session = sessionmaker(bind=engine)

print("Creating database...")
Base.metadata.create_all(engine)

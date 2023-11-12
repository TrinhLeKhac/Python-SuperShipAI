from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

port = 'postgresql://postgres:123456@localhost:5432/item_db'
engine = create_engine(port, echo=True)

Base = declarative_base()
session = sessionmaker(bind=engine)

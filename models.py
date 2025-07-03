from sqlalchemy import Column, Integer, String
from db import Base, engine

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(String(50), unique=True, index=True)
    title = Column(String(255))
    author = Column(String(255))
    isbn = Column(String(50))
    publisher = Column(String(100))
    pub_date = Column(String(20))
    lexile = Column(String(20))
    age_group = Column(String(50))
    award = Column(String(255))
    pages = Column(String(50))
    size = Column(String(100))
    format = Column(String(50))
    genre = Column(String(100))
    subject = Column(String(100))

Base.metadata.create_all(bind=engine)

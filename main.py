from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from db import SessionLocal, engine, Base
from models import Book
from contextlib import asynccontextmanager
import re

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

# FastAPI 앱 초기화
app = FastAPI(title="Wendybook Book API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# 의존성: DB 세션 주입
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 정렬 함수
def extract_lexile(lex: str) -> int:
    match = re.search(r"\b(\d+)[lL]?\b", lex)
    return int(match.group(1)) if match else -1

# 전체 도서 목록 조회 API (정렬/필터 지원)
@app.get("/books", summary="도서 전체 목록 (정렬/필터 지원)")
def get_books(
    limit: int = Query(20, ge=1),
    offset: int = Query(0, ge=0),
    sort: Optional[str] = Query(None),
    age_group: Optional[str] = Query(None),
    award: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Book)

    # 필터
    if age_group:
        query = query.filter(Book.age_group.like(f"%{age_group}%"))
    if award == "yes":
        query = query.filter(Book.award != "")
    elif award == "no":
        query = query.filter((Book.award == "") | (Book.award == None))

    # 정렬
    reverse = sort.startswith("-") if sort else False
    sort_key = sort.lstrip("-") if sort else None

    if sort_key == "title":
        query = query.order_by(Book.title.desc() if reverse else Book.title.asc())
    elif sort_key == "lexile":
        books = query.all()
        books.sort(key=lambda b: extract_lexile(b.lexile or ""), reverse=reverse)
        return books[offset:offset+limit]
    elif sort_key == "pub_date":
        query = query.order_by(Book.pub_date.desc() if reverse else Book.pub_date.asc())
    elif sort_key:
        raise HTTPException(status_code=400, detail=f"지원하지 않는 정렬 키: {sort_key}")

    return query.offset(offset).limit(limit).all()

# 도서 제목 검색 API
@app.get("/books/search", summary="도서 검색")
def search_books(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    keyword = f"%{q.strip().lower()}%"
    query = db.query(Book).filter(
        Book.book_id.ilike(keyword) |
        Book.title.ilike(keyword) |
        Book.isbn.ilike(keyword) |
        Book.genre.ilike(keyword) |
        Book.age_group.ilike(keyword) |
        Book.subject.ilike(keyword) |
        Book.award.ilike(keyword)
    )
    return query.all()

# 도서 추가 API(POST)
from pydantic import BaseModel

class BookCreate(BaseModel):
    book_id: str
    title: Optional[str] = ""
    isbn: Optional[str] = ""
    pages: Optional[str] = ""
    size: Optional[str] = ""
    format: Optional[str] = ""
    publisher: Optional[str] = ""
    pub_date: Optional[str] = ""
    genre: Optional[str] = ""
    age_group: Optional[str] = ""
    subject: Optional[str] = ""
    author: Optional[str] = ""
    lexile: Optional[str] = ""
    award: Optional[str] = ""

@app.post("/books/add", summary="도서 추가")
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# 도서 상세 조회
@app.get("/books/{book_id}")
def get_book(book_id: str, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.book_id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="해당 책을 찾을 수 없습니다.")
    return book
import csv
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Book

def safe_strip(value):
    return str(value).strip() if value is not None else ""

def load_books_from_csv(file_path: str):
    db: Session = SessionLocal()
    inserted, failed = 0, 0
    with open(file_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                cleaned_row = {k: safe_strip(v) for k, v in row.items()}
                book = Book(**cleaned_row)
                db.add(book)
                inserted += 1
            except Exception as e:
                failed += 1
                print(f"[에러] book_id={row.get('book_id')} 처리 실패: {e}")
        db.commit()
    db.close()
    print(f"데이터 이전 완료: 추가 {inserted}건, 실패 {failed}건")

if __name__ == "__main__":
    load_books_from_csv("books.csv")

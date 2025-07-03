# db.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 환경 변수 또는 기본값 설정
DB_USER = os.getenv("DB_USER", "fastapi")
DB_PASSWORD = os.getenv("DB_PASSWORD", "fastapi123")
DB_HOST = os.getenv("DB_HOST", "mysql-db")  # Docker Compose에선 'mysql-db', 로컬 테스트 시엔 'localhost'
DB_NAME = os.getenv("DB_NAME", "wendybook")

# MySQL 연결 URL (pymysql 드라이버 사용)
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"

# 1. 엔진 생성
engine = create_engine(
    DATABASE_URL,
    echo=True,           # SQL 로그 출력 (개발용)
    pool_pre_ping=True,  # 연결 전 ping 체크 (끊긴 연결 방지)
)

# 2. 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. 모든 모델이 상속받는 Base 클래스
Base = declarative_base()

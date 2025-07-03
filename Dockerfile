# 1. Python 베이스 이미지 사용
FROM python:3.10-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 앱 코드 복사
COPY . .

# 5. 포트 개방 (FastAPI 기본 8000)
EXPOSE 8000



# platform : 아키텍쳐 명시 리눅스 빌드 시 x96:64로
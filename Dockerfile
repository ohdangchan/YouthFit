FROM python:3.10-slim

WORKDIR /app

# 시스템 라이브러리 설치 (psycopg2 빌드 의존성)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 파이썬 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 전체 소스 복사
COPY . .

# 실행 포트 노출 (기본값 8000)
ENV PORT=8000
EXPOSE 8000

# 컨테이너 시작 명령어
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]

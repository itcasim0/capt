from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.default import settings

# 연결 설정
engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
# 세션 클래스
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

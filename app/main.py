import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy.orm import Session

from app.db.redis_helper import init_redis, is_connection

from app.service.capt import request_capt

from app.config.schema import InputMessage, Base
from app.config.database import engine, get_db

from app.utils.logger_factory import setup_logger, suppress_external_loggers

setup_logger()
suppress_external_loggers()


@asynccontextmanager
# TODO: redisDB, RDB, LLMProvidor 교통 정리 필요.
async def lifespan(app: FastAPI):
    logging.info("Starting...")

    # DB 초기화
    Base.metadata.create_all(bind=engine)
    logging.info("DB initialize successful.")

    # Redis 클라이언트 초기화
    app.state.redis = init_redis()
    if not is_connection(app.state.redis):
        logging.error("Redis connection failed")
        raise RuntimeError("Redis 연결에 실패했습니다. 서버를 다시 시작하세요.")
    logging.info("Redis initialize 및 connection successful.")

    yield  # 앱 실행

    logging.info("Shutdown...")


app = FastAPI(lifespan=lifespan)


@app.get("/test")
async def test():
    return {"Welcome to Server!"}


@app.post("/capt")
async def capt(
    input_message: InputMessage, request: Request, db: Session = Depends(get_db)
):
    try:
        redis_client = request.app.state.redis
        return request_capt(input_message, db, redis_client)
    except Exception as e:
        logging.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

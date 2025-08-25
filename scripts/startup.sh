#!/bin/bash

# 경로 설정
ROOT_PATH="/root/llm-api-server"
LOG_FILE="$ROOT_PATH/logs/server.log"

# 변수 설정
PORT=8001
APP_MODULE="app.main:app"
WORKERS=1

# 경로 이동
cd $ROOT_PATH

# 백그라운드 실행
nohup gunicorn $APP_MODULE \
    -k uvicorn.workers.UvicornWorker \
    --workers $WORKERS \
    --bind 0.0.0.0:$PORT \
    --access-logfile - \
    --error-logfile - \
    >> $LOG_FILE 2>&1 &

echo "FastAPI 서버가 백그라운드에서 실행 중입니다 (포트: $PORT, 워커: $WORKERS, 로그: $LOG_FILE)"
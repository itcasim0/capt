#!/bin/bash

# 실행 중인 uvicorn 프로세스를 찾고 종료
PID=$(ps aux | grep "gunicorn app.main:app" | grep -v grep | awk '{print $2}')

if [ -z "$PID" ]; then
  echo "실행 중인 FastAPI 서버가 없습니다."
else
  kill $PID
  echo "FastAPI 서버(PID: $PID)를 종료했습니다."
fi
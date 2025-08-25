@echo off
chcp 65001 > nul

:: .env.secret 파일에서 EXTERNAL_IP 값을 읽어서 환경 변수로 설정
for /f "tokens=1,* delims==" %%a in ('type ".env"') do (
    if "%%a"=="EXTERNAL_IP" set EXTERNAL_IP=%%b
)

:: POST 요청
curl -X POST "http://%EXTERNAL_IP%:8001/capt" ^
-H "Content-Type: application/json" ^
-d "{\"msg\": \"카피티야 나 방금 뭐라했냐?\"}"

echo.

pause
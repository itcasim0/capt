@echo off
chcp 65001 > nul

:: POST 요청
curl -X POST "http://localhost:8001/capt" ^
-H "Content-Type: application/json" ^
-d "{\"sender\": \"김철수\", \"room\": \"친구모임1\", \"msg\": \"진짜 부탁할게 한번만 조용해줘.\"}"

echo.
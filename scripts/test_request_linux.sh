#!/bin/bash

# POST 요청
curl -X POST "http://localhost:8001/capt" \
  -H "Content-Type: application/json" \
  -d '{"msg": "카피티 안녕? 기분이 어때?"}'

echo
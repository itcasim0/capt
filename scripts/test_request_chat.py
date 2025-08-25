import sys
import requests
import json
from pathlib import Path

import argparse

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

URL = "http://localhost:8001/capt"
HEADERS = {"Content-Type": "application/json"}
ROOM = "스터디방"


def main():
    # ArgumentParser 객체 생성
    parser = argparse.ArgumentParser()

    # 인자 정의
    parser.add_argument("user", type=str, help="사용자 명")

    # 인자 파싱
    args = parser.parse_args()

    while True:
        # 사용자 입력 받기
        user_input = input(f"{args.user}: ")

        # 종료 조건 확인
        if user_input.lower() in ["exit", "quit", "종료"]:
            print("\n대화를 종료합니다.")
            break

        data = {"sender": args.user, "room": ROOM, "msg": user_input}

        try:
            response = requests.post(URL, headers=HEADERS, data=json.dumps(data))
            # 응답 출력
            print(f"카피티: {response.json()["message"]}")

        except Exception as e:
            print(f"오류 발생: {str(e)}")
            print(response.text)


if __name__ == "__main__":
    main()

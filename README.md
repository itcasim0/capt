# 카카오톡 메신저 연동 LLM 기반 AI 봇

## 개요
* 카카오톡 메신저를 연동하여 LLM 기반의 AI 봇을 사용하기 위한 코드 입니다.
* 준비물: 서브폰(개통필수), LLM API, 서버
  * 서브폰은 알뜰폰으로 개통하면 6개월 통신 무료가 있음. (모요 플랫폼 추천)
  * LLM API 및 서버는 구글로 90일 무료를 통해서 Gemini API, GCP 서버 추천
* 서브폰에서 메신저봇R어플을 깔고 아래의 사이트에서 코드를 참고.
  * https://smecsm.tistory.com/264

## 버전 정보
* python==3.13
* langchain_google_genai
* FastAPI
* Redis
* SQLAlchemy

## 프로젝트 구조
```
.
├── app/                    # 애플리케이션 소스 코드
│   ├── api/                # 외부 API 연동 (Gemini API 등)
│   ├── config/             # 설정 파일
│   ├── db/                 # 데이터베이스 연동 (Redis, SQLite)
│   ├── service/            # 비즈니스 로직
│   └── utils/              # 유틸리티 함수
├── resources/
│   └── prompts/            # LLM 프롬프트 템플릿
│       └── character/      # 캐릭터별 프롬프트
├── scripts/                # 실행 및 테스트 스크립트
├── .env.example           # 환경 변수 예시 파일
└── README.md
```

## 환경 설정
### 로컬 개발 환경
1. 필수 환경 변수 설정
   - .env 파일을 생성하고 아래 내용을 설정합니다.
   ```
   DATABASE_URL=sqlite:///./data/server.db
   REDIS_HOST=localhost
   REDIS_PORT=6379
   LOG_LEVEL=info
   GOOGLE_API_KEY=<your-google-api-key>
   SERVER_PORT=8001
   ```

2. Redis 설치 및 실행
   - Windows 환경에서는 Redis를 별도로 설치하거나 Docker를 통해 실행할 수 있습니다.
   - Linux/macOS 환경에서는 아래 명령어로 설치 및 실행할 수 있습니다.
   ```bash
   sudo yum install epel-release -y
   sudo yum install redis -y
   sudo systemctl start redis
   sudo systemctl enable redis
   redis-cli ping
   ```

3. Python 환경 구성
   ```bash
   pip install uv
   uv sync
   ```

## 애플리케이션 실행
```bash
# 서버 시작
python -m app.main

# 또는 스크립트 사용
./scripts/startup.sh
```

## API 엔드포인트
- `/test` (GET): 서버 상태 확인
- `/capt` (POST): 채팅 메시지 전송 및 응답 수신
  ```json
  {
    "sender": "사용자명",
    "room": "채팅방명",
    "msg": "메시지 내용"
  }
  ```

## 테스트
다양한 테스트 스크립트를 제공합니다:
- `scripts/test_request_chat.py`: 대화형 채팅 테스트
  ```bash
  python scripts/test_request_chat.py 사용자명
  ```
- `scripts/test_request_dev_win.bat`: Windows 환경에서 로컬 API 테스트
- `scripts/test_request_prod_win.bat`: Windows 환경에서 배포된 API 테스트
- `scripts/test_request_linux.sh`: Linux 환경에서 API 테스트

## 채팅 모드
서비스는 다양한 채팅방 환경에 따라 다른 응답 전략을 사용합니다:
- 가족: 기본 응답 모드 (FAMILY 페르소나)
- 친구모임1/친구모임2/스터디방: 자연스러운 대화 모드 (FRIENDLY 페르소나)
- 기타 채팅방: 기본 응답 모드 (BASE 페르소나)

추가로 `/` 로 시작하는 메시지는 검색 기능을 활성화합니다.

## GCP 및 LLM API 설정 방법
### GCP VM 인스턴스 생성
1. Google Cloud Console에서 VM 인스턴스 만들기 클릭
2. 이름: 원하는 인스턴스 이름 설정
3. 머신구성은 기본 설정
   - 참고로 e2-medium (vCPU 2개, 메모리 4GB임)
4. OS 및 스토리지에서 OS 변경
    - CentOS Stream 9로 변경하면 용량은 20기가로 변경됨
5. 네트워킹
    - 기본 내부 IPv4 주소 고정 예약
    - 외부 IPv4 주소 고정 예약
      - server-static-ip 로 이름 입력
      - 외부 IP는 자동으로 지정.
6. 만들기 완료
7. 생성된 VM 클릭 후 아래에 네트워크 인터페이스에서 세부 정보 클릭후 좌측 방화벽 누르고 방화벽 규칙 만들기
   - 이름 : allow-8001
   - 대상 : 네트워크의 모든 인스턴스
   - 프로토콜 및 포트: 지정된 프로토콜 및 포트
     - TCP 체크 : 포트는 .env의 PORT확인

### SSH 연결 설정
1. SSH 브라우저 통해 연결하기
   - SSH 방화벽도 같이 열어주고, 공개키를 설정해야 함
   - (sudo su 하면 root 계정)

2. VSCode 연동하기
   - 공개키는 기존에 있는 거 사용
   - ~/.ssh/authorized_keys 만들어서 안에 공개키 넣기
   - 연동 확인하기

## Migration Server
* Google Cloud Console (GCC) 무료 계정을 활용하고 있음
  * 따라서, 90일 마다 서버를 이관해야함

### GCC VM Instance 생성 및 설정
* GCC 내에 VM 인스턴스 만들기 클릭
  * 이후 사용 버튼 누르고 다음 페이지 넘어갈 때 까지 기다리기 (시간이 조금 걸림)

### Google AI Studio
* 서버 이관 계정으로 로그인
* Get API Key 버튼 클릭
* 발급 후 .env.secret 변경

## Setting Production

### VSCode Extension
* Python
* Cline
* Redis for VS Code

### Git 환경 구성
git 설치 및 clone
```
sudo yum install git -y
git clone https://github.com/itcasim0/llm-api-server.git
```
* 단, github는 현재 token으로 로그인하는 방식으로 바뀌었음
  * .env.secret 확인

### Python 환경 구성
* 설치 및 환경 구성
```
sudo yum install python3-pip -y
pip install uv
uv sync
```
* 이 때 .python-version에 맞춰 알아서 .venv 생성 후 python 버전 설치됨
* 대신 pip은 python 버전과 맞지 않은 것이 흠이니 추후 확인 필요


## 서버 운영 관리
### 서버 시작/종료
* 시작: `scripts/startup.sh`
* 종료: `scripts/shutdown.sh`

### 모니터링
* 로그는 `logs` 디렉토리에 저장됨
* LOG_LEVEL 환경 변수를 통해 로그 레벨 조정 가능 (info, debug, error 등)

from typing import Optional

from google import genai
from google.genai.types import Tool, GoogleSearch, GenerateContentConfig

from app.config.default import settings


def _request_google(contents, model: str, config=None):
    client = genai.Client(api_key=settings.google_api_key)
    return client.models.generate_content(model=model, contents=contents, config=config)


def request_google(
    message: str,
    model: str = "gemini-2.0-flash",
    system_instruction: str = None,
    search: Optional[bool] = None,
):
    if search:
        search = [Tool(google_search=GoogleSearch())]

    configs = dict(
        system_instruction=system_instruction,
        max_output_tokens=8192,
        temperature=1,
        tools=search,
        response_modalities=["TEXT"],
    )  # gemini-2.0-flash는 max_tokens가 8,192임.

    return _request_google(message, model, config=GenerateContentConfig(**configs)).text


def create_chat(
    history: list[dict],
    model: str = "gemini-2.0-flash",
    system_instruction: str = None,
    search: Optional[bool] = None,
):
    # TODO: 그냥 chat 객체 함수는 뜯어서 커스텀 하는 게 나을 지도..?
    # TODO: 그냥 OpenAI SDK를 활용하는 방안도 검토.
    """Gemini chat 객체를 생성하는 함수.

    Args:
        history (list[dict]): 대화 히스토리. 다음과 같은 형식이어야 합니다.
        ex) [{"role": "user", "parts": [{"text": "안녕?"}]},
             {"role": "model", "parts": [{"text": "그래 안녕?"}]}]
        또 한, 반드시 첫번 째는 role은 user여야 함.
        model (str): 사용할 모델 이름. 기본값은 "gemini-2.0-flash".
        system_instruction (str): 시스템 역할 지시어 (선택).
        search (bool): Google Search 툴 사용 여부 (선택).

    Returns:
        genai.Chat: 생성된 chat 객체
    """

    # search tool 활용 유/무
    if search:
        search = [Tool(google_search=GoogleSearch())]

    # model 별 hyperparameters
    if model == "gemini_2.0-flash":
        # gemini-2.0-flash는 max_tokens가 8,192임.
        max_output_tokens = 8192
    else:
        max_output_tokens = None

    # chat object 생성을 위한 config
    configs = dict(
        system_instruction=system_instruction,
        max_output_tokens=max_output_tokens,
        temperature=1,
        tools=search,
        response_modalities=["TEXT"],
    )

    client = genai.Client(api_key=settings.google_api_key)
    return client.chats.create(
        model=model, config=GenerateContentConfig(**configs), history=history
    )

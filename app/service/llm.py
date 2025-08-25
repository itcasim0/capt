from typing import List
import logging
from threading import Lock

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# TODO: LLM API 요청 라이브러리는 항상 고민.. (openai vs google vs langchain)
from app.api.gemini import request_google

from app.utils.util import read_file

from app.config.schema import Message
from app.config.default import PROMPTS_PATH, SEARCH

logger = logging.getLogger(__name__)


class LLMProvider:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_inited", False):
            return
        self._inited = True

        self.base_chain = self._build_base_chain()
        self.natural_chain = self._build_natural_chain()

    # TODO: chat_history가 아닌 system, user, assistant를 활용한 구조로 요청한다면 성능이 어떨 지 비교.
    def _build_base_chain(self):
        """
        base chain에는 persona, chat_history, name이 필요합니다.
        """

        llm_model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", temperature=1, request_timeout=30
        )

        system_prompt = read_file(PROMPTS_PATH / "build_base.txt")
        chat_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                (
                    "user",
                    "\n\n{chat_history}\n{name}:",
                ),
            ]
        )

        return chat_prompt | llm_model

    # TODO: chat_history가 아닌 system, user, assistant를 활용한 구조로 요청한다면 성능이 어떨 지 비교.
    def _build_natural_chain(self):
        """
        natural chain에는 persona, chat_history, name이 필요합니다.
        """
        llm_model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", temperature=0.1, request_timeout=30
        )

        system_prompt = read_file(PROMPTS_PATH / "build_natural.txt")
        chat_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                (
                    "user",
                    "\n\n{chat_history}\n{name}:",
                ),
            ]
        )

        return chat_prompt | llm_model


def get_llm_provider() -> LLMProvider:
    return llm_provider


llm_provider = LLMProvider()


def base(
    messages: List[Message], persona: str, name: str, chain=llm_provider.base_chain
) -> Message:

    chat_history = "\n".join(
        [f"{message.sender} : {message.msg}" for message in messages]
    )
    logger.debug(f"Chat History: \n{chat_history}")

    chat_prompt: str = chain.steps[0]
    logger.debug(
        f"Formatted Prompt:\n{chat_prompt.format(persona=persona.format(name=name),
    chat_history=chat_history, name=name)}"
    )

    try:
        logger.debug("Invoking LLM chain...")
        result = chain.invoke(
            {
                "persona": persona.format(name=name),
                "chat_history": chat_history,
                "name": name,
            },
            timeout=40,  # 타임아웃 명시적 설정
        )
        logger.debug(f"Result received: \n{result}")
        response = (
            result.content.strip() if result and hasattr(result, "content") else ""
        )
        logger.debug(f"Processed response: '{response}'")
    except Exception as e:
        logger.error(f"Error invoking LLM chain: {str(e)}")
        # 오류 발생 시 공백으로 응답
        response = ""

    return response


def natural(
    messages: List[Message],
    persona: str,
    name: str,
) -> str:

    return base(
        messages=messages, persona=persona, name=name, chain=llm_provider.natural_chain
    )


# TODO: langchain을 통한 web search 기능 확인.
def search(message: str):
    return (
        request_google(message, system_instruction=SEARCH, search=True)
        .rstrip("\n")
        .lstrip(" ")
    )

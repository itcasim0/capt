from functools import partial
from typing import Callable, Dict, List

from app.service.llm import base, search, natural

from app.config.schema import Message
from app.config.default import BASE, FRIENDLY, FAMILY


def _base(messages: List[Message], persona=BASE, name="카피티"):

    last_message = messages[-1]
    if "카피티" in last_message.msg:
        response = base(messages, persona=persona, name=name)
    elif last_message.msg.startswith("/"):
        response = search(last_message.msg)
    else:
        response = ""

    return Message(room=last_message.room, msg=response, sender=name)


def _natural(messages: List[Message], persona=BASE, name="카피티"):

    last_message = messages[-1]
    if last_message.msg.startswith("/"):
        response = search(last_message.msg)
    else:
        response = natural(messages, persona=persona, name=name)

    return Message(room=last_message.room, msg=response, sender=name)


Handler = Callable[[List[Message]], Message]

STRATEGIES: Dict[str, Handler] = {
    "가족": partial(_base, persona=FAMILY),
    "친구모임1": partial(_natural, persona=FRIENDLY),
    "친구모임2": partial(_natural, persona=FRIENDLY),
    "스터디방": partial(_natural, persona=FRIENDLY),
}


def request_chat(messages: List[Message]) -> Message:

    # 특정 채팅방 명은 별도의 서비스로 분기하며, 그 외는 base 서비스 호출
    room_key = messages[-1].room
    return STRATEGIES.get(room_key, _base)(messages)

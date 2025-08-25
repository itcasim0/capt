import json

from sqlalchemy.orm import Session
import redis

from app.db import redis_helper, db_helper

from app.service.chat import request_chat

from app.config.schema import InputMessage, Message


def request_capt(input_message: InputMessage, db: Session, redis_client: redis.Redis):
    # to message from message_request
    message = Message.from_message_request(input_message)

    # RDB에 입력 메세지를 저장
    db_helper.save_message_to_db(input_message, db)

    # 채팅방 구분을 위한 key를 정의하고, 입력 메세지를 redisDB에 저장.
    key = f"chat:session:{message.room}"
    redis_helper.save_data(
        redis_client=redis_client, key=key, data=message.model_dump_json()
    )

    # 이전 메세지와 입력메세지를 포함하여 로드 후 AI에 request.
    messages = _load_messages(redis_client=redis_client, key=key)
    response: Message = request_chat(messages=messages)

    # redisDB에 AI 응답 저장.
    redis_helper.save_data(
        redis_client=redis_client, key=key, data=response.model_dump_json()
    )
    # TODO: RDB에 AI 응답 저장.

    # response가 None 또는 "" 일 경우에는 카피티가 아무런 대답을 하지 않음.
    return {"message": response.msg}


def _load_messages(redis_client: redis.Redis, key: str):
    messages = redis_helper.load_data(redis_client, key=key)
    return [Message(**json.loads(message)) for message in messages]

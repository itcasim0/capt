from __future__ import annotations

from typing import Optional, List
from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.ext.declarative import declarative_base


class InputMessage(BaseModel):
    """
    Represents a chat message with optional metadata.

    Attributes:
        room (Optional[str]): The chat room name.
        msg (str): The content of the message.
        sender (Optional[str]): The sender's name.
        isGroupChat (Optional[bool]): Indicates if the message is from a group chat.
        profileImage (Optional[str]): Base64-encoded string of the sender's profile image.
        packageName (Optional[str]): The package name of the app that sent the message.
            ex) kakaotalk: com.kakao.talk
    """

    model_config = ConfigDict(populate_by_name=True)  # by_alias 여부 제어

    room: Optional[str] = None
    msg: Optional[str] = None
    sender: Optional[str] = None
    is_group_chat: Optional[bool] = Field(default=None, alias="isGroupChat")
    profile_image: Optional[str] = Field(
        default=None, alias="profileImage"
    )  # base64 문자열
    package_name: Optional[str] = Field(default=None, alias="packageName")


class Message(BaseModel):
    """
    Attributes:
    """

    room: Optional[str] = None
    msg: Optional[str] = None
    sender: Optional[str] = None

    @classmethod
    def from_message_request(cls, message_request: InputMessage) -> Message:
        return cls(**message_request.model_dump(include={"room", "msg", "sender"}))


# Base 클래스
Base: DeclarativeMeta = declarative_base()


class MessageEntity(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    room = Column(String, nullable=True)
    msg = Column(String)
    sender = Column(String, nullable=True)
    is_group_chat = Column(Boolean, nullable=True)
    package_name = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.now(ZoneInfo("Asia/Seoul")))

    @classmethod
    def from_input_message(cls, input_message: InputMessage) -> MessageEntity:
        message_entity = input_message.model_dump(
            by_alias=False, exclude={"profile_image"}
        )
        message_entity["timestamp"] = datetime.now(ZoneInfo("Asia/Seoul"))
        return cls(**message_entity)


class ChatState(BaseModel):
    messages: List[Message]
    prompt: str
    name: str
    should_intervene: bool = False
    response: str = ""

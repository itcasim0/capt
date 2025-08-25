from sqlalchemy.orm import Session

from app.config.schema import InputMessage, MessageEntity


def save_message_to_db(input_message: InputMessage, db: Session):
    message_entity = MessageEntity.from_input_message(input_message)
    db.add(message_entity)
    db.commit()
    db.refresh(message_entity)

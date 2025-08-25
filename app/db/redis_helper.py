import redis

from app.config.default import settings

# TODO: class로 수정

def init_redis(
    host=settings.redis_host, port=settings.redis_port, db=0, decode_response=True
):
    return redis.Redis(host=host, port=port, db=db, decode_responses=decode_response)


def is_connection(redis_client: redis.Redis):
    if not redis_client.ping():
        return False
    return True

def load_data(redis_client: redis.Redis, key: str):
    # key에 해당하는 채팅 기록 모두 불러오기
    return redis_client.lrange(key, 0, -1)


def save_data(
    redis_client: redis.Redis, key: str, data: str, duration=30, max_message=10
):
    # 메시지 리스트에 추가
    redis_client.rpush(key, data)

    # 리스트 길이가 max_message개를 초과하면 앞에서 제거
    redis_client.ltrim(key, -max_message, -1)

    # 마지막 갱신으로부터 duration 동안 데이터 유효
    redis_client.expire(key, duration)

    return True

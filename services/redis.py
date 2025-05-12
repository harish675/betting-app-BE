# services/redis.py

import redis

class RedisService:
    def __init__(self):
        self.client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

    def store_otp(self, phone: str, otp: str, ttl_seconds: int = 300):
        self.client.setex(f"otp:{phone}", ttl_seconds, otp)

    def get_otp(self, phone: str) -> str | None:
        return self.client.get(f"otp:{phone}")

    def delete_otp(self, phone: str):
        self.client.delete(f"otp:{phone}")
    
    def store_email_otp(self, email: str, otp: str, ttl_seconds: int = 300):
        self.client.setex(f"otp:email:{email}", ttl_seconds, otp)

    def get_email_otp(self, email: str) -> str | None:
        return self.client.get(f"otp:email:{email}")

    def delete_email_otp(self, email: str):
        self.client.delete(f"otp:email:{email}")

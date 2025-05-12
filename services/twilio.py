from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from ..core.config import settings


class TwilioService:
    def __init__(self):
        self.client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN,
        )
        self.from_number = settings.TWILIO_PHONE_NUMBER

    def send_message(self, to_number: str, message: str):
        try:
            message = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number,
            )
            return message.sid
        except TwilioRestException as e:
            print(f"Failed to send message: {e}")
            return None
        


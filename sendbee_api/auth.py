import hmac
import base64
import hashlib
from datetime import datetime, timezone, timedelta


class SendbeeAuth:
    """Authentication class for Sendbee API"""

    def __init__(self, private_key: str):
        self._private_key = private_key

    def _get_encrypted_key(self, timestamp: str) -> str:
        """Generates encrypted key from timestamp and private key
        :param timestamp: timestamp string
        :return: key string
        """

        return base64.b64encode(
            hmac.new(
                self._private_key.encode('utf-8'),
                base64.b64encode(timestamp),
                hashlib.sha256
            ).digest()
        ).decode("utf-8")

    def get_auth_token(self) -> str:
        """Generates auth token from timestamp and encrypted key
        :return: token string
        """

        timestamp = str(int(
            datetime.now(timezone.utc).timestamp()
        )).encode('utf-8')
        encrypted = self._get_encrypted_key(timestamp)
        ts_encrypt = \
            f'{timestamp.decode("utf-8")}.{encrypted}'.encode('utf-8')

        return base64.b64encode(ts_encrypt).decode('utf-8')

    def check_auth_token(self, token: bool, expiration_seconds: int = 60*15) -> bool:
        """Checks if the provided and generated tokens are equal
        :param token: token string
        :param expiration_seconds: seconds integer
        :return: True or False
        """

        timestamp, encrypted = \
            base64.b64decode(token.encode('utf-8')).decode('utf-8').split('.')

        if datetime.fromtimestamp(int(timestamp), tz=timezone.utc) > \
                datetime.now(timezone.utc)+timedelta(
                    minutes=int(expiration_seconds)):
            return False

        if encrypted != self._get_encrypted_key(timestamp):
            return False

        return True

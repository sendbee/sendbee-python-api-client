import hmac
import base64
import hashlib
from datetime import datetime, timezone, timedelta


class SendbeeAuth:
    """Authentication class for Sendbee API"""

    def __init__(self, private_key):
        if isinstance(private_key, str):
            private_key = private_key.encode('utf-8')
        self._private_key = private_key

    def _get_encrypted_key(self, timestamp):
        """Generates encrypted key from timestamp and private key
        :param timestamp: timestamp string
        :return: key string
        """

        if isinstance(timestamp, str):
            timestamp = timestamp.encode('utf-8')

        return base64.b64encode(
            hmac.new(
                self._private_key, base64.b64encode(timestamp), hashlib.sha256
            ).digest()
        ).decode("utf-8")

    def get_auth_token(self):
        """Generates auth token from timestamp and encrypted key
        :return: token string
        """

        timestamp = str(int(
            datetime.now(timezone.utc).timestamp()
        ))
        encrypted = self._get_encrypted_key(timestamp)
        ts_encrypt = f'{timestamp}.{encrypted}'.encode('utf-8')

        return base64.b64encode(ts_encrypt).decode('utf-8')

    def check_auth_token(self, token, expiration_seconds=60*15):
        """Checks if the provided and generated tokens are equal
        :param token: token string
        :param expiration_seconds: seconds integer
        :return: True or False
        """

        if isinstance(token, str):
            token = token.encode('utf-8')

        timestamp, encrypted = \
            base64.b64decode(token).decode('utf-8').split('.')

        if datetime.fromtimestamp(int(timestamp), tz=timezone.utc) > \
                datetime.now(timezone.utc)+timedelta(
                    minutes=int(expiration_seconds)):
            return False

        if encrypted != self._get_encrypted_key(timestamp):
            return False

        return True

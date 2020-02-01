import hmac
import base64
import hashlib
from datetime import datetime, timezone, timedelta


class SendbeeAuth:

    def __init__(self, private_key):
        self._privat_key = private_key

    def _get_encrypted_key(self, timestamp):
        return base64.b64encode(
            hmac.new(
                self._privat_key.encode('utf-8'),
                base64.b64encode(timestamp.encode('utf-8')),
                hashlib.sha256
            ).digest()
        ).decode("utf-8")

    def get_auth_token(self):
        timestamp = str(int(
            datetime.now(timezone.utc).timestamp()
        )).encode('utf-8')
        encrypted = self._get_encrypted_key(timestamp)
        ts_encrypt = \
            f'{timestamp.decode("utf-8")}.{encrypted.decode("utf-8")}'\
                .encode('utf-8')
        return base64.b64encode(ts_encrypt).decode('utf-8')

    def check_auth_token(self, token, expiration_seconds=60*15):
        timestamp, encrypted = \
            base64.b64decode(token.encode('utf-8')).decode('utf-8').split('.')

        if datetime.fromtimestamp(int(timestamp), tz=timezone.utc) > \
                datetime.now(timezone.utc)+timedelta(minutes=expiration_seconds):
            return False

        if encrypted != self._get_encrypted_key(timestamp):
            return False

        return True

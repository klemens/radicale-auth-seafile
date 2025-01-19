from psycopg2 import connect
from passlib.crypto.digest import pbkdf2_hmac
from radicale.auth import BaseAuth

class Auth(BaseAuth):
    def _login(self, user, password):
        hash = self._read_hash(user)
        if hash is not None:
            if self._check_pbkdf2sha256(password, hash):
                return user
        return ""

    def _check_pbkdf2sha256(self, password, hash):
        hashParts = hash.split("$")
        if len(hashParts) == 4 and hashParts[0] == "PBKDF2SHA256":
            iterations = int(hashParts[1])
            saltBytes = bytes.fromhex(hashParts[2])
            storedHash = bytes.fromhex(hashParts[3])

            computedHash = pbkdf2_hmac(
                digest = "sha256",
                secret = password,
                salt = saltBytes,
                rounds = iterations,
            )

            return storedHash == computedHash
        else:
            self.logger.warning("Unknown seafile hash-format: %s", hash)
            return False

    def _read_hash(self, email):
        cursor = self._get_db_connection().cursor()

        query = "SELECT passwd FROM emailuser WHERE email = %s"
        cursor.execute(query, (email,))

        result = cursor.fetchone()
        if result is not None and len(result) > 0:
            return result[0]
        else:
            self.logger.info("Cannot find seafile user %s", email)
            return None

    def _get_db_connection(self):
        # Initial connect
        if not hasattr(self, "_db"):
            _db = self._db_connect()

        # Check if connection is alive and reconnect if not
        try:
            test = _db.cursor()
            test.execute("SELECT 1")
        except:
            self.logger.warning("Reconnect because of broken seafile db connection")
            _db = self._db_connect()

        return _db

    def _db_connect(self):
        uri = self.configuration.get("auth", "seafile_db")
        return connect(uri)

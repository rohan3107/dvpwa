from hashlib import md5, sha256
from typing import NamedTuple, Optional

from aiopg import Connection


class User(NamedTuple):
    id: int
    first_name: str
    middle_name: Optional[str]
    last_name: str
    username: str
    pwd_hash: str
    is_admin: bool

    @classmethod
    def from_raw(cls, raw: tuple):
        return cls(*raw) if raw else None

    @staticmethod
    async def get(conn: Connection, id_: int):
        async with conn.cursor() as cur:
            await cur.execute(
                'SELECT id, first_name, middle_name, last_name, '
                'username, pwd_hash, is_admin FROM users WHERE id = %s',
                (id_,),
            )
            return User.from_raw(await cur.fetchone())

    @staticmethod
    async def get_by_username(conn: Connection, username: str):
        async with conn.cursor() as cur:
            await cur.execute(
                'SELECT id, first_name, middle_name, last_name, '
                'username, pwd_hash, is_admin FROM users WHERE username = %s',
                (username,),
            )
            return User.from_raw(await cur.fetchone())

    @staticmethod
    def _get_sha256_hash(password: str) -> str:
        return sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def _get_md5_hash(password: str) -> str:
        return md5(password.encode('utf-8')).hexdigest()

    def check_password(self, password: str) -> bool:
        # Try SHA256 first (new format)
        if len(self.pwd_hash) == 64:  # SHA256 hash length
            return self.pwd_hash == self._get_sha256_hash(password)
        # Fall back to MD5 (legacy format)
        return self.pwd_hash == self._get_md5_hash(password)

    def get_upgraded_hash(self, password: str) -> str:
        """Get SHA256 hash for password upgrade if current password matches."""
        if self.check_password(password):
            return self._get_sha256_hash(password)
        return self.pwd_hash  # Return existing hash if password doesn't match

    @staticmethod
    async def update_password_hash(conn: Connection, user_id: int, new_hash: str) -> None:
        """Update the password hash for a user in the database."""
        async with conn.cursor() as cur:
            await cur.execute(
                'UPDATE users SET pwd_hash = %s WHERE id = %s',
                (new_hash, user_id),
            )

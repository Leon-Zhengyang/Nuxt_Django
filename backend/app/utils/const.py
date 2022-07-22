from enum import Enum


class UserType(Enum):
    """ユーザータイプ"""

    USER = 1
    SUPERUSER = 9

    def __str__(self):
        """日本語名"""
        names = {
            self.USER: "一般利用者",
            self.SUPERUSER: "スーパーユーザー",
        }
        return names[self]

    @classmethod
    def choices(cls):
        """一覧を返す"""
        return [(user_type.value, str(user_type)) for user_type in cls]

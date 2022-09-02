from enum import Enum


class Roles(Enum):
    USER = 'Пользователь'
    MODERATOR = 'Модератор'
    ADMIN = 'Администратор'

    @classmethod
    def choices(cls):
        return tuple((i.name.lower(), i.value) for i in cls)

    @classmethod
    def max_len(cls) -> int:
        return len(max([i.name for i in cls], key=len))

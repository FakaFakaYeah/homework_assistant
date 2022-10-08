class APIstatusCodeNot200Error(Exception):
    """Код ответа должен быть равен 200."""
    pass


class TelegramMessageError(Exception):
    """Исключение на случай, если ответ API некорректен."""
    pass


class JsonError(Exception):
    """Исключение на случай, если полученный json некорректен."""
    pass


class ConnectError(Exception):
    """Исключение на случай, если не удалось подключится к адресу."""
    pass

class APIstatusCodeNot200Error(Exception):
    """Код ответа должен быть равен 200."""
    pass


class KeysError(Exception):
    """Исключение на случай, если ответ API некорректен."""
    pass

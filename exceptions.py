class LoggerError(Exception):
    """Класс для ошибок, которые нужно только логировать"""
    pass


class APIstatusCodeNot200Error(Exception):
    """Код ответа должен быть равен 200."""
    pass


class TelegramMessageError(LoggerError):
    """Исключение на случай, если при отправке в телеграмм ошибка."""
    pass


class ConnectAndJsonError(Exception):
    """Исключение на случай, если не удалось подключится к адресу."""
    pass


class CurrentDateKeyError(LoggerError):
    """Исключение на случай, если не удалось получит ключ current_date."""
    pass

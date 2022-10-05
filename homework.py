import os
import time
import logging
from logging import StreamHandler
import sys
from http import HTTPStatus

import requests
from dotenv import load_dotenv
import telegram

from exceptions import APIstatusCodeNot200

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s - [%(levelname)s] - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

LAST_MESSAGE = ''


def last_error_message(message):
    """Исключение повторной отправки одинаковых сообщений об ошибках."""
    return message != LAST_MESSAGE


def send_message(bot, message):
    """Функция отправки сообщения."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.info('Сообщение отправленное в Телегграмм')
        global LAST_MESSAGE
        LAST_MESSAGE = message
    except Exception as error:
        logger.error(f'Сбой при отправке сообщения {error}')


def get_api_answer(current_timestamp):
    """Функция подключения к API яндекса."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        request = requests.get(ENDPOINT, headers=HEADERS, params=params)
        logger.info(f'Запрос к {ENDPOINT} прошел успешно')
    except Exception as error:
        logger.error(f'{ENDPOINT} недоступен {error}')
        raise
    if request.status_code != HTTPStatus.OK:
        raise APIstatusCodeNot200(f'Код запроса API равен'
                                  f' {requests.status_codes} ')
    return request.json()


def check_response(response):
    """Функция проверки ответа API."""
    if type(response) != dict:
        logger.error('В ответе отсутствует словарь!')
        raise TypeError('В ответе отсутствует словарь!')
    homeworks = response.get('homeworks')
    if homeworks is None:
        logger.error('Нет ответа по ключу homeworks')
        raise KeyError('Нет ответа по ключу homeworks')
    if type(homeworks) != list:
        logger.error('В ответе отсутствует список')
        raise TypeError('В ответе отсутствует список')
    if len(homeworks) > 0:
        return homeworks
    else:
        logger.debug('Отсутствуют новые статусы домашних работ!')


def parse_status(homework):
    """Функция проверки статуса домашней работы."""
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if homework_status not in HOMEWORK_STATUSES:
        logger.error('Полученный статус Д-З не документирован')
        raise KeyError('Полученный статус Д-З не документирован')
    verdict = HOMEWORK_STATUSES[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Функция проверки обязательных элеиентов окружения."""
    if (PRACTICUM_TOKEN is None
            or TELEGRAM_TOKEN is None or TELEGRAM_CHAT_ID is None):
        logger.critical('Отсутствуют обязательные переменные окружения!'
                        'Бот остановлен')
        return False
    return True


def main():
    """Основная логика работы бота."""
    logger.info('Бот начал свою работу')
    if check_tokens() is False:
        return None
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    while True:
        try:
            response = get_api_answer(current_timestamp)
            check_response_homework = check_response(response)
            if type(check_response_homework) == list:
                for homework in check_response_homework:
                    message = parse_status(homework)
                    send_message(bot, message)
            current_timestamp = response.get('current_date')
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
            if last_error_message(message):
                send_message(bot, message)
        time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()

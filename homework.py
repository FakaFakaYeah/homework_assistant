import os
import time
import logging
import sys
from http import HTTPStatus

import requests
from dotenv import load_dotenv
from telegram import TelegramError, Bot

from exceptions import (
    APIstatusCodeNot200Error, TelegramMessageError,
    ConnectAndJsonError, CurrentDateKeyError
)

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def send_message(bot, message):
    """Функция отправки сообщения."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except TelegramError as error:
        raise TelegramMessageError(
            f'Сообщение "{message}" не было отправлено в Телеграм.'
            f' Ошибка: {error}.'
        )
    else:
        logger.info('Сообщение отправленное в Телеграм')


def get_api_answer(current_timestamp):
    """Функция подключения к API яндекса."""
    params = {'from_date': current_timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
        if response.status_code != HTTPStatus.OK:
            raise APIstatusCodeNot200Error(
                f'{ENDPOINT} недоступен, код ответа: {response.status_code}'
            )
        return response.json()
    except requests.exceptions.RequestException as error:
        raise ConnectAndJsonError(f'Запрос завершился с ошибкой {error}')


def check_response(response):
    """Функция проверки ответа API."""
    if not isinstance(response, dict):
        raise TypeError('В ответе отсутствует словарь!')
    homeworks = response.get('homeworks')
    current_date = response.get('current_date')
    if homeworks is None:
        raise KeyError('Нет ответа по ключу homeworks')
    if current_date is None:
        raise CurrentDateKeyError('Нет ответа по ключу current_date')
    if not isinstance(homeworks, list):
        raise TypeError('В ответе отсутствует список')
    return homeworks


def parse_status(homework):
    """Функция проверки статуса домашней работы."""
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if homework_name is None:
        raise KeyError('Отсутствует ответ по ключу homework_name')
    if homework_status not in HOMEWORK_VERDICTS:
        raise KeyError(f'Статус {homework_status} не документирован')
    verdict = HOMEWORK_VERDICTS[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Функция проверки обязательных элементов окружения."""
    return all((PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID))


def main():
    """Основная логика работы бота."""
    logging.basicConfig(
        format='%(asctime)s - [%(levelname)s] - %(message)s - '
               'Имя функции:[%(funcName)s] - %(lineno)d',
        handlers=[logging.StreamHandler(sys.stdout)])
    logger.info('Бот начал свою работу')
    if not check_tokens():
        logger.critical('Отсутствуют обязательные переменные окружения!'
                        'Бот остановлен')
        sys.exit('Ошибка! Бот остановлен')
    bot = Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    last_error = ""
    while True:
        try:
            response = get_api_answer(current_timestamp)
            check_response_homework = check_response(response)
            if len(check_response_homework) > 0:
                for homework in check_response_homework:
                    message = parse_status(homework)
                    send_message(bot, message)
            else:
                logger.info('Отсутствуют новые статусы домашних работ!')
            current_timestamp = response.get('current_date')
        except (TelegramMessageError, CurrentDateKeyError) as error:
            logger.error(error)
        except Exception as error:
            message = f"Сбой в работе программы: {error}"
            logger.error(message)
            try:
                if str(error) != str(last_error):
                    send_message(bot, message)
            except TelegramMessageError as error:
                logger.error(error)
            else:
                last_error = error
        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()

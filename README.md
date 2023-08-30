# **Homework Assistant - Бот для получения статусов домашних работ**

### Оглавление
<ol>
 <li><a href="#description">Описание проекта</a></li>
 <li><a href="#stack">Используемые технологии</a></li>
 <li><a href="#api_token">Получение API токена</a></li>
 <li><a href="#env">Шаблон наполнения env файла</a></li>
 <li><a href="#docker">Как запустить проект в Docker?</a></li>
 <li><a href="#start_project">Как развернуть проект локально локально?</a></li>
 <li><a href="#author">Авторы проекта</a></li>
</ol>

---
### Описание проекта:<a name="description"></a>
Бот запрашивает новые статусы домашних работ студентов яндекса
с интервалов в 10 минут. Если получен новый статус домашней работы
бот отправляет сообщение пользователю в телеграм.

### **Используемые технологии**<a name="stack"></a>
![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![](https://img.shields.io/badge/Python_telegram_bot-gray?style=for-the-badge)
![](https://img.shields.io/badge/PYTEST-blue?style=for-the-badge&logo=pytest&logoColor=white)

---
### Получение API токена<a name="api_token"></a>

* Перейдите по ссылке и получите токен [Нажми на меня!](https://oauth.yandex.ru/verification_code#access_token=y0_AgAAAABft3DpAAYckQAAAADrc1GWOCl-IgZORDC6N51ElwAFzTxaRac&token_type=bearer&expires_in=2587372)

---
### Шаблон наполнения env файла<a name="env"></a>

* В корневой директории проекта создайте .env файл и заполните его по шаблону

    ```
    API_TOKEN=  #Токен, который вы получили по инструкции выше
    TELEGRAM_TOKEN=  #Токен, полученый от @bot_father в телеграм
    TELEGRAM_CHAT_ID=  #ID чата для отправки сообщений, можно узнать у @userinfobot
    ```
 
___
### Как запустить проект в Docker?<a name="docker"></a>

* Запустите терминал и клонируйте репозиторий 
    ```
    git clone https://github.com/FakaFakaYeah/homework_assistant.git
    ```
  
* Установите Docker по ссылке https://www.docker.com/products/docker-desktop

* Заполните .env файл по шаблону указанному выше

* Соберите актуальный образ из DockerFile

    ```
    docker build -t homework_bot .
    ```
* Запустите образ в контейнере

    ```
    docker run -d --name homework_bot homework_bot
    ```

___
### Как развернуть проект локально локально?<a name="start_project"></a>

* Запустите терминал и клонируйте репозиторий 
    ```
    git clone https://github.com/FakaFakaYeah/homework_assistant.git
    ```
  
* Создайте и активируйте виртуальное окружение

  Если у вас Linux/macOS

  ```
  python3 -m venv venv
  source venv/bin/activate
  ```
  
  Если у вас windows

  ```
  python -m venv venv
  source venv/scripts/activate
  ```
  
* Установите зависимости из файла requirements.txt:

  ```
  pip install -r requirements.txt
  ```
  
* Заполните .env файл по шаблону указанному выше

* Запустите проект

    ```
    python homework.py
    ```

___
### Авторы проекта:<a name="author"></a>
Смирнов Степан
<div>
  <a href="https://github.com/FakaFakaYeah">
    <img src="https://github.com/FakaFakaYeah/FakaFakaYeah/blob/main/files/images/GitHub.png" title="GitHub" alt="Github" width="39" height="39"/>&nbsp
  </a>
  <a href="https://t.me/s_smirnov_work" target="_blank">
      <img src="https://github.com/FakaFakaYeah/FakaFakaYeah/blob/main/files/images/telegram.png" title="Telegram" alt="Telegram" width="40" height="40"/>&nbsp
  </a>
</div>
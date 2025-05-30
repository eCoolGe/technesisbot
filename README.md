# TechnesisBot

_Данный бот был написан для парсинга цен с сайтов по ULR и X-Path_

<details>
<summary>Техническое задание</summary>
<br>

```text
Представьте, что у вас есть система без интерфейса пользователя, например краулер (сборщик информации), который парсит все сайты по продаже зюзюбликов и сохраняет в базу данных.
Появилась потребность дать обычному пользователю минимальными усилиями добавлять еще сайты для парсинга
Напишите простого бота, который будет иметь одну кнопку: загрузить файл
  1. При нажатии кнопки пользователь прикрепляет файл excel в формате таблицы с полями:
      a. title - название
      b. url - ссылка на сайт источник
      c. xpath - путь к элементу с ценой
  2. Бот получает файл, сохраняет
  3. Открывает файл библиотекой pandas
  4. Выводит содержимое в ответ пользователю
  5. Сохраняет содержимое в локальную БД sqlite
Реализация на python, решение должно быть представлено ссылкой на репозиторий и на бота (как основной вариант телеграм, но возможно вы предложите что-то еще).
Учесть возможность того, что сумма будет с пробелами, обозначением валюты и прочее.
Внутри репозитория должна быть инструкция по развёртыванию и корректный файл с необходимыми зависимостями (requirements, pipenv, poetry на ваш выбор)
Задание рассчитано на один день, выполнять можно в удобное время в течение недели

*Задача со звездочкой:
Провести парсинг по данным из таблицы и вывести среднюю цену зюзюблика по каждому сайту,
В качестве зюзюблика можете взять любой интересный вам товар
```

</details>




<details>
<summary>Список доступных команд</summary>
<br>

* Пользователь:
    * `/start` — _начальная команда любого бота в Telegram, выводит приветственное сообщение_
      * `Загрузить` — _кнопка для загрузки файла Excel_
    * `/help` — _команда, которая выводит список доступных команд_

* Администратор:
    * `/logs` — _отправляет в ответ текстовый документ с логами бота_
    * `/reset` — _пересоздать базу данных_
</details>


## Установка

* `python`, `exit()` _(проверялось на версии 3.11)_
* `cp .env.example .env`
* Вставить данные в созданный выше файл секретных данных <kbd>.env</kbd>
* Вставить данные конфигурации в файл <kbd>bot/config.py</kbd>

#### Установка/запуск через <kbd>pip</kbd>:
* `pip install -r requirements.txt`
* `python -m bot.main`

#### Установка/запуск через <kbd>Poetry</kbd>:
* `pip install poetry` — сначала надо установить <kbd>Poetry</kbd> через <kbd>pip</kbd> или аналогичный установщик, например, <kbd>pipx</kbd>
* `poetry install`
* `poetry run start`


## Дополнительно

<details>
<summary>Дополнительные команды консоли</summary>
<br>

* `poetry export -f requirements.txt --output requirements.txt --without-hashes` — сгенерировать новый список зависимостей для pip через poetry
* `poetry run python -m bot.main` — аналогично команде-скрипту `poetry run start`
* `poetry add $(cat requirements.txt)` — сгенерировать новый список зависимостей для poetry через pip
</details>

<details>
<summary>Пример файла <kbd>.env</kbd></summary>
<br>

```ini
# Токен бота
BOT_TOKEN=<token>
# Режим отправки сообщений в канал-чат
# При включенном режиме бот будет "дублировать" важные сообщения (запуск, критическая ошибка) в канал-чат 
LOG_MODE=False
# Идентификатор канала-чата, используйте 0, если он вам не нужен
LOG_GROUP_ID=<group_id>
# Путь к файлу логов
LOG_FILE_PATH=bot/static/logs.txt
# Путь к базе данных SQLite
DB_PATH=bot/static/sqlite.db
# Включение тестового режима
# При включенном тестовом режиме бот будет отвечать заглушкой всем, кроме администраторов, указанных в файле config.py
TESTING_MODE=False

```
</details>
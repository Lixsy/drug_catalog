# Описание
##Запуск приложения

    Для запуска приложения необходимо иметь установленный docker-compose

    Инструкция по запуску приложения в docker-compose:
    1.make build -- собирать образ docker-compose
    2.make run -- команда для запуска приложения и базы данных в докерах
    3.make import -- импорт данных из другого mock сервиса, который на момент запуска будет выдавать ошибки. Для 
    успешного импорта необходимо через Swagger создать несколько категорий и сверить id в базе с id в CATEGORY_MAP
    в файле api/drugstore.py
    После запуска приложения Swagger доступен по адресу 127.0.0.1:5000/docs

##Запуск unit tests

    Запуск юнит тестов вне docker-compose: необходимо установить библиотеки либо через poetry,
    либо через requirements.txt

    make test --  запуск unit тестов (работает после установки библиотек)

    

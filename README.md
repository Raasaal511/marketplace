# Marketplace - интернет-сервис для размещения объявлений о товарах

---
**Проект Marketplace - это API, разработанное с использованием фреймворка FastAPI.
Это приложение предоставляет платформу для размещения и поиска товаров от различных продавцов.** 

## Основной стек

---
* Python==3.11.0
* FastAPI==0.99.1
* PostgreSQL==15.3.2

## Функциональность

---

Проект Marketplace предоставляет следующую функциональность:

- Регистрация и аутентификация пользователей.
- Создание, редактирование и удаление объявлений о товарах.
- Поиск товаров по различным параметрам.

## Настройка проекта

После клонирования проекта не забудьте настроить виртуальное окружение в файле database.py
используесться переменные из вируального окужения по этому добавьте файл .env и назначьте следуйшие параметры.
То есть вам надо создать БД и поставить свои значение после равно.


<p>DB_USER=db_user</p>
<p>DB_PASSWORD=db_password</p>
<p>DB_HOST=db_host</p>
<p>DB_PORT=db_port</p>
<p>DB_NAME=db_name</p>



## Установка и развертывание

---
*В консоле перейдите в папку где будете клонировать свой проект*
Примечание*: Надеемся что вы используете виртуальное окружения и после этого выполняете установку с примера ниже

1. `git clone https://github.com/Raasaal511/marketplace.git` # Скопирует проект в директорию которой находитесь
2. `cd marketplace` # Перейдите в директорию проекта
3. `pip install -r requiremens.txt` # Скачаем зависимости проекта




## Поключения и настройка Alembic
<p><code>alembic init migration</code> # Подключения к alemibic</p>
<p>После подключения, в файле <b>./migrations/env.py</b> надо будет настроить подключение к БД.

Добавьте в начале после основных импортов: </br>
```
import sys

from marketplace_app.database import DB_URL
from marketplace_app.base import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# И в переменной target_metadata присвоить Base.metadata
<br><br> 

```
Поcле, в функции  `def run_migrations_offline():`
<br>
Мы в ней создаем переменную <code>url = DB_URL</code>. Где присваиваеться наша БД `DB_URL`
```
def run_migrations_offline() -> None:
    """..."""
    url = DB_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()
```
И мы присваиваем `url` в `context.configure(url=url, ...)`  


<p>
Так как мы используем асинхронное подключение к БД нам надо еще настроить фукнцию <code>run_async_migrations</code>.
В ней мы настроим конфиги <code>configuration = config.get_section(config.config_ini_section)</code>
и добавим туда нашу базу данных <code>configuration['sqlalchemy.url'] = DB_URL</code>.
<br>
Пример всего кода:

```
async def run_async_migrations() -> None:
    """
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    configuration = config.get_section(config.config_ini_section)
    configuration['sqlalchemy.url'] = DB_URL

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()
```

После добовления в наших кофигов БД, мы добвляем их в переменную `connectable = async_engine_from_config(configuration, ...)`
</p>

После этих настроек в файле `alimbic.ini` не надо менять `sqlalchemy.url = driver://user:pass@localhost/dbname`
Мы переназачили его в функции `def run_async_migrations` вот здесь: 
```
configuration = config.get_section(config.config_ini_section)
configuration['sqlalchemy.url'] = DB_URL
```

### После насройки alembic делаем миграции и применяем их к БД.
`alembic revision --autogenerate -m "Initial"` # Создайте миграции для базы данных с использованием Alembic и замените `"Initial"` на более подходящее название миграции. </br>

`alembic upgrade head` # Примените миграции к базе данных


## Запуск проекта

---

Дальше просто билдим проект с помощью Docker: <br>
`docker-compose up --build`

@Rasul Yusupov 2023.

P.S: Ну должно же работать
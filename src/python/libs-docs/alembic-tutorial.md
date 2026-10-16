# Tutorial alembic

alembic - это легковесный инструмент для создания и управления миграциями БД.

> Пример очень простого проекта, который настроен в соответствии с данным
> мануалом и показывает как работать с alembic можно найти
> [здесь](https://github.com/aleksey925/alembic-example).

## Содержание

- [Добавление в проект миграций БД](#добавление-в-проект-миграций-бд)
  - [Установка](#установка)
  - [Инициализация alembic в проекте](#инициализация-alembic-в-проекте)
  - [Автоматическая генерация миграций](#автоматическая-генерация-миграций)
  - [Ручное создание миграций](#ручное-создание-миграций)
  - [Добавление миграций в существующие приложение](#добавление-миграций-в-существующие-приложение)
  - [Использование alembic в тестах](#использование-alembic-в-тестах)
- [Исправление известных проблем](#исправление-известных-проблем)
  - [Команда для автоматической генерации миграции создает пустой скрипт](#команда-для-автоматической-генерации-миграции-создает-пустой-скрипт)
  - [No support for ALTER of constraints in SQLite dialec](#no-support-for-alter-of-constraints-in-sqlite-dialec)
  - [Изменение foreign key в sqlite](#изменение-foreign-key-в-sqlite)

## Добавление в проект миграций БД

Данный туториал описывает процесс настройки alembic в проекте, для управления
миграциями, а так же показывает как можно вызывать alembic из тестов для
инициализации БД.

### Установка

Устанавливаем alembic

```bash
pip install alembic>=1.13.3
```

### Инициализация alembic в проекте

Инициализируем alembic:

```bash
alembic init --template generic migrations
```

В создавшемся файле `alembic.ini` проверьте наличие следующих настроек в секции
`[alembic]` и если их нет или они закомментированы добавьте/раскомментируйте
их.

- `file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s` -
  шаблон имени файла с миграцией, который создает alembic. Довольно важный
  параметр, который помогает легче ориентироваться в созданных миграциях.

- `prepend_sys_path = .` - очень важная настройка. Она нужна, чтобы вы могли
  импортировать метаданные или какие-то любые другие части вашего проекта в
  скрипте`env.py` без проблем. Иначе вам придется редактировать `sys.path`
  вручную внутри `env.py`.

Теперь, после базовой настройки, необходимо немного подправить сгенерированный
скрипт `env.py`. Это нужно, чтобы объяснить alembic к какой базе данных он
должен подключаться, где он может найти метаданные sqlalchemy, а так же
включить поддержку автогенерации миграций.

Для этого открываем скрипт `migrations/env.py` и:

- импортируем базовый класс всех моделей sqlalchemy, берем из него metadata и
  кладем в переменную `target_metadata`

  ```python
  from main import Base
  ...
  target_metadata = Base.metadata
  ...
  ```

- где-то после объявления `target_metadata` вставляем следующий код, которые
  будет говорить alembic с какой БД он должен работать

  ```python
  pg_dns = build_pg_dsn(
      user=os.environ['PG_USER'],
      password=os.environ['PG_PASSWORD'],
      host=os.environ['PG_HOST'],
      dbname=os.environ['PG_DB'],
  )
  config.set_main_option('sqlalchemy.url', pg_dns)
  ```

  В данном случае, мы собираем строку подключения к БД из переменных окружения.
  Вы можете брать ее откуда угодно, на пример из конфигурационного файла
  проекта.

- находим строку `fileConfig(config.config_file_name)` и заменяем ее на
  `fileConfig(config.config_file_name, disable_existing_loggers=False)`. Если
  это не сделать alembic отключит все существующие логгеры. В случае если
  alembic вызывается исключительно как консольная команда, то это не страшно,
  но если работа с миграциями будет осуществляться из кода приложения, то
  дефотное поведение alembic может доставить много хлопот.

### Автоматическая генерация миграций

После настройки можно сгенерировать нашу первую миграцию, которая зафиксирует
начальное состояние базы. Скрипт с миграцией будет создан в папке
migrations/versions.

```bash
alembic revision --autogenerate -m "init"
```

Когда создание миграции закончено, можно применить ее к БД

```bash
alembic upgrade head
```

#### Ограничения автоматической генерации миграций

Автогенерация просто замечательна, но у нее есть некоторые ограничения, о
которых нужно знать. Прежде всего, если вы переименуете таблицу или столбец, то
alembic будет считать это удалением и созданием нового столбца/таблицы. Это
приведет к потере данных. По этому вы должны вручную произвести редактирование
автоматически сгенерированной миграции в которой был переименован
столбец/таблица.

### Ручное создание миграций

Иногда бывает нужно создать миграцию вручную. Для этого необходимо выполнить в
консоли команду

```bash
alembic revision -m "add_field_create_date"
```

После ее выполнения, в папке `migrations/versions`, будет создан скрипт
`2019_06_09_2107-7c86752c4a38_add_field_create_date.py` с пустыми функциями
upgrade и downgrade, в которых нужно будет описать то, что необходимо сделать с
БД.

В результате должен получиться примерно такой код:

```python
"""add_field_create_date

Revision ID: 7c86752c4a38
Revises: 2e8e603859e2
Create Date: 2019-06-09 21:07:17.573918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c86752c4a38'
down_revision = '2e8e603859e2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('student', sa.Column('create_date', sa.Date(), nullable=True))


def downgrade():
    with op.batch_alter_table('student') as batch_op:
        batch_op.drop_column('create_date')

```

Теперь, можно применить данную миграцию при помощи команды:

```bash
alembic upgrade head
```

Если необходимо будет откатить сделанные изменения, то это можно будет сделать
1 из ниже перечисленных команд:

```bash
# 2e8e603859e2 - это номер ревизии к которой мы должны откатиться
alembic downgrade 2e8e603859e2
```

```bash
alembic downgrade -1
```

### Добавление миграций в существующие приложение

При добавлении миграций в существующие приложение, где в БД уже созданы все
необходимые таблицы в ручную или просто sql скриптами необходимо выполнить
команду:

```
alembic stamp head
```

После этого alembic будет считать, что все миграции применены и не будет
пытаться запустить.

Ссылки на дополнительные материалы:

- [alembic – Python migrations quick start](https://michaelheap.com/alembic-python-migrations-quick-start/)
- [Schema migrations with Alembic, Python and PostgreSQL](https://www.compose.com/articles/schema-migrations-with-alembic-python-and-postgresql/)

### Использование alembic в тестах

Ниже приведен пример фикстур, которые нужно положить в `conftest.py` и после
этого вы можете писать тесты, которые будут взаимодействовать с БД через
подключение выдаваемое в фикстурой pg_conn.

```python
import asyncio
import os
from pathlib import Path
from typing import AsyncGenerator, Generator

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncConnection, create_async_engine
from sqlalchemy_utils import drop_database, create_database, database_exists

from main import build_pg_dsn

os.environ['PG_DB'] = f"{os.environ['PG_DB']}_test"
PG_DSN = build_pg_dsn(
    user=os.environ['PG_USER'],
    password=os.environ['PG_PASSWORD'],
    host=os.environ['PG_HOST'],
    dbname=os.environ['PG_DB'],
)
ROOT_DIR = Path(__file__).parent.parent


@pytest.fixture(scope='session')
def project_root() -> Path:
    return ROOT_DIR


@pytest.fixture(scope='session')
def setup_pg(project_root: Path) -> Generator[None, None, None]:
    if database_exists(PG_DSN):
        drop_database(PG_DSN)
    create_database(PG_DSN)

    curr_work_dir = os.getcwd()
    os.chdir(project_root)
    alembic_cfg = Config(str(ROOT_DIR / 'alembic.ini'))
    command.upgrade(alembic_cfg, 'head')
    os.chdir(curr_work_dir)

    yield

    drop_database(PG_DSN)


@pytest.fixture(scope='session')
def pg_engine() -> Generator[AsyncEngine, None, None]:
    engine = create_async_engine(PG_DSN)
    yield engine
    asyncio.run(engine.dispose())


@pytest.fixture
async def pg_conn(setup_pg: None, pg_engine: AsyncEngine) -> AsyncGenerator[AsyncConnection, None]:
    async with pg_engine.begin() as conn:
        yield conn
        await conn.rollback()
```

## Исправление известных проблем

### Команда для автоматической генерации миграции создает пустой скрипт

Если вы столкнулись с тем, что автоматическая генерация миграций не
срабатывает, значит вам необходимо проверить, что при импорте базового класса
(`Base`) происходит импорт всех моделей приложения.

> Это очень важно, так как базовый класс моделей внутри себя пользуется
> возможностями метапрограммирования по этому, если во время исполнения скрипта
> env.py модели не будут импортированы, то sqlalchemy ничего не будет о них
> знать и следовательно не сможет сгенерировать миграцию.

Если вы поняли, что столкнулись именно с такой ситуацией, то один из путей
решения проблемы, это:

- вынести все модули с моделями в отдельный пакет
- реализовать в `__init__.py` импортирование всех модулей пакета
- в env.py импортировать класс Base из этого пакета

### No support for ALTER of constraints in SQLite dialec

При использовании sqlite может возникать ошибка
`No support for ALTER of constraints in SQLite dialect` (в моем случае данная
ошибка возникала, когда один из столбцов был помечен как уникальный
`unique=True`).

Для того, чтобы исправить данную ошибку, нужно внести исправления в функции
`run_migrations_offline` и `run_migrations_online`, которые находятся в скрипте
env.

В этих функциях необходимо найти вызов context.configure и добавить в него
параметр `render_as_batch=True`. После этого будут генерироваться корректные
миграции.

Полезные ссылки:

- [Sqlite lack of ALTER support, Alembic migration failing because of this. Solutions?](https://stackoverflow.com/questions/30378233/sqlite-lack-of-alter-support-alembic-migration-failing-because-of-this-solutio)
- [batch_alter_table - alembic](https://kite.com/python/docs/alembic.op.batch_alter_table)

### Изменение foreign key в sqlite

Пример миграции, которая изменяет значение ondelete у внешнего ключа

```python
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm


NEW_SERIES_TABLE_ARGS = (
    'series',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_serial', sa.Integer(), nullable=True),
    sa.Column('series_number', sa.Integer(), nullable=True),
    sa.Column('season_number', sa.Integer(), nullable=True),
    sa.Column('looked', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id_serial'], ['serial.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
)

OLD_SERIES_TABLE_ARGS = (
    'series',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_serial', sa.Integer(), nullable=True),
    sa.Column('series_number', sa.Integer(), nullable=True),
    sa.Column('season_number', sa.Integer(), nullable=True),
    sa.Column('looked', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id_serial'], ['serial.id'], ),
    sa.PrimaryKeyConstraint('id')
)


def move_data(table_args):
    temp_serial_table_name = 'series_temp'
    column_series_tabel = [
        'id', 'id_serial', 'series_number', 'season_number', 'looked'
    ]
    sql_get_all_series = (
        f'select {", ".join(column_series_tabel)} '
        f'from {temp_serial_table_name}'
    )

    # В sqlite нельзя изменить foreign key, по этому приходится создавать новую
    # таблицу и переносить в нее данные из старой
    op.rename_table('series', temp_serial_table_name)

    new_series_table = op.create_table(*table_args)

    bind = op.get_bind()
    session = orm.Session(bind=bind)

    all_series = list(map(
        lambda row: dict(zip(column_series_tabel, row)),
        session.execute(sql_get_all_series)
    ))
    op.bulk_insert(new_series_table, all_series)
    session.commit()

    op.drop_table(temp_serial_table_name)


def upgrade():
    move_data(NEW_SERIES_TABLE_ARGS)


def downgrade():
    move_data(OLD_SERIES_TABLE_ARGS)
```

Полезные ссылки:

- [SQLite: Foreign Keys with Cascade Delete](https://www.techonthenet.com/sqlite/foreign_keys/foreign_delete.php)

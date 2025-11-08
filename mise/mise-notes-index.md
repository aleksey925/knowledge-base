mise
====

# Оглавление

- [Порядок загрузки mise.toml при активации окружения](#порядок-загрузки-misetoml-при-активации-окружения)


<a name='порядок-загрузки-misetoml-при-активации-окружения'></a>
# Порядок загрузки mise.toml при активации окружения

> Ресерч делался на основе версии 2025.11.3

> Что происходит, когда вы переходите в директорию с mise.toml и mise автоматически настраивает ваше окружение

## Введение

Когда у вас настроена интеграция mise с shell:

```bash
# В .bashrc/ или .zshrc:
eval "$(mise activate bash)"
```

И вы переходите в директорию с проектом:

```bash
cd /home/user/myproject
```

mise автоматически загружает конфигурацию из `mise.toml` и настраивает окружение. Важно понимать 
**в каком порядке** это происходит, чтобы правильно выстраивать зависимости между секциями.

---

## Секции mise.toml

Основные секции конфигурационного файла:

```toml
[vars]          # Переменные для использования в templates
[env]           # Переменные окружения
[[env]]         # Дополнительные блоки env (порядок важен!)
[tools]         # Инструменты для установки
[alias]         # Алиасы для инструментов (опционально)
[plugins]       # Внешние плагины (опционально)
```

---

## Шпаргалка

```
┌───────────────────────────────────────────────────────────────┐
│              Порядок загрузки при cd в папку                  │
├───────────────────────────────────────────────────────────────┤
│ 1. [vars]            - переменные для шаблонов                │
│ 2. [alias]/[plugins] - опционально                            │
│ 3. [env] БЕЗ tools   - базовые переменные окружения           │
│ 4. [tools]           - установка/проверка инструментов        │
│ 5. [env] С tools     - переменные после установки tools       │
│ 6. Применение        - export в shell                         │
└───────────────────────────────────────────────────────────────┘

Ключевые правила:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• [[env]] блоки выполняются В ПОРЯДКЕ НАПИСАНИЯ
• Но с учетом двух проходов: без tools → с tools
• vars НЕ может использовать env или tools
• env может использовать vars ВСЕГДА
• env может использовать tools ТОЛЬКО с tools=true
• _.python.venv ВСЕГДА имеет tools=true (нельзя изменить)
• Порядок _. директив внутри [env] жестко закодирован:
  _.path → _.file → _.source → другие → _.python.venv
```

---

## Полный процесс активации

Когда вы делаете `cd` в директорию с `mise.toml`, происходит следующее:

```
cd /project
    ↓
mise hook-env запускается
    ↓
┌─────────────────────────────────────┐
│ 1. Загрузка конфигурации            │
│    - Парсинг mise.toml              │
│    - Применение [settings]          │
│    - Валидация структуры            │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. Обработка [vars]                 │
│    - Загружаются ВСЕ переменные     │
│    - Становятся доступны в шаблонах │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. Обработка [alias] и [plugins]    │
│    - Регистрация алиасов            │
│    - Подключение внешних плагинов   │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. Обработка [env] - Проход 1       │
│    - Только директивы БЕЗ tools     │
│    - _.file, _.source (без tools)   │
│    - Обычные переменные             │
│    - В порядке [[env]] блоков       │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 5. Обработка [tools]                │
│    - Проверка установленных версий  │
│    - Автоустановка (если включена)  │
│    - Добавление в PATH              │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 6. Обработка [env] - Проход 2       │
│    - Только директивы С tools=true  │
│    - _.python.venv                  │
│    - _.source с tools=true          │
│    - В порядке [[env]] блоков       │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 7. Применение к shell               │
│    - export переменных окружения    │
│    - Модификация PATH               │
│    - Активация venv (если создан)   │
└─────────────────────────────────────┘
    ↓
Ваш shell готов! 🎉
```

---

## Детальное описание каждого шага

### Шаг 1: Загрузка конфигурации

**Что происходит:**

- mise находит `mise.toml` в текущей директории
- Парсит TOML файл
- Применяет настройки из `[settings]` (если есть)
- Проверяет синтаксис

### Шаг 2: Обработка [vars]

> `[vars]` - это значения, которые доступны в tasks, похожи на переменные окружения, но они не передаются в 
> виде переменных окружения в скрипты. Они определяются в секции `vars` файла mise.toml.

**Что происходит:**

- Все переменные из `[vars]` вычисляются и сохраняются
- Становятся доступны для использования в других секциях через `{{vars.NAME}}`

**Зачем это первым:**

- Другие секции могут использовать vars в шаблонах
- vars **НЕ могут** использовать env или tools

**Пример:**

```toml
[vars]
PROJECT_ROOT = "{{config_root}}"
DATA_DIR = "{{vars.PROJECT_ROOT}}/data"
LIB_DIR = "{{vars.PROJECT_ROOT}}/lib"
```

**Что доступно в шаблонах vars:**

- `{{config_root}}` - путь к директории с mise.toml
- `{{cwd}}` - текущая рабочая директория
- `{{vars.NAME}}` - другие переменные из [vars]

### Шаг 3: Обработка [alias] и [plugins]

**Что происходит:**

- Регистрируются алиасы для инструментов
- Подключаются внешние плагины (asdf/vfox)

**Пример:**

```toml
[alias.node]
lts = "24"

[plugins]
my-tool = "https://github.com/user/asdf-my-tool"
```

**Для большинства пользователей:**

- Можно пропустить эту секцию
- Нужна только для продвинутых сценариев

### Шаг 4: Обработка [env] - Первый проход

**Что происходит:**

- Обрабатываются только директивы **БЕЗ `tools = true`**. 
- Блоки `[[env]]` обрабатываются **в порядке их написания**
- Внутри одного блока `[env]` порядок `_.*` директив жестко закодирован

**Что загружается:**

```toml
[[env]]
_.file = ".env"           # ✅ Загружается
VAR1 = "value"            # ✅ Загружается

[[env]]
_.source = "script.sh"    # ✅ Загружается (если БЕЗ tools=true)
VAR2 = "other"            # ✅ Загружается
```

**Что НЕ загружается (откладывается до второго прохода):**

```toml
[[env]]
_.python.venv = { path = ".venv", create = true }  # ⏭️ Пропускается (всегда tools=true)
_.source = { path = "script.sh", tools = true }    # ⏭️ Пропускается
VAR3 = { value = "val", tools = true }             # ⏭️ Пропускается
```

**Что доступно в шаблонах:**

- `{{vars.NAME}}` - все переменные из [vars]
- `{{env.NAME}}` - уже загруженные переменные из предыдущих [[env]] блоков
- `{{config_root}}`, `{{cwd}}`

**Порядок директив внутри одного [env] блока:**

Если вы пишете:
```toml
[env]
_.python.venv = { path = ".venv", create = true }
_.source = "script.sh"
_.file = ".env"
MY_VAR = "value"
```

**Реальный порядок выполнения** (жестко закодирован):

1. `_.file = ".env"`
2. `_.source = "script.sh"`
3. `MY_VAR = "value"`
4. `_.python.venv` (но на втором проходе!)

**Решение:** используйте отдельные `[[env]]` блоки для контроля порядка:

```toml
[[env]]
_.file = ".env"

[[env]]
_.source = "script.sh"

[[env]]
MY_VAR = "value"

[[env]]
_.python.venv = { path = ".venv", create = true }
```

### Шаг 5: Обработка [tools]

**Что происходит:**

- mise проверяет какие инструменты требуются
- Проверяет установлены ли они
- Если `settings.auto_install = true` и инструмент не установлен - автоматически устанавливает
- Добавляет пути к инструментам в PATH
- Устанавливает переменные окружения инструментов (например, `GEM_HOME` для ruby)

**Пример:**

```toml
[tools]
python = "3.12.3"
node = "24.4.1"
uv = "0.9.7"
```

**Результат после этого шага:**

- В PATH добавлены: `~/.local/share/mise/installs/python/3.12.3/bin`, `~/.local/share/mise/installs/node/24.4.1/bin` и т.д.
- Переменные инструментов доступны (например, `GEM_HOME`, `GOPATH`)

**Об автоустановке:**

По умолчанию `auto_install = false`, инструменты нужно установить вручную через `mise install`. С `auto_install = true` они установятся автоматически при активации.

### Шаг 6: Обработка [env] - Второй проход

**Что происходит:**

- Обрабатываются только директивы **С `tools = true`**
- Блоки `[[env]]` снова обрабатываются **в порядке их написания**
- Но теперь пропускаются все директивы БЕЗ `tools`

**Что загружается:**

```toml
[[env]]
_.python.venv = { path = ".venv", create = true }  # ✅ Сейчас загружается

[[env]]
_.source = { path = "after-tools.sh", tools = true }  # ✅ Сейчас загружается

[[env]]
CUSTOM_VAR = { value = "{{env.VIRTUAL_ENV}}/data", tools = true }  # ✅ Сейчас загружается
```

**Что доступно в шаблонах:**

- Всё из первого прохода (vars, env)
- Установленные tools в PATH
- Переменные, созданные tools (например, `GEM_HOME`, `GOPATH`)
- `VIRTUAL_ENV` (если venv был создан на этом проходе ранее)

**Важно про порядок:**

Если несколько `[[env]]` блоков имеют `tools=true`, они выполняются в порядке написания:

```toml
[[env]]
_.python.venv = { path = ".venv", create = true }  # Выполнится первым

[[env]]
# Этот блок выполнится ПОСЛЕ создания venv
VENV_DATA = { value = "{{env.VIRTUAL_ENV}}/data", tools = true }  # ✅ VIRTUAL_ENV доступна
```

### Шаг 7: Применение к shell

**Что происходит:**

- Все переменные окружения экспортируются в ваш shell (`export VAR=value`)
- PATH модифицируется (добавляются пути к tools и venv)
- Если был создан venv - он активируется (промпт меняется)

**Результат в shell:**

```bash
$ echo $VIRTUAL_ENV
/home/user/project/.venv

$ which python
/home/user/project/.venv/bin/python

$ echo $PATH
/home/user/project/.venv/bin:/home/user/.local/share/mise/installs/node/24.4.1/bin:...

$ echo $MY_CUSTOM_VAR
value_from_mise_toml
```

---

## Порядок обработки [[env]] блоков

### Ключевое правило

Блоки `[[env]]` обрабатываются **в порядке их написания в файле**, НО с учетом двух проходов (без/с tools).

### Пример с пояснением

```toml
# Блок 1
[[env]]
_.file = ".env"

# Блок 2
[[env]]
BASE_VAR = "value"

# Блок 3
[[env]]
_.python.venv = { path = ".venv", create = true }

# Блок 4
[[env]]
_.source = { path = "final.sh", tools = true }

# Блок 5
[[env]]
FINAL_VAR = "{{env.VIRTUAL_ENV}}/data"

[tools]
python = "3.12.3"
```

**Реальный порядок выполнения:**

```
Проход 1 (БЕЗ tools):
  1. Блок 1: _.file = ".env"
  2. Блок 2: BASE_VAR = "value"
  3. Блок 3: пропускается (_.python.venv всегда имеет tools=true)
  4. Блок 4: пропускается (tools=true)
  5. Блок 5: FINAL_VAR = ".../data" ← ❌ VIRTUAL_ENV ещё не создан! Будет пустая строка или ошибка!

[Установка tools: python 3.12.3]

Проход 2 (С tools):
  6. Блок 1: пропускается (уже выполнен)
  7. Блок 2: пропускается (уже выполнен)
  8. Блок 3: _.python.venv - создается venv, устанавливается VIRTUAL_ENV
  9. Блок 4: _.source = "final.sh" - скрипт теперь имеет доступ к venv
  10. Блок 5: пропускается (уже выполнен, но VIRTUAL_ENV не было!)
```

### Правильная версия

Чтобы `FINAL_VAR` имел доступ к `VIRTUAL_ENV`, нужно добавить `tools = true`:

```toml
[[env]]
_.file = ".env"

[[env]]
BASE_VAR = "value"

[[env]]
_.python.venv = { path = ".venv", create = true }

[[env]]
_.source = { path = "final.sh", tools = true }

[[env]]
FINAL_VAR = { value = "{{env.VIRTUAL_ENV}}/data", tools = true }  # ✅ Теперь правильно!

[tools]
python = "3.12.3"
```

**Теперь порядок:**

```
Проход 1:
  1. _.file = ".env"
  2. BASE_VAR = "value"

[Установка tools]

Проход 2:
  3. _.python.venv - создается venv
  4. _.source = "final.sh"
  5. FINAL_VAR = "/path/to/.venv/data" ✅
```

---

## Доступность данных в templates

Что может использовать что в шаблонах:

| Секция           | vars | env (pass 1) | tools | env (pass 2) |
|------------------|------|--------------|-------|--------------|
| `[vars]`         | ✅   | ❌           | ❌    | ❌           |
| `[env]` pass 1   | ✅   | ✅           | ❌    | ❌           |
| `[env]` pass 2   | ✅   | ✅           | ✅    | ✅           |

**Расшифровка:**

- ✅ - можно использовать
- ❌ - нельзя использовать

**Примеры:**

```toml
[vars]
MY_VAR = "{{vars.OTHER_VAR}}"        # ✅ vars может использовать другие vars
MY_VAR = "{{env.SOME_VAR}}"          # ❌ vars НЕ может использовать env

[env]
VAR1 = "{{vars.MY_VAR}}"             # ✅ env pass 1 может использовать vars
VAR2 = "{{env.VAR1}}"                # ✅ env pass 1 может использовать другие env
VAR3 = "{{env.GEM_HOME}}"            # ❌ env НЕ может использовать переменную с опцией tools

[env]
VAR4 = { value = "{{env.GEM_HOME}}", tools = true }  # ✅ env pass 2 может использовать tools
```

---

## Практические примеры

### Пример 1: Типичная настройка Python проекта

```toml
[vars]
PROJECT_ROOT = "{{config_root}}"
VENV_DIR = ".venv"

# Загружаем базовые переменные из .env
[[env]]
_.file = ".env"

# Создаем виртуальное окружение (после установки Python)
[[env]]
_.python.venv = { path = "{{vars.VENV_DIR}}", create = true }

# Устанавливаем инструменты
[tools]
python = "3.12.3"
uv = "0.9.7"
```

**Что происходит при `cd` в папку:**

1. Загружаются vars: `PROJECT_ROOT`, `VENV_DIR`
2. Загружается `.env` файл
3. Устанавливаются Python 3.12.3 и uv (если `auto_install = true`)
4. Создается venv в `.venv`
5. Venv активируется, PATH модифицируется

### Пример 2: Использование переменных из venv

```toml
[vars]
DATA_DIR = "data"

# Базовые переменные
[[env]]
_.file = ".env"

# Создание venv
[[env]]
_.python.venv = { path = ".venv", create = true }

# Переменная, использующая VIRTUAL_ENV (ДОЛЖНА быть с tools=true!)
[[env]]
CUSTOM_DATA_PATH = { value = "{{env.VIRTUAL_ENV}}/{{vars.DATA_DIR}}", tools = true }
PYTHONPATH = { value = "{{env.VIRTUAL_ENV}}/src", tools = true }

[tools]
python = "3.12.3"
```

**Результат:**

- `CUSTOM_DATA_PATH = "/path/to/.venv/data"`
- `PYTHONPATH = "/path/to/.venv/src"`

### Пример 3: Скрипт инициализации после создания venv

```toml
# Базовые переменные
[[env]]
_.file = ".env"

# Создание venv
[[env]]
_.python.venv = { path = ".venv", create = true }

# Скрипт выполнится ПОСЛЕ создания venv и установки tools
[[env]]
_.source = { path = "./scripts/setup-dev-env.sh", tools = true }

[tools]
python = "3.12.3"
node = "24.4.1"
```

**scripts/setup-dev-env.sh** имеет доступ к:

- Python 3.12.3 из mise
- Node 24.4.1 из mise
- Активированному venv (python из venv в PATH)
- Всем переменным из `.env`
- `VIRTUAL_ENV` переменной
- Командам из venv (`pip`, и т.д.)

**Пример скрипта:**
```bash
#!/bin/bash
# scripts/setup-dev-env.sh

# Доступен python из venv
export PYTHON_VERSION=$(python --version)

# Можно использовать pip из venv
export PIP_PACKAGES=$(pip list --format=freeze | wc -l)

# Можно использовать переменные из .env
export LOG_DIR="${PROJECT_DIR}/logs"

echo "Setup complete! Python: $PYTHON_VERSION, Packages: $PIP_PACKAGES"
```

### Пример 4: Композиция нескольких источников

```toml
[vars]
PROJECT_ROOT = "{{config_root}}"
CONFIG_DIR = "{{vars.PROJECT_ROOT}}/config"

# Блок 1: загрузка базовых переменных
[[env]]
_.file = [".env.base", ".env.local"]

# Блок 2: дополнительные пути в PATH
[[env]]
_.path = ["{{vars.PROJECT_ROOT}}/bin", "{{vars.PROJECT_ROOT}}/scripts"]

# Блок 3: базовые переменные
[[env]]
PROJECT_NAME = "my-app"
ENV = "development"

# Блок 4: создание venv (после установки Python)
[[env]]
_.python.venv = { path = "{{vars.PROJECT_ROOT}}/.venv", create = true }

# Блок 5: переменные, зависящие от venv
[[env]]
APP_VENV_PATH = { value = "{{env.VIRTUAL_ENV}}", tools = true }
APP_PYTHON = { value = "{{env.VIRTUAL_ENV}}/bin/python", tools = true }

# Блок 6: финальный скрипт инициализации
[[env]]
_.source = { path = "{{vars.CONFIG_DIR}}/init-env.sh", tools = true }

[tools]
python = "3.12.3"
node = "24.4.1"
uv = "0.9.7"
```

**Порядок выполнения:**

Проход 1 (БЕЗ tools):

- Блок 1: загрузка `.env.base`, `.env.local`
- Блок 2: добавление путей в PATH
- Блок 3: `PROJECT_NAME`, `ENV`

Установка tools:

- Python 3.12.3, Node 24.4.1, uv 0.9.7

Проход 2 (С tools):

- Блок 4: создание venv
- Блок 5: `APP_VENV_PATH`, `APP_PYTHON`
- Блок 6: выполнение `init-env.sh`

---

## Частые ошибки

### ❌ Ошибка 1: Использование VIRTUAL_ENV без tools=true

```toml
[[env]]
_.python.venv = { path = ".venv", create = true }

[[env]]
MY_PATH = "{{env.VIRTUAL_ENV}}/data"  # ❌ VIRTUAL_ENV еще нет!
```

**Проблема:**

Блок 2 выполнится на **первом проходе** (до создания venv), а venv создается на **втором проходе**.

**Исправление:**

```toml
[[env]]
_.python.venv = { path = ".venv", create = true }

[[env]]
MY_PATH = { value = "{{env.VIRTUAL_ENV}}/data", tools = true }  # ✅
```

---

### ❌ Ошибка 2: Использование env в vars

```toml
[env]
MY_VAR = "value"

[vars]
OTHER_VAR = "{{env.MY_VAR}}"  # ❌ env не доступны в vars!
```

**Проблема:**

`[vars]` загружаются **до** `[env]`, поэтому env переменные недоступны.

**Исправление:**
```toml
[vars]
MY_VAR = "value"
OTHER_VAR = "{{vars.MY_VAR}}"  # ✅
```

Если вам нужна переменная окружения в другой переменной окружения:
```toml
[env]
MY_VAR = "value"
OTHER_VAR = "{{env.MY_VAR}}"  # ✅ env может использовать другие env
```

---

### ❌ Ошибка 3: Ожидание порядка _.* директив внутри [env]

```toml
[env]
_.python.venv = { path = ".venv", create = true }
_.source = "script.sh"
_.file = ".env"
```

**Проблема:**

Порядок директив `_.*` внутри одного `[env]` блока **жестко закодирован** и не зависит от порядка написания.

**Реальный порядок выполнения:**

1. `_.file = ".env"`
2. `_.source = "script.sh"`
3. `_.python.venv = ...`

**Исправление:**

Используйте отдельные `[[env]]` блоки:
```toml
[[env]]
_.file = ".env"

[[env]]
_.source = "script.sh"

[[env]]
_.python.venv = { path = ".venv", create = true }
```

---

### ❌ Ошибка 4: Скрипт выполняется до установки tools

```toml
[[env]]
_.source = "setup.sh"  # Скрипту нужен Python, но его еще нет!

[tools]
python = "3.12.3"
```

**Проблема:**
Скрипт без `tools=true` выполняется **до** установки инструментов.

**Исправление:**
```toml
[[env]]
_.source = { path = "setup.sh", tools = true }  # ✅ Выполнится после установки Python

[tools]
python = "3.12.3"
```

---

## Диаграмма взаимосвязей секций

```
     [settings]
         ↓
      [vars]
         ↓
    ┌────┴────┐
    ↓         ↓
[env pass 1] [alias]
    ↓        [plugins]
    ↓
  [tools]
    ↓
[env pass 2]
    ↓
export в shell
```

**Стрелки показывают:**

- Порядок выполнения (сверху вниз)
- Какие секции могут использовать результаты других

**Доступность данных в шаблонах:**

```
[vars]           → доступны: vars, config_root, cwd
[env] pass 1     → доступны: vars, env (pass 1), config_root, cwd
[env] pass 2     → доступны: vars, env (pass 1 + 2), tools, config_root, cwd
```

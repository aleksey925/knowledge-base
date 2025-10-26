Claude
=======

# Оглавление

- [Установка claude code](#установка-claude-code)
- [Настройка JetBrains IDE](#настройка-jetbrains-ide)
- [Model Context Protocol (MCP)](#model-context-protocol-mcp)


<a name='установка-claude-code'></a>
# Установка claude code

Официальная документация на данный момент не описывает, как установить версию claude code написанную на nodejs 
правильно. Этот скрипт закрывает эту проблему, он установит claude code сразу правильно, чтобы потом не нужно было 
запускать `claude migrate-installer` и кроме того он использует `mise` для установки `node`, что позволяет не 
засорять окружение.

```bash
#!/bin/bash
# Script for installing Claude code the right way, as it would be done by
# the Claude command "migrate-installer".
set -e

CLAUDE_PATH="$HOME/.claude/local/"
NODE_LATEST="$(mise latest node)"

echo "Installing Node.js $NODE_LATEST for running Claude code..."
mise install node@"$NODE_LATEST"

if [ -d "$HOME/.claude/local/" ]; then
  echo "Removing existing Claude code installation at: $CLAUDE_PATH"
  rm -rf "$CLAUDE_PATH"
fi
mkdir -p "$CLAUDE_PATH"
mise exec node@"$NODE_LATEST" -- npm install --prefix "$CLAUDE_PATH" @anthropic-ai/claude-code

cat > "$CLAUDE_PATH"/claude << EOF
#!/bin/bash
mise exec node@$NODE_LATEST -- "$CLAUDE_PATH"/node_modules/.bin/claude "\$@"
EOF

chmod +x "$CLAUDE_PATH"/claude
echo "Claude installed successfully at: $CLAUDE_PATH"
```

<a name='настройка-jetbrains-ide'></a>
# Настройка JetBrains IDE

Чтобы удобно было использовать Claude Code из консоли JetBrains IDE, нужно сделать следующее:

- В `Tools -> Terminal` включить следующие опции

    - Use Option as Meta key

    - Override IDE shortcuts

    > Если версия Pycharm 2025.2 или новее, то `Terminal Engine` выбрать `Classic` и после этого перезагрузить IDE. 
    > Это необходимо, так как начиная с этой версии, что-то сломали и `esc` продолжает переносить фокус в редактор, 
    > даже если этот хоткей отключен.

- В `Keymap` найти и удалить хоткей `Switch focus to Editor`. Он находится в группе `Plugins -> Terminal`.

Полезные ссылки:

- https://docs.claude.com/en/docs/claude-code/jetbrains#esc-key-configuration
- https://youtrack.jetbrains.com/issue/IJPL-203824/ESC-key-focus-behavior-ignores-Terminal-settings-after-PyCharm-2025.2.0.1-update


<a name='model-context-protocol-mcp'></a>
# Model Context Protocol (MCP)

**Model Context Protocol (MCP)** — это открытый стандартный протокол от Anthropic для подключения AI приложений к внешним инструментам, данным и сервисам.

**Типы MCP серверов**

**🏠 Локальные MCP серверы**

**Где запускаются:** На вашей локальной машине  
**Транспорт:** stdio (стандартный ввод/вывод)  
**Данные:** Остаются на вашем компьютере  

**Примеры:**

- **filesystem** - доступ к файлам и папкам
- **sqlite** - работа с локальными базами данных
- **puppeteer** - автоматизация браузера
- **git** - управление git репозиториями


**☁️ Удаленные MCP серверы**

**Где запускаются:** На облачных серверах (у партнеров или ваши собственные)  
**Транспорт:** HTTP/SSE (Server-Sent Events)  
**Данные:** Передаются через интернет  
**Безопасность:** OAuth, HTTPS, контроль разрешений

**Примеры:**

- **Notion** - работа с документами и базами Notion
- **Slack** - отправка сообщений, чтение каналов
- **GitHub** - создание PR, issues, работа с кодом
- **Zapier** - доступ к 5000+ интеграций
- **Canva** - создание дизайнов
- **Figma** - работа с макетами

**Когда использовать:**

- Интеграция с SaaS сервисами
- Командная работа
- Доступ с разных устройств
- Синхронизация данных


## Подключение MCP в Claude Desktop

### Способ 1: Через Connectors

- выбрать нужный connector `Settings → Connectors → Browse connectors`

  > В каталоге доступны:
  > 
  > - **Web** (Notion, Linear, Slack, Zapier и др.)
  > - **Desktop Extensions** (локальные MCP)

- установить

- использовать в чате
    - чате нажать **"Search and tools"** (нижний левый угол)
    - включить нужные connectors
    - claude автоматически использует их при необходимости

Или же можно добавить кастомный connector `Settings → Connectors → Add custom connector`


### Способ 2: Через конфигурационный файл (для локальных MCP серверов (старый способ))

- открыть конфигурационный файл `Settings → Developer → Edit Config`

- добавить MCP сервер, на пример [Browser MCP](https://browsermcp.io/)

    ```json
    {
      "mcpServers": {
        "browsermcp": {
          "command": "mise",
          "args": ["exec", "--", "npx", "@browsermcp/mcp@latest"]
        }
      }
    }
    ```

- перезапустить Claude Desktop

  > Изменения в `claude_desktop_config.json` требуют полного перезапуска приложения.


## Подключение MCP в Claude Code

### Способ 1: Через CLI команды

```bash
claude mcp add filesystem

# Filesystem с конкретной папкой
claude mcp add filesystem --args "/path/to/folder"

# С переменными окружения
claude mcp add github --env GITHUB_TOKEN=your_token
```

**Управление MCP**

- `claude mcp list` - список всех MCP серверов
- `claude mcp remove server-name` - удалить MCP сервер


### Способ 2: Через Plugins

MCP серверы могут быть упакованы в плагины.

```bash
# Добавляем marketplace
/plugin marketplace add anthropics/claude-code

# Устанавливаем нужный MCP
/plugin install <name-of-plugin>
```

> Плагин автоматически настроит MCP сервер
> Не требуется дополнительная конфигурация

Marketplaces:

- [https://github.com/anthropics/claude-code/blob/main/plugins/README.md](https://github.com/anthropics/claude-code/blob/main/plugins/README.md)

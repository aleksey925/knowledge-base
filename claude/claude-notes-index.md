Claude
=======

# Оглавление

- [Установка](#установка)
- [Настройка JetBrains IDE](#настройка-jetbrains-ide)


# Установка

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

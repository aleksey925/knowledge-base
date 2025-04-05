Заметки о работе с MacOS
=============================

# Оглавление

1. <h3>[Настройка системы](#Настройка-системы)</h3>
    
    - [Горячие клавиши](#Горячие-клавиши)
    - [Принудительная очистка ОЗУ](#Принудительная-очистка-ОЗУ)
    - [Отключение Dashboard](#Отключение-Dashboard)
    - [Отключение автоматического изменения порядка рабочих столов](#Отключение-автоматического-изменения-порядка-рабочих-столов)
    - [Отображение в finder папок перед файлами](#Отображение-в-finder-папок-перед-файлами)
    - [Предпросмотр содержимого архива в finder](#Предпросмотр-содержимого-архива-в-finder)
    - [Изменение значения TTL](#Изменение-значения-TTL)
    - [Создание MacOS приложения из простого скрипта](#Создание-MacOS-приложения-из-простого-скрипта)
    - [Отключение SIP](#Отключение-SIP)
    - [Отключение Spotlight](#Отключение-Spotlight)
    - [Отключение уведомления "default interactive shell is now zsh"](#Отключение-уведомления-default-interactive-shell-is-now-zsh)
    - [Настройка автодополнения команд в zsh](#Настройка-автодополнения-команд-в-zsh)
    - [Удаление мусора](#Удаление-мусора)
    - [Отключение авторизации для доступа к сертификату из keychain](#Отключение-авторизации-для-доступа-к-сертификату-из-keychain)
    - [Авторизация в консоли через TouchID](#Авторизация-в-консоли-через-TouchID)
    - [Terminal. Удаление слов через option + delete](#Terminal-удаление-слов-через-option-+-delete)
    
2. <h3>[Установка/удаление программ](#Установка/удаление-программ)</h3>

    - <h4>[Brew](#Brew)</h4>
    
        - [Установка brew](#Установка-brew)
        - [Использование несколькими пользователями](#Использование-несколькими-пользователями)
        - [Установка пакетов brew](#Установка-пакетов-brew)
        - [Удаление пакетов brew](#Удаление-пакетов-brew)
        - [Репозитории brew](#Репозитории-brew)
        - [Кэш brew](#Кэш-brew)
        - [Смена используемой версии пакета](#Смена-используемой-версии-пакета)
        - [Запуск и остановка фоновых служб brew](#Запуск-и-остановка-фоновых-служб-brew)
        - [Установка приложений](#Установка-приложений)
        
    - <h4>[PGK](#PGK)</h4>
    
        - [Удаление pkg](#Удаление-pkg)
        
    - <h4>[Python](#Python)</h4>
    
        - [Установка PyQt4](#Установка-PyQt4)
        - [Установка lxml](#Установка-lxml)
        - [Установка mpi4py](#Установка-mpi4py)
        - [Установка numpy](#Установка-numpy)

3. <h3>[Устранение проблем](#Устранение-проблем)</h3>
    
    - [Не удаляется VPN соединение](#Не-удаляется-VPN-соединение)

4. <h3>[Разное](#Разное)</h3>
    
    - [Создание автозагрузочной флешки с windows](#Создание-автозагрузочной-флешки-с-windows)
    - [Создание автозагрузочной флешки с linux](#Создание-автозагрузочной-флешки-с-linux)
    - [Разбить большой файл на части](#Разбить-большой-файл-на-части)
    - [Хранение конфигов системы в git](#Хранение-конфигов-системы-в-git)


<a name='Настройка-системы'></a>
## Настройка системы


<a name='Горячие-клавиши'></a>
### Горячие клавиши

**Система**

Комбинация                                        |   Описание 
--------------------------------------------------|-------------------------------
option + (комб. клавиш или взаимодействие с ui )  | option выступает мастер клавишей, которая позволяет получить доступ к большему количеству опций (например если зажать клавишу option и кликнуть по wi-fi или иконке настройке звука, то вы увидите меню с расширенными настройками) или получить альтернативный результат. Более подробно можно узнать [здесь](https://youtu.be/pasrZ4QEUCQ).



**Finder**
 
Комбинация              |   Описание 
------------------------|-------------------------------
shift + command + .     | Показать/скрыть скрытые файлы


Если нужно посмотреть наиболее полную справку по горячим клавишам можно 
поставить программу `CheatSheet`.


<a name='Принудительная-очистка-ОЗУ'></a>
### Принудительная очистка ОЗУ

```
sudo purge
```

<a name='Отключение-Dashboard'></a>
### Отключение Dashboard

Для отключение Dashboard необходимо в консоли выполнить следующие команды

```bash
defaults write com.apple.dashboard mcx-disabled -boolean YES
killall Dock
```

Если вы передумали, включить Dashboard можно следующей командой

```bash
defaults write com.apple.dashboard mcx-disabled -boolean NO
```


<a name='Отключение-автоматического-изменения-порядка-рабочих-столов'></a>
### Отключение автоматического изменения порядка рабочих столов

В macos есть фукнция, которая автоматически меняет порядок созданных рабочих 
столов. Упорядочивает она их по частоте использования. Такое поведение не 
всегда удобно, а иногда вообще доставляет сильный дискомфорт.

К счастью эту "супер крутую" фичу можно отключить!

MacOS < 13.x

- откройте `Системные настройки`
- выберите пункт `Mission Control`
- снимите галочку с `Автоматически использовать последние расположение пространств`

MacOS >= 13.x

- откройте `Системные настройки`
- выберите пункт `Рабочий стол и Dock`
- найдите раздел `Mission Control`
- снимите галочку с `Менять расположение пространств в зависимости от недавнего использования`


<a name='Отображение-в-finder-папок-перед-файлами'></a>
### Отображение в finder папок перед файлами

Полезные ссылки:

- [Finder – как показывать папки перед файлами](https://severe-programmer.com/manual/finder-kak-pokazyvat-papki-pered-faĭlami/) 


<a name='Предпросмотр-содержимого-архива-в-finder'></a>
### Предпросмотр содержимого архива в finder

По умолчанию, для большинства файлов в finder доступен предпросмотр по нажатию `Option` + `Space`. К сожалению,
в этот список не входят архивы. Для исправления этой проблемы необходимо установить `betterzip`.

```bash
brew install --cask betterzip
```

После установки, приложение автоматически начнет работать, но будет не лишним зайти в его настройки и полазить там. 
Оно имеет очень много полезных настроек.


<a name='Изменение-значения-TTL'></a>
### Изменение значения TTL

Time to live (TTL) — число итераций или переходов, за который набор данных 
(пакет) может существовать до своего исчезновения.

Есть 2 способа изменить значение TTL:

1. Значение TTL меняется на ограниченое время. После перезагрузки
   системы будет востановлено значение по умолчанию.

    ```bash
    sudo sysctl -w net.inet.ip.ttl=<нужное значение ttl>
    ```
   
2. Установка постоянного значения TTL делается следующим образом:

    - создаем файл `/etc/sysctl.conf`
    - добавляем в него строку `net.inet.ip.ttl=<нужное значение ttl>`


<a name='Создание-MacOS-приложения-из-простого-скрипта'></a>
### Создание MacOS приложения из простого скрипта

В MacOS программы устроенны очень интересным образом, все программы это 
своебразные пакеты с набором файлов в том, числе и с самой программой. Вы 
можете сами убедиться в этом, нажав на программу правой кнопкой мыши выбрав 
-> `Показать содержимое пакета`.

Внутри вы скорей всего увидите примерно такую структуру:

```
.
└── Contents
    ├── MacOS
    └── Resources
```

`Resources` - содержит ресурсы программы (иконка программы и т.д.), в `MacOS` 
находиться сама программа, точнее исполнительный файл, который запускает 
программу. 

Кроме описанных выше каталогов, в корне папаки `Contents` могут находится еще 
различные текстовые файлы, в них хранятся метаданные пакета.

Теперь, когда мы уже имеем некоторое представление о том, что из себя 
представляют приложения в MacOS, давайте превратим обычный python скрипт в 
полноценное приложение.

Код скрипта:

```python
import sys
from PyQt5.QtWidgets import QApplication, QWidget


app = QApplication(sys.argv)

w = QWidget()
w.resize(250, 150)
w.move(300, 300)
w.setWindowTitle('Simple')
w.show()

sys.exit(app.exec_())
```

Для того, чтобы реализовать задуманное:

- Необходимо создать папку, которая будет иметь такое-же имя как наша программа.
- Потом, создаем внутри этой папки следующую структуру:
    ```
    .
    └── Contents
        ├── MacOS
        ├── Resources
        └── Info.plist
    ```
- Теперь можно разместить внутри папки MacOS наш скрипт, содержание которого 
  мы описали выше.
- Кроме самого python скрипта, потребуется еще bash скрипт, который
  будет указывать, как именно запускать python скрипт. Расположить его 
  необходимо так же в папке MacOS. В нашем случае скрипт будет называться 
  simpleapp и будет иметь следующие содержание:
  ```bash
  #!/usr/bin/env bash
  BASE_DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
  cd "$BASE_DIR"
  python3 ./main.py
  ``` 
- Для того, чтобы скрипт успешно выполнился, он должен иметь права на 
  исполнение. Дать ему эти права можно следующей командой: `sudo chmod +x simpleapp`
- После создания скриптов, необходимо скопировать иконку изображения в папку 
  Resources. Иконка должна быть в формате `*.icns`.
- Теперь, необходимо создать в корне папки `Contents` файл `Info.plist` со 
  следующим содержанием:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
        <dict>
            <key>CFBundleDevelopmentRegion</key>
            <string>English</string>
            <key>CFBundleExecutable</key>
            <string>run.sh</string>
            <key>CFBundleIconFile</key>
            <string>app.icns</string>
            <key>CFBundleInfoDictionaryVersion</key>
            <string>6.0</string>
            <key>CFBundleName</key>
            <string>Simple app</string>
            <key>CFBundlePackageType</key>
            <string>APPL</string>
            <key>CFBundleIdentifier</key>
            <string>org.python.python</string>
            <key>CFBundleSignature</key>
            <string>????</string>
            <key>CFBundleGetInfoString</key>
            <string>Simple app 1.0.0</string>
            <key>CFBundleShortVersionString</key>
            <string>1.0.0</string>
            <key>CFBundleVersion</key>
            <string>1.0.0</string>
            <key>LSApplicationCategoryType</key>
            <string>public.app-category.entertainment</string>
    
            <key>NSRequiresAquaSystemAppearance</key>
            <string>false</string>
    
            <key>LSRequiresNativeExecution</key>
            <string>YES</string>
            <key>LSMinimumSystemVersion</key>
            <string>10.8</string>
        </dict>
    </plist>
    ```
- И в качестве завершающего этапа, необходимо к имени папки, которую мы 
  создали выполняя первый этап инструкции, добавить расширение `.app`.
  
После того, как были проделаны все описанные выше пункты, должнна получиться 
папка со следующим содержанием:

```
.
└── Simple\ app.app
    └── Contents
        ├── Info.plist
        ├── MacOS
        │   ├── main.py
        │   └── run.sh
        └── Resources
            └── app.icns

```  
 
Теперь, вы можете 2 раза щелкнуть по папке `Simple app` и будет запущен 
созданный нами скрипт. 

**P.S.**

Для того, чтобы убедиться в том, что у нашего приложения отображается 
правильная картинка, необходимо либо перезагрузить комьютер, либо просто 
выполнить `touch ./Simple app.app`.

Полезные ссылки:

- [Превращаем Bash скрипт в macOS *.app программу](http://mynotelist.blogspot.com/2016/06/macos-bash-macos-app.html)
- [Changing Mac OS X Application Icons Programmatically](https://www.sethvargo.com/replace-icons-osx)
- [Пример скрипта, который автоматически собирает python приложение в macos пакет](https://bitbucket.org/alex925/serial-notifier/src/master/tools/create_macos_package.py)
- [building-osx-app-bundle - stackoverflow](https://stackoverflow.com/questions/1596945/building-osx-app-bundle)


<a name='Отключение-SIP'></a>
### Отключение SIP

System Integrity Protection – это технология, направленная на защиту от 
вредоносного программного обеспечения. SIP серьезно ограничивает возможность 
любого изменения системных файлов сторонним программами или пользователем. 
Доступ к редактированию обладают только особые процессы, подписанные Apple. 
Например, один из таких процессов — обновление ПО.

Данный способ защиты может доставлять достаточно большое количество проблем, 
если компьюетр используется для ведения разработки, по этому лучше его 
отключить.

Для того, чтобы отключить SIP, вам необходимо выполнить следующие действия:

- выключаем mac
- при включении удерживаем комбинацию клавиш Command + R, чтобы загрузился 
  режим Recovery
- после загрузки выбираем в меню «Утилиты» приложение «Терминал»
- в терминале выполняем команду
  ```bash
  csrutil disable
  ```
  Если в будующем вы решите обратно включить данную защиту, то вам необходимо
  выполнить
  ```bash
  csrutil enable
  ```

<a name='Отключение-Spotlight'></a>
### Отключение Spotlight

Spotlight - это система «глобального» поиска по компьютеру. Она переодически 
запускает индексацию файлов, и тратит на это ресурсы компьютера (аккумулятор, 
процессор и т д). Если вы не пользутесь данной службой, то лучше будет ее 
отключить.

Сделать это можно командой:

```bash
sudo mdutil -a -i off
``` 

Включить обратно службу можно будет так:

```bash
sudo mdutil -a -i on
``` 

Полезные ссылки:

- [Как ускорить работу Mac и сократить расход батареи с помощью Spotlight](https://iphonegeek.me/instructions/dlya-chajnikov/255-kak-uskorit-rabotu-mac-i-sokratit-rashod-batarei-s-pomoschyu-spotlight.html)


<a name='Отключение-уведомления-default-interactive-shell-is-now-zsh'></a>
### Отключение уведомления "default interactive shell is now zsh"

После обновления на macos catalina при открытии терминала всегда появляется 
надоедливое сообщение:

>The default interactive shell is now zsh. To update your account to use zsh, 
>please run chsh -s /bin/zsh.

К счатью его можно легко отключить. Для этого необходимо добавить в файл
`~/.bash_profile` строку `export BASH_SILENCE_DEPRECATION_WARNING=1`.


<a name='Настройка-автодополнения-команд-в-zsh'></a>
### Настройка автодополнения команд в zsh

В данном примере будет показно, как включить автодополнение для: git, poetry, docker и docker-compose.

1. Устанавливаем bash-completion `brew install bash-completion`
2. Создаем папку для хранения файлов необходимых для автодополнения.

    > Если у вас в окружении не определена переменная окружения HOMEBREW_PREFIX, то вам нужно инициализировать 
    > окружение при помощи вызова `brew shellenv`.

    ```
    mkdir -p ~/.zsh && cd ~/.zsh
   
    poetry completions zsh > ~/.zsh/_poetry
   
    curl -o git-completion.bash https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash
    curl -o _git https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.zsh
   
    cp $HOMEBREW_PREFIX/share/zsh/site-functions/_docker ~/.zsh/_docker
    cp $HOMEBREW_PREFIX/share/zsh/site-functions/_docker_compose ~/.zsh/_docker_compose
    ```

3. Активируем загрузку автодополнений. Для этого открываем `~/.zshrc` и добавляем туда

    ```
    # Enable console autocompletion
    zstyle ':completion:*:*:git:*' script ~/.zsh/git-completion.bash
    fpath=(~/.zsh $fpath)
    autoload -Uz compinit && compinit
    ```

4. Перезагружаем консоль и наслаждаемся.

P.S. Если вы хотите включить автодополнение еще для какой-то утилиты и вы эту утилиту устанавливали через brew, то
первым делом попробуйте поискать файл нужный для включения автодополнения в папке 
`$HOMEBREW_PREFIX/share/zsh/site-functions/`.


<a name='Удаление-мусора'></a>
### Удаление мусора

Удаление ненужных файлов XCode

```bash
#!/bin/bash

# Delete Archived Applications
rm -r ~/Library/Developer/Xcode/Archives/*/

# Delete Devired Data
rm -r ~/Library/Developer/Xcode/DerivedData/*/

# Delete Apple cached files
rm -r ~/Library/Developer/CoreSimulator/Caches/dyld/*/*/

# Delegete cache on com.apple.DeveloperTools
rm -r /private/var/folders/dk/*/C/com.apple.DeveloperTools/*/

# Delete unused simulators
xcrun simctl delete unavailable
```


<a name='Отключение-авторизации-для-доступа-к-сертификату-из-keychain'></a>
### Отключение авторизации для доступа к сертификату из keychain

Некоторые приложения могут запрашивать доступ к сертификатам установленным в keychain и по 
умолчанию MacOS в этом случае будет запрашивать авторизацию. Если это происходит часто, это 
может начать бесить. Я столкнулся с такой проблемой при использовании Google Chrome. Ниже я
опишу как решить эту проблему.

1. Открываем keychain.

2. Находим там закрытый ключ к которому пытается получить доступ Google Chrome.

    P.S. Название ключа прописано во всплывающем окне `Выбор сертификата`.

3. Открываем его свойства и переходим во вкладку `Доступ`.

4. Добавляем нужное приложение (в моем случае это был Google Chrome) в список `Всегда разрешать доступ этим программам`.


<a name='Авторизация-в-консоли-через-TouchID'></a>
### Авторизация в консоли через TouchID


Делаем резервную копию конфига sudo демона и открываем его на редактирование

```
cp /etc/pam.d/sudo ~/
sudo vim /etc/pam.d/sudo
```

Добавьте первой строкой после комментария следующий текст:

```
auth       sufficient     pam_tid.so
```

> Сохраните файл, но не закрывайте редактор, сначала проверьте в соседнем окне
> терминала, что вы без проблем можете запускать приложения используя sudo. Так
> если у вас возникнут какие-то проблемы, вы сможете откатить сделанные изменения. 

В результате у вас должно получится, что-то вроде этого:

```
# sudo: auth account password session
auth       sufficient     pam_tid.so
auth       sufficient     pam_smartcard.so
auth       required       pam_opendirectory.so
account    required       pam_permit.so
password   required       pam_deny.so
session    required       pam_permit.so
```

Переоткройте терминал и наслаждайтесь тем, что подтвердить выполнение программы
от имени суперпользователя можно при помощи отпечатка пальца.

Полезные ссылки:

- [How to use sudo with Touch ID on a Mac](https://nicholasmangold.com/blog/how-use-sudo-touch-id-mac)


<a name='Terminal-удаление-слов-через-option-+-delete'></a>
### Terminal. Удаление слов через option + delete

В терминале можно удалять слова целиком, если нажать `option` + `delete`, но по умолчанию 
данный hotkey не активен. Активировать его можно следующим образом:

- открываем терминал
- нажимаем `cmd` + `,`, чтобы открыть настройки терминала
- переходим во вкладку `Profiles` -> `Keyboard`
- внизу окна находим `Use Option as Meta key` и активируем его

Нашел [здесь](https://stackoverflow.com/questions/327664/mac-os-x-terminal-map-optiondelete-to-backward-delete-word).


<a name='Установка/удаление-программ'></a>
## Установка/удаление программ


<a name='Brew'></a>
### Brew

<a name='Установка-brew'></a>
#### Установка brew

**Установка на mac с intel**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Полезные ссылки:
- http://dghubble.com/blog/posts/homebrew-os-x-package-management/


**Установка на mac с apple silicon**

Работа на mac с apple silicon имеет свои особенности. Это связано с тем, что пока не все программы имеют нативные 
версии. По этому ниже будет описано как установить и использовать brew на устройствах с чипом от apple.

Установка и настройка системы:

1. Для начала, необходимо установить 2 версии brew, одна позволит нам устанавливать программы, которые будут работать 
   через эмулятор, а вторая будет устанавливать нативные приложения.

    ```
    arch -x86_64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    arch -arm64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

    После установки brew для m1 будет установлен в `/opt/homebrew/bin/brew`, а для intel `/usr/local/bin/brew`.

2. После установки очень важно правильно настроить инициализацию окружения. Для этого открываем файл `~/.zshrc` и 
    добавляем в него следующие строки:

    ```bash
    # brew
    if [[ $(arch) == 'arm64' ]]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    else
        eval "$(/usr/local/bin/brew shellenv)"
    fi
     
    # Генерирует флаги необходимые для сборки из исходников сишных библиотек
    export LDFLAGS=""
    export CPPFLAGS=""
    export PKG_CONFIG_PATH=""
     
    pkgs=(openssl@1.1 curl readline zlib sqlite)
    for pkg in $pkgs; do
        pkg_dir="$HOMEBREW_PREFIX/opt/$pkg"
     
        lib_dir="$pkg_dir/lib"
     
        if [ -d "$lib_dir" ]; then
            export LDFLAGS="$LDFLAGS -L$lib_dir"
        fi
     
        include_dir="$pkg_dir/include"
        if [ -d "$include_dir" ]; then
            export CPPFLAGS="$CPPFLAGS -I$include_dir"
        fi
     
        pkg_config_dir="$lib_dir/pkgconfig"
        if [ -d "$pkg_config_dir" ]; then
            if [ "x$PKG_CONFIG_PATH" = "x" ]; then
                export PKG_CONFIG_PATH="$pkg_config_dir"
            else
                export PKG_CONFIG_PATH="PKG_CONFIG_PATH:$pkg_config_dir"
            fi
        fi
    done
    ```
   
    Данная конфигурация описывает логику выбора версии brew и создает переменные окружения необходимые для сборки из 
    исходников приложений, которые зависят от софта устанавливаемого через brew.

    В переменной pkgs описаны пакеты, которые являются зависимостями необходимыми для сборки других приложений из 
    исходников. В данный момент там перечисленны некоторые из очень популярных библиотек, если для сборки нужной вам 
    библиотеки нужные другие пакеты, которые вы уже установили, просто добавьте их туда.

3. Теперь закройте и откройте новое окно терминала. Это необходимо для загрузки ранее описанной конфигурации.

Теперь, когда система настроена. Для установки нативных приложений вам всегда необходимо открывать терминал для 
архитектуры arm64, а для установки старых приложений терминал нужно открывать для архитектуры x86_64. Сделать это можно 
так:

```bash
# Открывает терминал позволяющий работать с нативными приложениями
arch -arm64 zsh

# Открывает терминал позволяющий работать с приложениями в режиме эмуляции
arch -x86_64 zsh
```

> Необходимо обратить внимание, что нужно делать именно так. Если вы будете пробовать выполнять команды вида 
> `arch -x86_64 brew install python`, то возможно возникновение проблем, так как вы работаете в уже настроенном для 
> другой архитектуры окружении.

<a name='Использование-несколькими-пользователями'></a>
#### Использование несколькими пользователями

Если вы хотите использовать brew на одном компьютере несколькими пользователями, то у вас сразу возникает проблема, так
как brew не заточен под такое использование. Нормально решить эту проблему на сколько я знаю нельзя, но есть
несколько костылей. Они могут частично решить проблему. Ниже я опишу наиболее адекватный костыль, который сейчас сам 
использую:

1. Создаем отдельного пользователя.
2. Авторизуемся под ним и [устанавливаем brew](#Установка-brew) в нем.
3. После этого настраиваем в `.zshrc` инициализацию окружения в каждом из пользователей, которые будут использовать 
brew.
4. Добавляем в `.zshrc` следующий alias:

    ```
    alias brew='sudo -Hu <account_name> brew'
    ```
    
    Это позволит нам запускать brew от имени пользователя, которого мы создали на первом этапе.

P.S. Важно заметить, что вариант не идеальный и с некоторыми приложениями могут возникать проблемы.

Полезные ссылки:

- https://www.codejam.info/2021/11/homebrew-multi-user.html
- https://stackoverflow.com/questions/13762280/zsh-compinit-insecure-directories


<a name='Установка-пакетов-brew'></a>
#### Установка пакетов brew

```bash
brew install <FORMULA>
```

FORMULA - это название пакета, который будет установлен.

**Установка конкретной версии**

При помощи команды выше будет установлена самая последняя версия приложения.
Если вам необходимо установить определенную версию, то необходимо будет сделать 
немного больше телодвижений:

- заходим в репозиторий и ищем в Pull requests коммит с нужной нам версией
программы и переходим к нему
- открываем вкладку commits
- переходим к коду этого коммита
- нажимаем view, чтобы посмотреть код этого коммита
- теперь переходим в режим просмотра кода raw
- копируем ссылку из адресной строки и подставляем в команду
    ```bash
    brew install https://raw.github.com/dsr/homebrew/9b22d42f50fcbc5e52c764448b3ac002bc153bd7/Library/Formula/python3.rb
    ``` 
Таким способом можно поставить любую версию интересующей вас программы.

Ссылки на дополнительную информацию:

- https://github.com/Homebrew/homebrew/blob/master/share/doc/homebrew/Tips-N'-Tricks.md
- http://effectif.com/mac-os-x/installing-specific-version-of-homebrew-formula (инф. старая)


<a name='Удаление-пакетов-brew'></a>
#### Удаление пакетов brew

Удаление пакетов установленных при помощи brew производится командой:

```bash
brew rm <FORMULA>
```

Неприятным моментом является то, что эта команда удаляет только указанный пакет,
а все зависимости данного пакета остаются. Частичным решением данной проблемы 
является команда (выполнять ее нужно после удаления самого пакета):

```bash
brew rm $(join <(brew leaves) <(brew deps FORMULA))
```

- `FORMULA` - название пакета у которого необходимо найти неиспользуемые 
   зависимости
- `brew leaves` - выводит все пакеты, которые не зависят от других пакетов
- `brew deps` - выводит пакеты, от которых зависит данный пакет

Она удаляет пакеты зависящие от удаляемого пакета и те которые не 
зависят больше ни от каких других пакетов. К сожалению данный способ ни как не
решает проблему циклических зависимостей.

**rmtree**

rmtree - это расширение для brew, которое в теории должно позволять 1 командой
удалять пакет со всеми его зависимостями. К сожалению, работает оно не всегда 
хорошо.

Установка rmtree делается следующей командой:

```bash
brew tap beeftornado/rmtree
```

Теперь удалять пакеты можно следующей командой:

```bash
brew rmtree <package>
```


Если подытожить, то пока нет идеального способа удалить пакет со всеми его 
зависимостями. Лучший способ - это комбинация 2 описанных ранее способов.

Ссылки по теме:

- http://oryband.com/removing-homebrew-packages-with-dependencies/
- https://stackoverflow.com/questions/7323261/uninstall-remove-a-homebrew-package-including-all-its-dependencies


<a name='Репозитории-brew'></a>
#### Репозитории brew

Репозитории в brew называются tap.

Добавить новый репозиторий можно командой:

```bash
brew tap <REPO>
```

Список полезных реппозиториев:

- homebrew/cask


<a name='Кэш-brew'></a>
#### Кэш brew

Для получения пути к папке где brew хранит исходники использовавшиеся
для сборки, нужно выполнить:

```bash
brew --cache
```

<a name='Смена-используемой-версии-пакета'></a>
#### Смена используемой версии пакета

Brew позволяет вам установить одновременно несколько версий одного приложения, 
но по умолчанию у вас будет вызываться последняя установленная версия.
Для того, чтобы переключиться на предыдущую версию необходимо использовать 
команду switch.

Общий синтаксис команды

```bash
brew switch <FORMULA> <VERSION>
```

Пример установки python 3.5.1 как версии используемой по умолчанию 

```bash
brew switch python3 3.5.1
```


<a name='Запуск-и-остановка-фоновых-служб-brew'></a>
#### Запуск и остановка фоновых служб brew

https://robots.thoughtbot.com/starting-and-stopping-background-services-with-homebrew


<a name='Установка-приложений'></a>
#### Установка приложений

brew — «менеджер недостающих пакетов для macOS», как его называет создатель. 
Изначально он предназначается для компиляции приложений из исходных кодов. Но 
brew умеет не только это. Вместе с дополнением homebrew-cask он способен 
устанавливать приложения из «Терминала».

Для этого необходимо добавить в Homebrew репозиторий cask:

```
brew tap caskroom/cask
```

После этого, можно устанавливать приложения просто 1 командой. Например, 
команда ниже производит установку браузера google chrome:

```
brew install --cask google-chrome
```

Если вам требуется установить несколько приложений, то вы можете сделать это 1 
командой. Данная команда установит docker и google-chrome:

```
brew install --cask google-chrome docker
```

Удаляются установленные приложения также просто как и устанавливаются:

```
brew uninstall --cask google-chrome
```

<a name='Brew-удаление-не-использующихся-зависимостей'></a>
#### Удаление не использующихся зависимостей

```
brew autoremove
```

<a name='PGK'></a>
### PGK

<a name='Удаление-pkg'></a>
#### Удаление pkg

1. Выведем список всех pkg в системе

    ```bash
    pkgutil --pkgs
    ```

2. Выбираем pkg, который нужно удалить и копируем его имя и вставляем его в команду

    ```bash
    pkgutil --forget <скопированное имя>
    ```
    
3. Перетащить app файл в корзину (если он остался)


<a name='Python'></a>
### Python

<a name='Установка-PyQt4'></a>
#### Установка PyQt4

```bash
brew install pyqt --with-python3
```

<a name='Установка-lxml'></a>
#### Установка lxml

Для того, чтобы установить библиотеку lxml нужно сначала установить сишную 
реализацию этой либы

```bash
brew install libxml2 
brew install libxslt
 
brew link libxml2 --force 
brew link libxslt --force
```

Теперь можно устанавливать обертку для python

```bash
pip3 install lxml
```

Теперь можно выполнить

```bash
brew unlink libxml2 
brew unlink libxslt
```

<a name='Установка-mpi4py'></a>
#### Установка mpi4py

```bash
brew install mpich
pip3 install mpi4py
```

<a name='Установка-numpy'></a>
#### Установка numpy

```bash
brew install homebrew/python/numpy --with-python3
```



<a name='Устранение-проблем'></a>
## Устранение проблем

<a name='Не-удаляется-VPN-соединение'></a>
### Не удаляется VPN соединение

Иногда может случиться так, что у вас не получается удалить старое VPN 
соединение (кнопка удаления в меню "Сеть" не активна и в меню "Профили"
профиль для вашего VPN уже удален). 
В этом случае придется удалить информацию о всех VPN соединениях.

```bash
sudo cp /Library/Preferences/com.apple.networkextension.plist /Library/Preferences/com.apple.networkextension.plist.old
sudo rm /Library/Preferences/com.apple.networkextension.plist 
```

P.S. Если у вас не получается удалить файл, то проверьте отключен ли у вас SIP. 

Полезные ссылки:

- [Where macOS keeps VPN Network configuration?](https://apple.stackexchange.com/questions/315797/where-macos-keeps-vpn-network-configuration)



<a name='Разное'></a>
## Разное

<a name='Создание-автозагрузочной-флешки-с-windows'></a>
### Создание автозагрузочной флешки с windows

Для создания автозагрузочной флешки сделайте следующее:

1. Подключите флешку к ПК

2. Откройте терминал и введите там команду

    ```
    diskutil list
    ``` 
    
    ```
    MBP-Aleksej:~ aleksey$ diskutil list
    /dev/disk0 (internal, physical):
       #:                       TYPE NAME                    SIZE       IDENTIFIER
       0:      GUID_partition_scheme                        *1.0 TB     disk0
       1:                        EFI EFI                     314.6 MB   disk0s1
       2:                 Apple_APFS Container disk1         1.0 TB     disk0s2
    
    /dev/disk1 (synthesized):
       #:                       TYPE NAME                    SIZE       IDENTIFIER
       0:      APFS Container Scheme -                      +1.0 TB     disk1
                                     Physical Store disk0s2
       1:                APFS Volume Macintosh HD — данные   185.7 GB   disk1s1
       2:                APFS Volume Preboot                 84.1 MB    disk1s2
       3:                APFS Volume Recovery                528.1 MB   disk1s3
       4:                APFS Volume VM                      1.1 GB     disk1s4
       5:                APFS Volume Macintosh HD            11.1 GB    disk1s5
    
    /dev/disk2 (external, physical):
       #:                       TYPE NAME                    SIZE       IDENTIFIER
       0:      GUID_partition_scheme                        *7.8 GB     disk2
       1:                        EFI EFI                     209.7 MB   disk2s1
       2:       Microsoft Basic Data WIN10                   7.6 GB     disk2s2
    ```
    
    Данная команда позволила нам узнать идентификатор, который система присвоила
    нашей флешке. В моем случае флешка называется `/dev/disk2`.

3. Теперь необходимо отформатировать флешку для работы в windows.

    ```
    diskutil eraseDisk MS-DOS "LIVEUSB" GPT /dev/disk2
    ```
    
    ```
    Started erase on disk2
    Unmounting disk
    Creating the partition map
    Waiting for partitions to activate
    Formatting disk2s2 as MS-DOS (FAT) with name LIVEUSB
    512 bytes per physical sector
    /dev/rdisk2s2: 14814936 sectors in 1851867 FAT32 clusters (4096 bytes/cluster)
    bps=512 spc=8 res=32 nft=2 mid=0xf8 spt=32 hds=255 hid=411648 drv=0x80 bsec=14843904 bspf=14468 rdcl=2 infs=1 bkbs=6
    Mounting disk
    Finished erase on disk2
    ```
    
    Если при форматировании возникли ошибки, то необходимо выполнить немного другую
    команду:
    
    ```
    diskutil eraseDisk MS-DOS "LIVEUSB" MBR /dev/disk2
    ```

4. Примонтируем iso образ, который будем устанавливать на флешку

    ```
    hdiutil mount ~/Downloads/Win10.iso
    ```

5. Скопируем все файлы из образа на нашу флешку

    ```
    cp -rp /Volumes/Win10/* /Volumes/LIVEUSB/
    ```

Отлично, теперь все готово, можно извлечь флешку и использовать.

Полезные ссылки:

- [How Make a Windows 10 USB Using Your Mac - Build a Bootable ISO From Your Mac's Terminal](https://www.freecodecamp.org/news/how-make-a-windows-10-usb-using-your-mac-build-a-bootable-iso-from-your-macs-terminal/)


<a name='Создание-автозагрузочной-флешки-с-linux'></a>
### Создание автозагрузочной флешки с linux

1. Подключите флешку

2. Отформатируйте при помощи дисковой утилиты ее в FAT

3. Откройте терминал и введите там команду

    ```
    diskutil list
    ``` 
    
    ```
    MBP-Aleksej:~ aleksey$ diskutil list
    /dev/disk0 (internal, physical):
       #:                       TYPE NAME                    SIZE       IDENTIFIER
       0:      GUID_partition_scheme                        *1.0 TB     disk0
       1:                        EFI EFI                     314.6 MB   disk0s1
       2:                 Apple_APFS Container disk1         1.0 TB     disk0s2
    
    /dev/disk1 (synthesized):
       #:                       TYPE NAME                    SIZE       IDENTIFIER
       0:      APFS Container Scheme -                      +1.0 TB     disk1
                                     Physical Store disk0s2
       1:                APFS Volume Macintosh HD — данные   185.7 GB   disk1s1
       2:                APFS Volume Preboot                 84.1 MB    disk1s2
       3:                APFS Volume Recovery                528.1 MB   disk1s3
       4:                APFS Volume VM                      1.1 GB     disk1s4
       5:                APFS Volume Macintosh HD            11.1 GB    disk1s5
    
    /dev/disk2 (external, physical):
       #:                       TYPE NAME                    SIZE       IDENTIFIER
       0:      GUID_partition_scheme                        *7.8 GB     disk2
       1:                        EFI EFI                     209.7 MB   disk2s1
       2:       Microsoft Basic Data WIN10                   7.6 GB     disk2s2
    ```
    
    Данная команда позволила нам узнать идентификатор, который система присвоила
    нашей флешке. В моем случае флешка называется `/dev/disk2`.

4. Отмонитируем флешку

    ```
    diskutil unmountDisk /dev/disk2
    ```

5. Теперь можно приступать к записи образа

    ```
    sudo dd if=~/Downloads/linuxmint-20-mate-64bit.iso of=/dev/disk2 bs=1m
    ```
    
    После того как команда завершится, macos выкинет предупреждение "Вставленный 
    Вами диск не может быть прочитан на этом компьютере", это совершенно нормально,
    вам необходимо нажать "Извлечь".

6. Можно использовать сделанную флешку по назначению


Полезные ссылки:

- [How To Create A Bootable Ubuntu USB Drive For Mac In OS X](https://itsfoss.com/create-bootable-ubuntu-usb-drive-mac-os/)


<a name='Разбить-большой-файл-на-части'></a>
### Разбить большой файл на части

Разбить большой файл на части можно при помощи команды split

```bash
split -a 1 -d -b 4000M sample.iso sample.iso.part
```

Данная команда разобьёт исходный файл sample.iso на части по 4 Гбайта, каждая из 
которых будет именоваться как sample.iso.part<N>, где N = 0, 1, 2, ... .

Собрать файл потом можно при помощи cat:

```bash
cat sample.iso.part* > sample.iso
```

Применение маски приведет к тому, что утилита cat переберет все файлы по порядку, начиная с sample.iso.part0.

Источник: https://habr.com/ru/articles/43260/


<a name='Хранение-конфигов-системы-в-git'></a>
### Хранение конфигов системы в git

Чтобы иметь воспроизводимые настройки системы, удобно хранить некоторые из конфигов домашнй 
директории в git репозитории. Сделать это можно следующим образом.

Инициализирует проект и настраиваем его:

```bash
git init --bare $HOME/.home-git
echo -e "\n\n[status]\n\tshowUntrackedFiles = no" >> $HOME/.home-git/config
```

Эти команды создадут новый проект и укажут, что не нужно отслеживать по умолчанию все файлы, 
так как мы будем добавлять под версионный контроль только те файлы, которые нам нужны.

После этого нужно добавить в систему следующий alias:

```bash
alias home='git --work-tree=$HOME --git-dir=$HOME/.home-git'
```

Этот alias будет указывывать папку `$HOME/.home-git` как git репозиторий, а `$HOME` как рабочую папку. 
Такой подход удобен, так как снижает риск случайно закомитить то что не нужно.

После это добавляем нужные файлы под версионный контроль, коммитим их теперь мы всегда будем иметь 
настройки нашей системы, которые удобно переносить между разными системами.

```bash
home add .zshrc
home add .zprofile
home commit -m init
home push
```

На новом компьютере, чтобы получить все настройки, нужно будет сделать следующее:

```bash
git clone --bare <git-repo-url> $HOME/.home-git
```

Полезные ссылки:

- [Git home config](https://mirror.xyz/bobuk.eth/1fxC0ks6p3Js-cbpYLwuP3iPLOsXJkmnQCChnHdfSlo)
- [Dotfiles: Best way to store in a bare git repository](https://www.atlassian.com/git/tutorials/dotfiles)

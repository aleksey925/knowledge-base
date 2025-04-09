Git
===

# Оглавление

1. <h3>[Теория](#Теория)</h3>

    - [Терминология](#Терминология)
    - [Обучение](#Обучение)

2. <h3>[Настройка](#Настройка)</h3>

    - <h4>[Общая настройка](#Общая-настройка)</h4>

        - [Начальная настройка](#Начальная-настройка)
        - [Автодополнение в MacOS](#Автодополнение-в-MacOS)
    
    - <h4>[Решение проблем](#Решение-проблем)</h4>
    
        - [SSL Certificate problem: unable to get local issuer certificate](#SSL-Certificate-problem:-unable-to-get-local-issuer-certificate)
        - [Не сохраняется логин/пароль](#Не-сохраняется-логин/пароль)
    
3. <h3>[Локальные репозитории](#Локальные-репозитории)</h3>

    - [Общее](#Общее)
    - [Перезапись истории](#Перезапись-истории)
    - [Локальный gitignore](#Локальный-gitignore)
    - [Авторизация при помощи токена](#Авторизация-при-помощи-токена)
    
<a name='Теория'></a>
## Теория

<a name='Терминология'></a>
### Терминология
    
Индекс и область подготовленных файлов - это синонимы.
Самый быстрый способ увидеть что индексе, можно с помощью команды `git status`. 
Когда вы выполните команду `git status`, то увидите какие файлы попали в 
индекс, какие модифицированы, но не в индексе и какие в данный момент вообще не 
отслеживаются git.

<a name='Обучение'></a>
### Обучение

<https://learngitbranching.js.org/?demo> - сервис, который позволяет 
визуализировать действие тех или иных команд git.

<a name='Настройка'></a>
## Настройка

<a name='Общая-настройка'></a>
### Общая настройка

<a name='Начальная-настройка'></a>
#### Начальная настройка

Настройки для git которые нужные выполнить после установки git и на linux и 
windows.

- `git config --global user.name "Aleksey Petrunnik"` - задаем имя пользователя
- `git config --global user.email my_mail@mail.ru` - задаем email пользователя
- `git config --global core.editor nano` - задаём редактор по умолчанию
- `git config --list` - выводит список установленных настроек

В windows ещё нужно выполнить:

```bash
git config --global core.autocrlf true
git config --global core.safecrlf true
```

Для корректного отображения киррилицы в nano, необходимо создать следующую 
переменную окружения:

- `LANG: ru_RU.UTF8`


<a name='Автодополнение-в-MacOS'></a>
#### Автодополнение в MacOS

**bash**

По умолчанию в терминале MacOS для git отключено автодоплнение. Исправить это
можно следующим образом:

- выполнить поиск в системе скрипта `git-completion.bash`

    ```bash
    sudo find / -type f -name "git-completion.bash"
    ```
    
    Результат выполнения команды будет примерно такой:
    
    ```
    MBP-Aleksej:~ aleksey$ sudo find / -type f -name "git-completion.bash"
    /Library/Developer/CommandLineTools/usr/share/git-core/git-completion.bash
    ```

- после того как путь к скрипту найден необходимо скопировать его в папку
    `/usr/local/etc/bash_completion.d/git-completion.bash`.
  
    ```
    sudo cp /Library/Developer/CommandLineTools/usr/share/git-core/git-completion.bash /usr/local/etc/bash_completion.d/git-completion.bash 
    ```

Теперь если открыть новое окно терминала, то там будет доступно автодополнение 
при вводе команд для git. 

**zsh**

- устанавливаем bash-completion

    ```
    brew install bash-completion
    ```

- скачиваем необходимые скрипты

    ```
    mkdir -p ~/.zsh && cd ~/.zsh
    
    curl -o git-completion.bash https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash
    curl -o _git https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.zsh
    ```

- включаем использование скриптов. Для этого открываем файл `~/.zshrc` и вставляем туда

    ```
    # Load Git completion
    zstyle ':completion:*:*:git:*' script ~/.zsh/git-completion.bash
    fpath=(~/.zsh $fpath)
    
    autoload -Uz compinit && compinit
    ```

- очищаем cache
    
    ```
    rm ~/.zcompdump
    ```

Полезные ссылки:

- [Adding Git Completion to Zsh](https://oliverspryn.medium.com/adding-git-completion-to-zsh-60f3b0e7ffbc)


<a name='Решение-проблем'></a>
### Решение проблем

<a name='SSL-Certificate-problem:-unable-to-get-local-issuer-certificate'></a>
#### SSL Certificate problem: unable to get local issuer certificate

При клонировании репозитория (возможно не только при клонировании) может 
возникнуть ошибка `SSL Certificate problem: unable to get local issuer 
certificate`. Устранить ее можно просто отключив проверку SSL сертификата. 

Сделать это можно 2 способами:

- `export GIT_SSL_NO_VERIFY=1`
- `git config --global http.sslVerify false`

Ответ нашел [тут](https://confluence.atlassian.com/bitbucketserverkb/ssl-certificate-problem-unable-to-get-local-issuer-certificate-816521128.html)


<a name='Не-сохраняется-логин/пароль'></a>
#### Не сохраняется логин/пароль

Для включения возможности сохранять credential необходимо выполнить

```
git config --global credential.helper store
```

Полезные ссылки:

- [How to save username and password in GIT [GitExtension]?](https://stackoverflow.com/questions/35942754/how-to-save-username-and-password-in-git-gitextension)



<a name='Локальные-репозитории'></a>
## Локальные репозитории

<a name='Общее'></a>
### Общее

**Создание репозитория с проектом** 

`git init` - создаёт репозиторий в текущей папке

**Добавление (удаление) новых или изменённых файлов в репозиторий**

Для того, чтобы добавить файлы под версионный контроль нужно воспользоваться 
командой `add <имя файла>`, после этого будет зафиксировано текущее состояние 
файла и когда будет выполнен комит, в репозитории будет отравлен файл в том 
состоянии в котором он находится во время выполнения команды `add`. После 
внесения изменений файл, если их нужно отправить в репозиторий, то нужно опять 
повторить действия с командой add.

- `git add *.py` - добавить все файлы с расширеним py под версионный контроль 
- `git add .` - добавить все файлы и подпапки текущей папки под версионный контроль 
- `git add phone.txt` - добавить файл phone.txt под версионный контроль 

- `git commit -m 'init version project'` - отправляет в репозиторий все файлы 
  добавленные под версионный контроль. С помощью ключа -m указывается 
  комментарий к комиту. 

- `git rm <файл>` - удаляет файл из рабочей директории, области подготовленных
  файлов, а после выполения commit файл будет удалён и из репозитория
- `git rm <файл> --cached` - удаляет файл из области подготовленных файлов, но 
  оставляет его в рабочей директории
  
**Просмотр информации**

- `git status` - показывает статус репозитория (какие файлы изменились, какие 
новые, какие были добавлены в индекс (было выполнено `git add`, но commit не 
совершался)) 

- `git log` - истории коммитов (автор, емеил, хэш, комментарий) 
- `git log --max-count 2` - информация о 2 последних коммитах

**Возвращение рабочего каталога к предыдущему состоянию**
 
Используется для получения предыдущих версий файлов или просто для переключения
на другую рабочую ветку.

- `git checkout <hash>` - выгружает из репозитория предыдущую версию файла, 
которая зафиксирована в коммите с заданным `<hash>` 

- `git checkout <file name>` - загрузит в рабочую директорию последнею версию 
файла с именем `<file name>`
 
- `git checkout master` - получаем файлы последней версии из ветки master


<a name='Перезапись-истории'></a>
### Перезапись истории

**Изменение последнего комита**

`git commit —amend` - изменение последнего комита

Эта команда полезна в том случае, если нужно изменить последний коммит 
(исправить описание коммита, добавить забытый файл, исправить пару забытых 
опечаток и т д).

Если нужно только изменить описание, то выполняем коммит с ключом `--amend`, 
откроется редактор описания последнего коммита, там вносим правки и сохраняем 
изменения (после закрытия редактора, будет выполнен коммит).
Если же нужно изменить файлы, то меняем их, добавляем их в индекс `git add .` и 
выполняем коммит с ключом `--amend`.

**Объединение нескольких коммитов в один**

**Способ 1**

Объединение всех коммитов в ветке в один.

```
git rebase --root -i
```

В открывшемся окне редактора для всех коммитов кроме первого меняем `pick` на `squash`, сохраняем изменения и закрываем 
файл. 

Такие настройки говорят гиту использовать первый коммит как основной, а все остальные приклеить к нему.

**Способ 2**

Объединение 2 последних коммитов в 1

```
git rebase -i HEAD~2
```

В открывшемся окне редактора для всех коммитов кроме первого меняем `pick` на `squash`, сохраняем изменения и закрываем 
файл.

**Способ 3**

Объединение коммитов в середине истории.

Вместо HEAD указываем хэш нужного коммита и через тильду указываем сколько коммитов нужно склеить.

```
git rebase -i ae88544~3
```

Полезные ссылки:

- <https://stackoverflow.com/questions/1657017/how-to-squash-all-git-commits-into-one>
- <https://pingvinus.ru/git/1591#:~:text=Объединение%20коммитов%20(с%20использованием%20git,-i%20(интерактивный%20режим).&text=Откроется%20текстовый%20редактор%2C%20в%20котором,pick%20ab37583%20Added%20feature%201>
- <https://htmlacademy.ru/blog/27-how-to-squash-commits-and-why-it-is-needed>


**Удаление файла из всех коммитов в репозитории**

Данные команды производят удаление из всех коммитов папки `bin`.
Если необходимо удалить не папку, а файл, то из первой команды нужно убрать 
ключ `--force`.

```bash
git filter-branch --force --index-filter 'git rm -r --cached --ignore-unmatch bin' --prune-empty --tag-name-filter cat -- --all

rm -rf .git/refs/original && git gc --aggressive
git reflog expire --expire=now --all && git gc --prune=now
```

Материалы по теме:

- <http://onedev.net/post/191>
- <https://blog.truecrux.org/post/ix>
- <http://unixforum.org/index.php?showtopic=140254&st=0&gopid=1287903> - здесь 
  мне помогли найти ответ на данный вопрос

**Отправка на сервер измененного репозитория**

В случае если производилось изменение истории коммитов (коммиты объединялись 
при помощи `reset hard` или выполнялся `commit --amend`), то загрузить 
измененную историю на сервер простым `push` не получится. Необходимо
выполнять:

```bash 
git push -f origin master
```

Ответ нашел [тут](https://habrahabr.ru/post/138590/)


<a name='Локальный-gitignore'></a>
### Локальный gitignore

Бывают ситуации, когда в папке с проектом нужно хранить файлы, которые не должны
попасть под версионный контроль, но и файл `.gitignore` расположенный в корне 
проекта использовать нельзя. 

В этом случае можно использовать файл `.git/info/exclude`. Он имеет тот же формат, 
что и `.gitignore`.


<a name='Авторизация-при-помощи-токена'></a>
### Авторизация при помощи токена

[git pull with access token, git push with username / password](https://stackoverflow.com/questions/52445475/git-pull-with-access-token-git-push-with-username-password)

# Tutorial argparse

argparse — это библиотека для простого и удобного создания программ с
консольным интерфейсом.

[Ссылка на оригинал](https://docs.python.org/3/howto/argparse.html)

### Основы

Давайте начнем с самых основ и рассмотрим минимальное количество кода
необходимого для работы argparse.

```python
import argparse
parser = argparse.ArgumentParser()
parser.parse_args()
```

Результат выполнения получим:

```bash
$ python3 prog.py
$ python3 prog.py --help
usage: prog.py [-h]

optional arguments:
  -h, --help  show this help message and exit
$ python3 prog.py --verbose
usage: prog.py [-h]
prog.py: error: unrecognized arguments: --verbose
$ python3 prog.py foo
usage: prog.py [-h]
prog.py: error: unrecognized arguments: foo
```

Вот, что здесь происходит:

- Запущен скрипт без аргументов, на стандартный вывод в результате ничего не
  выведено. Не особо полезно
- Начиная со второго примера начинает раскрываться потенциал argparse. Мы
  практически ничего не сделали, но уже получили справку.
- При использовании не правильных аргументов мы автоматически получаем вывод
  команды --help, которую можно так же сократить до -h. Но по умолчанию, мы
  опять же получаем не информативный вывод.

### Введение в позиционные аргументы

Пример:

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("echo")
args = parser.parse_args()
print(args.echo)
```

В результате запуска выдает:

```bash
$ python3 prog.py
usage: prog.py [-h] echo
prog.py: error: the following arguments are required: echo
$ python3 prog.py --help
usage: prog.py [-h] echo

positional arguments:
  echo

optional arguments:
  -h, --help  show this help message and exit
$ python3 prog.py foo
foo
```

Что здесь происходит:

- Мы здесь добавили использование метода add_argument() , который определяет
  какие аргументы командной строки программа должна принимать. В данном случае,
  аргумент назван echo, в соотвествии с назначением моей программы.
- Теперь при вызове нашей программы мы должны указывать данный аргумент.
- parse_args() возвращает разобранные аргументы командной строки, которые мы
  определили у нашей программы (в данном случае, это echo).
- Нам не нужно определять в каких переменных будут храниться разобранные
  данные. Имя переменной соответствует имени аргумента (в данном случае echo).

В данный момент вывод справки о программе пока все ещё не особо информативен.
На пример мы видим, что программа ожидает позиционный аргумент echo, но мы не
знаем зачем он нужен. По этому давайте сделаем справку немного более
информативной:

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("echo", help="echo the string you use here")
args = parser.parse_args()
print(args.echo)
```

И мы получим:

```bash
$ python3 prog.py -h
usage: prog.py [-h] echo

positional arguments:
  echo        echo the string you use here

optional arguments:
  -h, --help  show this help message and exit
```

Теперь как на счет того, чтобы сделать, что-то ещё более полезное:

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", help="display a square of a given number")
args = parser.parse_args()
print(args.square**2)
```

Результат выполнения следующего кода:

```bash
$ python3 prog.py 4
Traceback (most recent call last):
  File "prog.py", line 5, in <module>
    print(args.square**2)
TypeError: unsupported operand type(s) for ** or pow(): 'str' and 'int'
```

Это не очень хорошо. По умолчанию argparse возвращает все аругменты в строковом
представлении, пока мы явно не укажем тип аругмента. По этому давайте скажем
argparse, что square, это int.

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", help="display a square of a given number",
                    type=int)
args = parser.parse_args()
print(args.square**2)
```

Результат выполнения следующего кода:

```bash
$ python3 prog.py 4
16
$ python3 prog.py four
usage: prog.py [-h] square
prog.py: error: argument square: invalid int value: 'four'
```

Вот теперь отлично. Теперь программа сообщает нам, если передан аргумент не
того типа.

### Необязательные позиционные аргументы

До этого описывались позиционные аргументы, которым нужно было обязательно
передать данные, сейчас мы рассмотрим необязательные позиционные аргументы.

```python
import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('path', nargs='?', default=os.getcwd(),
                    help='путь к папке чье содержимое нужно отобразить')
args = parser.parse_args()
print(args.path)
```

И запустив получим:

```bash
$ python3 prog.py
/home/alex/PycharmProjects/По мелочи
$ python3 prog.py /home/alex
/home/alex
```

- Мы можем запустить программу без параметров (или если у нас есть другие
  параметры, просто пропустить параметр path) и тогда используется значение по
  умолчанию;
- Если значение по умолчанию не устраивает, можно задать необходимое.

Пример такого поведения можно увидеть у программы ls. Мы можем посмотреть файлы
в заданной папке или отобразить файлы из рабочей директории.

### Введение в необязательные аргументы

До сих пор мы игрались с позиционными (обязательными) аргументами. Давайте
теперь посмотрим как добавить не обязательный аргумент.

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--verbosity", help="increase output verbosity")
args = parser.parse_args()
if args.verbosity:
    print("verbosity turned on")
```

И посмотрим вывод:

```bash
$ python3 prog.py --verbosity 1
verbosity turned on
$ python3 prog.py
$ python3 prog.py --help
usage: prog.py [-h] [--verbosity VERBOSITY]
optional arguments:
  -h, --help            show this help message and exit
  --verbosity VERBOSITY
                        increase output verbosity
$ python3 prog.py --verbosity
usage: prog.py [-h] [--verbosity VERBOSITY]
prog.py: error: argument --verbosity: expected one argument
```

Здесь мы видим:

- Программа выводит какие-то подробности, когда --verbosity определен и не
  отображает нечего в обратном случае.
- Так как аргумент действительно не обязательный, то когда мы запускаем
  программу без него, то ошибок не возникает. Нужно заметить, что когда
  необязательный аргумент не используется, то в соответствующей переменной
  (arg.verbosity) хранится None. По этому используется if, для проверки
  хранящегося значения.
- Справка немного отличается.
- Когда мы используем ключ --verbosity, то мы должны определить для него
  какое-то любое значение.

В примере выше, программа принимает произвольное значение типа `int` для
`--verbosity`, но в нашей простой программе нам нужно знать только одно. Был
использован ключ `--verbosity` при запуске программы или нет (`True` или
`False`). Для того, чтобы нам получать только `True` или `False` давайте
исправим код:

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()
if args.verbose:
    print("verbosity turned on")
```

и получим следующий вывод:

```bash
$ python3 prog.py --verbose
verbosity turned on
$ python3 prog.py --verbose 1
usage: prog.py [-h] [--verbose]
prog.py: error: unrecognized arguments: 1
$ python3 prog.py --help
usage: prog.py [-h] [--verbose]
optional arguments:
  -h, --help  show this help message and exit
  --verbose   increase output verbosity
```

Здесь мы видим:

- Этот параметр теперь больше похожа на флаг. По этому мы изменили его
  название. Обратите внимание, мы использовали новый ключевой аргумент `action`
  со значением `'store_true'`. Это значит, что если при вызове будет
  использован параметр `--verbose`, то переменная `args.verbose` будет
  содержать True, а если нет, `False`.
- Вы получите ошибку, если будете пытаться этой опции присвоить какое-то
  значение (по тому, что этот параметр теперь играет роль флага).
- Обратите внимание на изменившийся текст справки.

### Короткие аргументы

Если вы хорошо знакомы с командной строкой, то вы заметили, что мы ещё не
обсудили создание коротких версий аргументов. Это очень просто:

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()
if args.verbose:
    print("verbosity turned on")
```

Это даст:

```bash
$ python3 prog.py -v
verbosity turned on
$ python3 prog.py --help
usage: prog.py [-h] [-v]
optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  increase output verbosity
```

Обратите внимание, что все изменения зафиксированы в справке.

### Комбинирование обязательных и необязательных аргументов

Наша программа усложняется:

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbose:
    print("the square of {} equals {}".format(args.square, answer))
else:
    print(answer)
```

Сейчас выводит:

```bash
$ python3 prog.py
usage: prog.py [-h] [-v] square
prog.py: error: the following arguments are required: square
$ python3 prog.py 4
16
$ python3 prog.py 4 --verbose
the square of 4 equals 16
$ python3 prog.py --verbose 4
the square of 4 equals 16
```

- Мы добавили позиционный (обязательный) аргумент, отсюда и ошибка.
- Обратите внимание, что порядок не имеет значения.

Как насчет того, чтобы усложнить нашу программу и создать несколько уровней
детализации и управлять ими.

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbosity", type=int,
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbosity == 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity == 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)
```

И в выводе получим:

```bash
$ python3 prog.py 4
16
$ python3 prog.py 4 -v
usage: prog.py [-h] [-v VERBOSITY] square
prog.py: error: argument -v/--verbosity: expected one argument
$ python3 prog.py 4 -v 1
4^2 == 16
$ python3 prog.py 4 -v 2
the square of 4 equals 16
$ python3 prog.py 4 -v 3
16
```

В этой версии программы все хорошо, кроме бага с аргументом `-v`. Давайте
исправим его, задав какие значения может принимать аргумент `-v`:

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2],
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbosity == 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity == 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)
```

И в выводе получим:

```bash
$ python3 prog.py 4 -v 3
usage: prog.py [-h] [-v {0,1,2}] square
prog.py: error: argument -v/--verbosity: invalid choice: 3 (choose from 0, 1, 2)
$ python3 prog.py 4 -h
usage: prog.py [-h] [-v {0,1,2}] square
positional arguments:
  square                display a square of a given number
optional arguments:
  -h, --help            show this help message and exit
  -v {0,1,2}, --verbosity {0,1,2}
                        increase output verbosity
```

Обратите внимание, что изменения отражены в сообщениях об ошибке и в справке.
Давайте применим другой, более распространенный подход в использовании
`--verbosity`. Он соответствует способу обработки аргумента `--verbosity`, в
CPython (проверьте вывод команды python `--help`):

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display the square of a given number")
parser.add_argument("-v", "--verbosity", action="count",
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbosity == 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity == 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)
```

В этом примере представлено ещё одно действие, `count`. Оно используется для
того, чтобы посчитать сколько раз использовался необязательный аргумент при
вызове программы.

```bash
$ python3 prog.py 4
16
$ python3 prog.py 4 -v
4^2 == 16
$ python3 prog.py 4 -vv
the square of 4 equals 16
$ python3 prog.py 4 --verbosity --verbosity
the square of 4 equals 16
$ python3 prog.py 4 -v 1
usage: prog.py [-h] [-v] square
prog.py: error: unrecognized arguments: 1
$ python3 prog.py 4 -h
usage: prog.py [-h] [-v] square
positional arguments:
  square           display a square of a given number
optional arguments:
  -h, --help       show this help message and exit
  -v, --verbosity  increase output verbosity
$ python3 prog.py 4 -vvv
16
```

- Да, сейчас это больше похоже на флаг (как в случае с `action="store_true"`),
  как в предыдущей версии скрипта.
- Ведет себя аналогично `store_true`.
- Теперь давайте продемонстрируем, что действие count нам даёт.
- Если флаг `-v` не использовался, то соотвествующая переменная будет равна
  `None` (так же как и в случае с store_true).
- Неважно какую форму флага вы использовали, длинную или короткую.
- К сожалению документация не содержит информацию об внесенных в скрипт
  изменениях, но это всегда можно исправить дополнив справку с помощью
  именованного аргумента `help`.
- Последний вывод показывает допущенную в программе ошибку.

Давайте исправим ее:

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbosity", action="count",
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
# bugfix: replace == with >=
if args.verbosity >= 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity >= 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)
```

И вот, что мы получаем:

```bash
$ python3 prog.py 4 -vvv
the square of 4 equals 16
$ python3 prog.py 4 -vvvv
the square of 4 equals 16
$ python3 prog.py 4
Traceback (most recent call last):
  File "prog.py", line 11, in <module>
    if args.verbosity >= 2:
TypeError: unorderable types: NoneType() >= int()
```

- Ошибку, которую мы хотели исправить, мы исправили.
- Третий вывод, не так хорош.

Давайте исправим этот баг:

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbosity", action="count", default=0,
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbosity >= 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity >= 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)
```

Мы просто использовали ещё один именованный аргумент `default`. Мы задали его
равным `0`, чтобы значение хранящиеся в `verbosity` могло участвовать в
операции сравнения с числами и не возникало ошибки, когда пользователь не
использовал аргумент `verbosity` (потому что если мы этого не сделаем, там
будет `None`).

И:

```bash
$ python3 prog.py 4
16
```

Даже с тем, что мы узнали до сих пор вы уже можете сделать многое, но на самом
деле это только вершина айсберга. Модуль argparse очень мощный и невозможно все
рассмотреть в этом учебнике.

Дополнительные материалы по теме:

- [Argparse — парсим аргументы и параметры командной строки с легкостью | habr](https://habr.com/post/144416/)

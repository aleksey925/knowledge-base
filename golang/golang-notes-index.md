# Golang

# Оглавление

1. [Настройка системы](#настройка-системы)
   - [Установка/удаление на MacOS](#установкаудаление-на-macos)
   - [Настройка окружения](#настройка-окружения)
   - [Управление зависимостями](#управление-зависимостями)

2. [Основы](#основы)
   - [Общие понятия](#общие-понятия)
   - [Автоматическое определение размера массива](#автоматическое-определение-размера-массива)
   - [Кросс компиляция](#кросс-компиляция)
   - [Создание shared library](#создание-shared-library)

3. [Сборщик мусора](#сборщик-мусора)
   - [Реализация GC](#реализация-gc)
   - [Логирование данных о потребляемой памяти](#логирование-данных-о-потребляемой-памяти)

4. [Реализация интересных заданий](#реализация-интересных-заданий)
   - [Подсчет сколько раз какой символ встретился в строке](#подсчет-сколько-раз-какой-символ-встретился-в-строке)

## Настройка системы

### Установка/удаление на MacOS

**Установка**

Для установки golang удобно пользоваться утилитой goenv. Она позволяет быстро и
удобно установить на компьютер различные версии компилятора. Установить ее
можно вот так.

```bash
git clone https://github.com/syndbg/goenv.git ~/.goenv
```

Добавьте в `~/.zshrc` следующие строки и перезагрузите терминал.

```bash
export PATH="$HOME/.goenv/bin:"$PATH
eval "$(goenv init -)"
export GOPATH=~/Golang
export GOBIN=${GOPATH}/bin
export PATH=${PATH}:${GOPATH}/:${GOBIN}
```

Теперь установим golang и сделаем его дефолтным для всей системы.

```bash
goenv install 1.20.3
goenv global 1.20.3
```

Проверить, что установка прошла успешно, можно следующей командой:

```bash
go version
```

Если команда выполняется без ошибок, то значит установка прошла без проблем.

**Удаление**

```bash
rm -rf `goenv root`
```

### Настройка окружения

Перед тем как начинать разработку вам нужно настроить окружение. Разработка на
go предполагает, что у вас есть 1 папка, в которой располагаются все проекты.
Структура данной папки следующая:

```
Golang
├── bin
├── pkg
└── src
```

Теперь нужно создать переменные окружения и описать их в файле `~/.zshrc` (если
это еще не было сделано во время установки).

```
export GOPATH=~/Golang
export GOBIN=${GOPATH}/bin
export PATH=${PATH}:${GOPATH}/:${GOBIN}
```

**Описание переменных окружения**

- GOROOT - указывает на папку где лежат исходные коды go, стандартная
  библиотека и т д. Это, что-то вроде JAVA_HOME. Задавать эту переменную нужно
  только в случае, если устанавливаете go из исходников.

  Раньше (до версии 1.0) эта переменная была нужна — её использовали скрипты
  сборки, равно как и GOARCH и GOOS. Но после Go 1.0 немного изменилась
  внутренняя логика работы go tool и сейчас значение GOROOT хардкодится на
  этапе сборки или инсталляции. Тоесть, go — дефолтно проинсталлированный —
  знает это значение и так. Его можно посмотреть с помощью команды:
  `go env GOROOT`

- GOPATH - указывает на папку, которая служит «рабочим пространством», то есть
  там располагаются исходники всех проектов, скомпилированные версии проектов и
  т д

  Переменная должна задаваться обязательно!

- GOBIN - указывает на папку в которую складываются скомпилированные бинарники.

### Управление зависимостями

Полезные ссылки:

- [О Go modules - тут блог](https://blog.gelin.ru/2019/08/gomod.html)
- [Введение в систему модулей Go - habr](https://habr.com/ru/post/421411/)
- [Некоторые тонкости управления зависимостями в Go - eax.me](https://eax.me/go-mod/)
- [Правда ли, что GOPATH и GOROOT больше не нужны? - habr](https://habr.com/ru/company/oleg-bunin/blog/467697/)
- [Go += управление версиями пакетов - habr](https://habr.com/ru/post/442272/)

## Основы

### Общие понятия

Файлы с кодом go, имеют расширение go. Программа на go состоят из пакетов.
Пакет можно разбить на любое количество файлов, и если все они будут иметь
одинаковое объявление пакета, с точки зрения языка Go все они будут являться
частями одного и того же пакета, как если бы все их содержимое находилось в
единственном файле.

Каждая программа должна иметь пакет main c функцией main, которая является
точкой входа в программу. Так же пакет main может ещё иметь функцию init,
которая выполняется перед функцией main.

Запуск

- `go run hello.go` — запускает программу на go;
- `go install` — компилирует файлы из текущего рабочего каталога и кладёт в
  папку bin. Для корректного выполнения команды нужно установить переменную
  окружения GOBIN;
- `go build` — делает тоже самое, что и предыдущая команда, но собранный файл
  помещается в текущую директорию.

### Автоматическое определение размера массива

Обычно при объявлении или создании массива нужно объявлять его длину.

```go
var array1 [5]int  // Объявление массива длиной 5
array2 := [2]int{1, 2}  // Объявление и инициализация массива длиной 2
```

Но если при объявлении массива мы его сразу инициализируем, то можно не
указывать точную длину, а просто написать три точки. В этом случае компилятор
сам вычислит длину массива исходя из количества заносимых элементов.

```go
func main() {
    array := [...]int{1, 2, 3, 4} // Объявление и инициализация массива
    fmt.Println(cap(array))
}
```

### Кросс-компиляция

Сначала нужно собрать toolchane для целевой платформы. Для этого переходим в
директорию с исходным кодом Go (она же $GOROOT/src, она же всегда есть у вас на
машине) и пересобираем под нужную платформу, скажем Windows/amd64:

```bash
cd $(go env GOROOT)/src
sudo GOOS=windows GOARCH=amd64 CGO_ENABLED=0 ./make.bash —no-clean
```

Скрипт make.bash — это стандартный скрипт сборки Go, которым бы вы
инсталлировали Go, если бы ставили из исходников. Он собирает, собственно, Go,
и всю стандартную библиотеку, только в этот раз — для платформы windows/amd64.

**Значения GOOS и GOARCH**

| OS            | $GOOS     |
| ------------- | --------- |
| Linux         | linux     |
| MacOS X       | darwin    |
| Windows       | windows   |
| FreeBSD       | freebsd   |
| NetBSD        | netbsd    |
| OpenBSD       | openbsd   |
| DragonFly BSD | dragonfly |
| Plan 9        | plan9     |
| Native Client | nacl      |
| Android       | android   |

| Architecture           | $GOARCH  |
| ---------------------- | -------- |
| x386                   | 386      |
| AMD64                  | amd64    |
| AMD64 с 32 разр. указ. | amd64p32 |
| ARM                    | arm      |

**Сборка проекта**

Переходим в папку проекта и собираем его командой:

```bash
GOOS=windows GOARCH=amd64 go build ./test.go
```

При выполнении данной команды может возникнуть ошибка

```
ERROR: Cannot find /Users/alex/go1.4/bin/go.
Set $GOROOT_BOOTSTRAP to a working Go tree >= Go 1.4.
```

Решить ее заданием переменной окружения GOROOT_BOOTSTRAP может не получиться. В
этом случае можно создать в папке /Users/alex/ символьную ссылку на папку
GOROOT. Для того, чтобы это исправить надо выполнить в консоли:

```bash
ln -s $(go env GOROOT) ~/go1.4
```

После этого все должно успешно собраться.

Заметка основана на [статье](https://habrahabr.ru/post/249449/).

### Создание shared library

Начиная с go 1.5.1 можно на go создавать библиотеки, для других языков
программирования.

```go
package main

import "C"

//export add
func add(left, right int) int {
   return left + right
}

func main() {}
```

Перед функциями, которые можно импортировать нужно вставлять комментарий
`export <имя функции>`.

Компиляция должна выполняться с помощью команды:

```bash
go build -buildmode=c-shared -o ./lib.so .lib.go
```

После этого скомпилированную библиотеку можно использовать в python следующим
образом:

```python
from ctypes import cdll

lib = cdll.LoadLibrary('./lib.so')
result = lib.add(2, 3)
print(result)
```

В примере выше был показан простой случай, когда функция в shared library
принимает на вход число и возвращает число. В случае, когда хочется работать со
строками, код будет немного сложнее.

```go
package main

// #include <stdlib.h>
import "C"
import (
    "fmt"
    "strings"
    "unsafe"
)

//export JoinStr
func JoinStr(sep string, str1 string, str2 string) *C.char {
    result := strings.Join([]string{str1, str2}, sep)
    fmt.Println("print from go", result)
    return C.CString(result)
}

//export FreePointer
func FreePointer(pointer *C.char) {
    C.free(unsafe.Pointer(pointer))
}

func main() {}
```

```python
import ctypes


class GoStr(ctypes.Structure):
    _fields_ = [("p", ctypes.c_char_p), ("n", ctypes.c_int64)]

    @classmethod
    def from_param(cls, value):
        """
        Converts a python string to a GoStr
        """
        value = value.encode()
        return cls(value, len(value))

    def __str__(self):
        return ctypes.string_at(self.p, self.n).decode()


library = ctypes.CDLL('./lib.so')
join_str = library.JoinStr
join_str.argtypes = [GoStr, GoStr, GoStr]
join_str.restype = ctypes.POINTER(ctypes.c_char)
free_pointer = library.FreePointer
free_pointer.argtypes = [ctypes.POINTER(ctypes.c_char)]

for i in range(1, 30):
    result_pointer = join_str('-', 'str', str(i))
    print(ctypes.c_char_p.from_buffer(result_pointer).value)
    free_pointer(result_pointer)
```

В python коде, обратите внимание на строку
`join_str.restype = ctypes.POINTER(ctypes.c_char)`. В ней указывается, что
функция `join_str` будет возвращать указатель на строку, а не просто строку.
Если мы укажем, что ожидаем просто `ctypes.c_char`, то у нас будет течь в
приложении память, так как python будет получать указатель, брать из него
данные и отбасывать укатель. В итоге память на которую узказывает указатель не
будет ни когда освобождена.

Полезные ссылки:

- [cgo - github](https://github.com/golang/go/wiki/cgo)
- [Python ctypes definition for c struct - stackoverflow](https://stackoverflow.com/questions/24640817/python-ctypes-definition-for-c-struct)
- [See Python, See Python Go, Go Python Go - heroku](https://blog.heroku.com/see_python_see_python_go_go_python_go)
- [Go from Python - github](https://github.com/jbuberel/buildmodeshared/tree/master/gofrompython)
- [BUILDING PYTHON MODULES WITH GO 1.5 - blog.filippo](https://blog.filippo.io/building-python-modules-with-go-1-5/)
- [Building shared libraries in Go: Part 1](https://www.darkcoding.net/software/building-shared-libraries-in-go-part-1/)
- [Creating shared libraries in Go](http://snowsyn.net/2016/09/11/creating-shared-libraries-in-go/)
- [ctypes return a string from c function](https://stackoverflow.com/questions/14883853/ctypes-return-a-string-from-c-function)
- [Вызов функций Go из других языков](https://habr.com/ru/company/mailru/blog/324250/)
- [Go: How to deal with Memory leaks while returning a CString? - stackoverflow](https://stackoverflow.com/questions/74990578/go-how-to-deal-with-memory-leaks-while-returning-a-cstring)
- [Pass arrays to shared libraries from python using C types - github gist](https://gist.github.com/lmammino/10ae9ad290809f172e6eb3b6957bd18c)
- [Return array in Python from shared library built in Go](https://stackoverflow.com/questions/61898877/return-array-in-python-from-shared-library-built-in-go)

## Сборщик мусора

### Реализация GC

- [Как устроен garbage collector в Go 1.9 - Андрей Дроздов, Avito](https://www.youtube.com/watch?time_continue=2&v=CX4GSErFenI)
- [Механизмы выделения памяти в Go - habr](https://habr.com/ru/company/ruvds/blog/442648/)

### Логирование данных о потребляемой памяти

```go
import (
	"runtime"
	"time"
)

...

go func() {
    for {
        var m runtime.MemStats
        runtime.ReadMemStats(&m)
        log.Printf("\nAlloc = %v\nTotalAlloc = %v\nSys = %v\nNumGC = %v\n\n", m.Alloc / 1024, m.TotalAlloc / 1024, m.Sys / 1024, m.NumGC)
        time.Sleep(5 * time.Second)
    }
}()
```

## Реализация интересных заданий

### Подсчет сколько раз какой символ встретился в строке

Создаем массив байтов, размером 256 (размер ascii таблицы), он будет
использоваться для подсчета. Индекс массива будет представлять собой код
символа, а значение в массиве указывать, сколько раз каждый из символов
встретится при переборе строки.

> Данное задание можно реализовать с использованием словарей, но вариант
> описанный в данной заметке будет работать значительно быстрее.

```go
package main

import (
   "fmt"
)

func main() {
   counter := make([]int, 256)
   str := "hello"
   for _, char := range str {
      counter[char]++
   }
   for char, count := range counter {
      if count > 0 {
         fmt.Println(string(char), ": ", count)
      }
   }
}
```

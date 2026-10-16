# Реализации интересных заданий

# Оглавление

- [Проверка на чётность с помощью поразрядного И](#проверка-на-чётность-с-помощью-поразрядного-и)
- [Получение времени последнего изменения файла](#получение-времени-последнего-изменения-файла)
- [Прервание работы функции по таймауту](#прервание-работы-функции-по-таймауту)
- [Получение из объекта функции ещё несколько таких же функций](#получение-из-объекта-функции-ещё-несколько-таких-же-функций)
- [Работа с менеджерами контекста](#работа-с-менеджерами-контекста)
- [Консольный progressbar на коленке](#консольный-progressbar-на-коленке)
- [Автоматическая запись всех атрибутов класса в верхнем регистре](#автоматическая-запись-всех-атрибутов-класса-в-верхнем-регистре)
- [Реализация глобального для всех TestCase setUp and tearDown](#реализация-глобального-для-всех-testcase-setup-and-teardown)

### Проверка на чётность с помощью поразрядного И

```python
for num in range(10000000):
    if (num & 1) == 1:
        print('Нечетное')
    else:
        print('Чётное')
```

### Получение времени последнего изменения файла

```python
import os
import datetime

def get_modif_time(filepath):
    # Получается время последнего изменения файла, в секундах.
    time = os.path.getmtime(filepath)
    # Преобразуется в удобочитаемый вид
    return datetime.datetime.fromtimestamp(time)

print(get_modif_time('temp3.py'))
```

### Прервание работы функции по таймауту

Реализация для linux

```python
import time
import signal
import functools

class ExceededError(Exception):
    pass

def timeout(seconds=10):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise ExceededError('Превышено время ожидания')

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        if seconds == 0:
            return func
        else:
            return wrapper

    return decorator


@timeout(seconds=0)
def long_running_function():
    print('start')
    time.sleep(10)
    print('end')

try:
    long_running_function()
except ExceededError as error:
    print(error)

print('Продолжаем работу')
```

Кроссплатформенная реализация

```python
import time
import functools
import threading

class ExceededError(Exception):
    pass

def timeout(seconds):
    def decorator(func):
        def run_with_timeout(*args, **kwargs):
            def target():
                """
                Обертка для выполенения функции в отдельном потоке
                """
                try:
                    result['returned'] = func(*args, **kwargs)
                    result['timeout_exceeded'] = False
                except Exception as error:
                    result['error'] = error
            result = {'returned': None, 'error': None}
            worker = threading.Thread(target=target)
            worker.daemon = True
            try:
                worker.start()
                worker.join(seconds)
            except Exception as error:
                print('Error starting thread')
                raise error

            # Проверяем результат выполнения целевой функции
            if result.get('timeout_exceeded', True):
                message = (
                    'Функция "{}" выполнялась дольше,'.format(func.__name__) +
                    ' чем было разрешено "{}" сек.'.format(seconds)
                )
                raise ExceededError(message)
            else:
                if result['error']:
                    raise result['error']
                return result['returned']
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if seconds == 0:
                return func(*args, **kwargs)
            else:
                return run_with_timeout(*args, **kwargs)
        return wrapper

    return decorator

@timeout(2)
def long_running_function():
    print('start')
    time.sleep(5)
    print('end')
    return [0.1], 1, 543

print(long_running_function())
```

### Получение из объекта функции ещё несколько таких же функций

```python
import functools
import types

def copy_func(func):
    g = types.FunctionType(func.__code__, func.__globals__, name=func.__name__,
                           argdefs=func.__defaults__,
                           closure=func.__closure__)
    g = functools.update_wrapper(g, func)
    g.__kwdefaults__ = func.__kwdefaults__
    return g

def f(arg1, arg2, arg3, kwarg1="FOO", *args, kwarg2="BAR", kwarg3="BAZ"):
    return (arg1, arg2, arg3, args, kwarg1, kwarg2, kwarg3)

f.cache = [1, 2, 3]
g = copy_func(f)
print(f(1, 2, 3, 4, 5))
print(g(1, 2, 3, 4, 5))
print(g.cache)
assert f is not g
```

Ещё можно так, но этот пример работает в самом простом варианте (на функции из
предыдущего примера это не сработает).

```python
def f(arg1, arg2, arg3):
    return arg1, arg2, arg3

g = f.__new__(f.__class__, f.__code__, f.__globals__)
print(f(1, 2, 3))
print(g(1, 2, 3))
assert f is not g
```

[Ссылка на оригинальную статью](http://stackoverflow.com/questions/13503079/how-to-create-a-copy-of-a-python-function)

### Работа с менеджерами контекста

Допишите реализацию класса Enviroment, чтобы проходили все тесты.

```python
class Environment(object):
    pass

def main():
    result = []
    env = Environment()
    try:
        result.append(env.attr)
    except AttributeError:
        result.append('ok')
    with env.extend({'attr': 23, 'foo': 'bar'}):
        result.append(env.attr)
        result.append(env.foo)
        result.append('ok')
        try:
            result.append(env.bar)
        except AttributeError:
            result.append('ok')
    try:
        result.append(env.attr)
    except AttributeError:
        result.append('ok')
    try:
        result.append(env.foo)
    except AttributeError:
        result.append('ok')
    try:
        result.append(env.bar)
    except AttributeError:
        result.append('ok')
    return result
result = main()
assert result == ['ok', 23, 'bar', 'ok', 'ok', 'ok', 'ok', 'ok']
```

Рабочая реализация

```python
class Environment(object):
    def __init__(self):
        self.temp_attr = {}
    def extend(self, attrs: dict):
        self.temp_attr.update(attrs)
        for key, value in attrs.items():
            setattr(self, key, value)
        return self

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        for i in self.temp_attr.keys():
            delattr(self, i)
        self.temp_attr.clear()
        return True if exc_type is None else False

def main():
    result = []
    env = Environment()
    try:
        result.append(env.attr)
    except AttributeError:
        result.append('ok')
    with env.extend({'attr': 23, 'foo': 'bar'}):
        result.append(env.attr)
        result.append(env.foo)
        result.append('ok')
        try:
            result.append(env.bar)
        except AttributeError:
            result.append('ok')
    try:
        result.append(env.attr)
    except AttributeError:
        result.append('ok')
    try:
        result.append(env.foo)
    except AttributeError:
        result.append('ok')
    try:
        result.append(env.bar)
    except AttributeError:
        result.append('ok')
    return result

result = main()
assert result == ['ok', 23, 'bar', 'ok', 'ok', 'ok', 'ok', 'ok']
```

### Консольный progressbar на коленке

```python
import time

count_iter = 9
for current_iter in range(1, count_iter + 1):
    made = round(current_iter / count_iter * 100)
    print('\r[{:<25}] {}%'.format('#' * round(made / 4), made), end='')
    time.sleep(.5)
else:
    print()
```

### Автоматическая запись всех атрибутов класса в верхнем регистре

```python
def upper_attribute(classname, classparents, classatributs):
    attr = ((name, value) for name, value in classatributs.items() if
            not name.startswith("__"))
    uppercase_attr = dict((name.upper(), value) for name, value in attr)
    return type(classname, classparents, uppercase_attr)

class Check(metaclass=upper_attribute):
    a = "AttrName"

print(hasattr(Check, 'a'))
print(hasattr(Check, 'A'))
```

### Реализация глобального для всех TestCase setUp and tearDown

```python
import unittest

class TestCaseMount(type):
    """
    Метакласс, который позволяет собрать классы всех TestCase в одном месте.
    """
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'test_cases'):
            cls.test_cases = []
        else:
            cls.test_cases.append(cls)

    @property
    def count_test_cases(cls) -> int:
        """
        :return: количество test case
        """
        return len(cls.test_cases)


class BaseTestCase(unittest.TestCase, metaclass=TestCaseMount):
    """
    Базовый класс для всех test case
    """
    test_cases_executed = 0

    @classmethod
    def setUpClass(cls):
        """
        Реализует глобальный для всех тестов setUp
        """
        if BaseTestCase.test_cases_executed == 0:
            drop_test_db(engine)
            create_test_db(engine)
            models.Base.metadata.create_all(engine)

        BaseTestCase.test_cases_executed += 1

    @classmethod
    def tearDownClass(cls):
        """
        Реализует глобальный для всех тестов tearDown
        """
        if BaseTestCase.test_cases_executed == cls.count_test_cases:
            drop_test_db(engine)
```

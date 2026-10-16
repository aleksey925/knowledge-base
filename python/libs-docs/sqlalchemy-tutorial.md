# SQLAlchemy

# Оглавление

1. [Общее](#общее)
   - [Обзор возможностей](#обзор-возможностей)
   - [В чем разница между flush и commit](#в-чем-разница-между-flush-и-commit)
   - [Работа с сессиями](#работа-с-сессиями)

2. [Проблемы](#проблемы)
   - [n+1 select](#n1-select)

## Общее

### Обзор возможностей

- очень подробный разбор возможностей sqlalchemy
  [локально сохраненная версия доклада](https://cloud.mail.ru/public/55Ku/5KbWy8ANZ),
  [Денис Катаев, Tinkoff.ru «SQLAlchemy: Python vs Raw SQL»](https://www.youtube.com/watch?v=jUGK-CtM-Mk)
- оптимизация
  [Ускорение SQLAlchemy для архитектурных космонавтов / Алексей Старков (Qrator Labs)](https://www.youtube.com/watch?v=flA2lEl2a0M)

### В чем разница между flush и commit

[SQLAlchemy: Какая разница между flush() и commit()? - python | Qaru](http://qaru.site/questions/26368/sqlalchemy-whats-the-difference-between-flush-and-commit)

### Работа с сессиями

[БД в SQLAlchemy: правильно работаем с сессиями | OTUS](https://otus.ru/nest/post/250/)

## Проблемы

### n+1 select

Предположим у нас есть объекты Car (строки таблицы) и у любой машины есть набор
объектов Wheel (строки таблицы). Таким образом имеем отношение 1 ко многим (Car
— Wheel).

Теперь предположим, что нам нужно обойти все машины и для каждой вывести список
ее колес. Наивное решение будет таким:

```sql
SELECT * FROM Cars;
```

И потом для каждой машины выполнить:

```sql
SELECT * FROM Wheel WHERE CarId = ?
```

Таким образом у нас есть 1 select для выборки всех машин и N дополнительных
selects (N это общее колличество машин).

Более правильным решением будет получить все колеса и выполнить поиск в памяти.

```sql
SELECT * FROM Wheel;
```

Это уменьшает колличество обращений к базе от N + 1, до 2.

**Пример решения этой проблемы в SQLAlchemy**

Модель

```python
class OrderItem(Base):
    id = Column(Integer, primary_key=True)
    order = many_to_one('Order')
    product = many_to_one('Product')
    quantity = Column(Integer)

class Order(Base):
    ...
    def update_stock(self):
        for item in self.items:
            item.product.stock -= item.quantity
```

Большинство orm используют lazy loading. Когда первый раз используется
отношение, выдается SQL запрос для загрузки нужных данных. В примере выше
используется oreder.items, который вызывает исполнение SQL запроса, затем
каждый вызов item.product выполняет очередной запрос к БД. Из-за вызова
item.product в цикле создается большое количество запросов к БД и это может к
снижению производительности. Это называется пробелема N + 1 select.

SQLAlchemy имеет решение: безотложенная загрузка. Когда мы загружаем объект
Order, можно указать ORM какие отношения мы будем использовать и тогда все
данные загрузятся в 1 запросе. Для этого используется следующий синтаксис.

```python
session.query(Order).options(joinedload_all('items.product')).get(order_id)
```

[Ссылка на оригинальную статью](http://pajhome.org.uk/blog/10_reasons_to_love_sqlalchemy.html)

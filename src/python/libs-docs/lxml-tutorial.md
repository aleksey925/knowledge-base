# Tutorial lxml

lxml - библиотека для работы с XML и HTML, она основана сишных библиотеках
libxml2 и libxslt. Она совмещает в себе высокую скорость работы, богатый
функционал и простоту использования при обработке XML и HTML.

### XML

Начнём с разбора данных в XML. Сначала импортируем библиотеку и проинициализуем
тестовые строки.

```python
from lxml import html, etree
example_xml = """
<notes>
     <note>
         <to>Timmy</to>
         <from>Rich</from>
         <heading>Reminder</heading>
         <body>Remeber the concert tickets.</body>
     </note>
     <note>
         <to>Eric</to>
         <from>Josh</from>
         <heading>Ride Plans</heading>
        <body>Meet at the gas station on the corner of Diffley and 13 at 6:00pm.</body>
    </note>
</notes>
"""
```

Структура двух определённых заметок (notes) с сообщениями и некоторой
дополнительной информацией. Сейчас мы попробуем получить некотрую информацию из
этой разметки.

Сначала с помощью метода `fromstring` мы загрузим данные в новый объект.

```python
notes = etree.fromstring(example_xml)
```

Теперь в цикле обойдём все дочерние элементы notes.

```python
for note in notes.getchildren():
   print(note.tag)
```

После выполнения этого кода в консоли мы увидим следующие строки:

```
note
note
```

Сохраним в отдельную переменную первый дочерний элемент notes для дальнейшего
исследования.

```python
note = notes.getchildren()[0]
```

Выведем данные содержащиеся в полях полученного нами элемента.

```python
for field in note.iterchildren():
    print('%s: %s' % (field.tag, field.text))
```

После выполнения этого кода в консоли мы увидим следующие строки:

```
to: Timmy
from: Rich
heading: Reminder
body: Remeber the concert tickets.
```

Из заметок очень легко можно извлечь имена людей, которым она предназначается.

```python
for field in notes.findall('.//to'):
    print('Note to: %s' % field.text)
```

После выполнения этого кода в консоли мы увидим следующие строки:

```
Note to: Timmy
Note to: Eric
```

### HTML

Теперь когда мы научились извлекать данные из XML, попробуем поработать с HTML.
Начнём опять с определения тестовых строк, с которыми будем работать.

```python
example_html = """
    <html>
        <head>
            <title>Example HTML Title</title>
        </head>
        <body>
            <h1 class="big_heading">LXML Example HTML</h1>
            <div class="all_items">
                <p class="item">
                    This is the first paragrah.
                </p>
                <p class="item">
                    This is the second paragraph.
                    <img src='/fakeurl/to_fake_img.png' />
                </p>
            </div>
        </body>
    </html>
"""
```

Так же как и в случае с XML, нам нужно сначала создать объект с помощью
которого мы будем парсить HTML. Для этого нужно использовать функцию
`document_fromstring`.

```python
doc = html.document_fromstring(example_html)
```

Теперь мы можем начать извлекать данные. Для поиска нужных элементов мы можем
использовать CSS селекторы.

Получим заголовок страницы:

```python
title = doc.cssselect('head title')[0]
print(title.text)
```

Теперь попробуем извлечь все элементы списка:

```python
items = doc.cssselect('div.all_items .item')
for item in items:
    print(item.text.strip())
```

После выполнения этого кода в консоли мы увидим следующие строки:

```
This is the first paragrah.
This is the second paragraph.
```

Здесь мы продемонстрировали примеры того, на сколько просто использовать
библиотеку lxml. Есть много дополнительных функций, к которым мы даже близко не
подобрались, мы всего лишь извлекли содержимое некоторых тегов.

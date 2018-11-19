Computer Science
================

# Оглавление

- [Почему доступ по индексу к любому элементу массива происходит за O(1)](#Почему-доступ-по-индексу-к-любому-элементу-массива-происходит-за-O(1))


<a name='Почему-доступ-по-индексу-к-любому-элементу-массива-происходит-за-O(1)'></a>
### Почему доступ по индексу к любому элементу массива происходит за O(1)

Доступ по индексу к любому элементу массива за константное время обеспечивается
несколькими особенностями массива:

- массив это непрерывная область памяти;
- массив хранит данные одного типа;
- массив имеет фиксированный размер.

За счет этих особенностей мы знаем размер каждого элемента массива и можем
обратиться к любому из них при помощи смещения (offset), которое вычисляется 
по формуле `размер елемента * индекс`.
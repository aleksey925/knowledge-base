RabbitMQ
========

# Оглавление

1. [Producer throttling](#Producer-throttling)


<a name='Producer-throttling'></a>
## Producer throttling

В больших системах, где сервисы обмениваются данными через брокер сообщений может возникать проблема со скоростью 
обработки сообщений из очереди. В этом случае размер очереди может очень быстро увеличиваться и может достигать 
размеров, когда это может начинать негативно влиять на производительность всего брокера. Эта ситуация может быть большой 
проблемой, когда с брокером взаимодействует вся система или большая её часть. В связи с этим очень важно иметь 
настроенный мониторинг, который будет оповещать о наличии проблем и очень желательно интегрировать в consumers/producers 
механизм позволяющий в автоматическом режиме разрешать такие проблемы, чтобы одновременно не легла вся система.
Есть несколько способов реализовать подобное. 

Первый и самый простой это интеграция блоков, которые будут после отправки каждого сообщения тормозить producer на 
заданное количество времени (то есть будут просто вызывать `time.sleep()` с определенным значением). При таком подходе 
довольно важно иметь возможность в realtime обновлять значение на основании которого будет происходить "засыпание" 
producer. Это нужно, чтобы в критический момент кто-то из службы сопровождения мог замедлить публикацию новых сообщений 
и consumer успел обработать сообщения из очереди. Этот способ очень простой и действенный, но он требует постоянного 
сопровождения, особенно если в разное время producer генерирует разную нагрузку на систему. В этом как раз кроется 
главный минус этого подхода.

Второй подход более автоматизированный и позволяет системе работать в автоматическом режиме, без внешних вмешательств.
Он основан на внутреннем механизме rabbitmq, который позволяет объявить максимальный размер очереди и определить 
поведение брокера при попытке положить новое сообщение в переполненную очередь. Идея использования данного механизма 
заключается в следующем:

- создаем очередь и указываем ее максимальный размер
- определяем, что при попытке отправить в переполненную очередь новое сообщение оно должно отбрасываться (реджектится)
- в producer включаем подтверждение отправки сообщения (`publisher confirms`). Это даст нам возможность понять удалось
  ли успешно положить новое сообщение в очередь.
- реализовываем в producer логику обработки ошибки говорящей о том, что сообщение не удалось положить в очередь, где при
  возникновении такой ситуации мы засыпаем на некоторое время и после снова пытаемся отправить нужное сообщение. Если 
  в следующий раз опять возникла ошибка, то опять повторяем ранее описанную логику и так до тех пор, пока у нас не 
  закончится разрешенное кол-во попыток. Если разрешенное кол-во попыток, кончилось, а опубликовать сообщения так и не 
  получилось, то нужно начинать бить тревогу (писать в лог информацию о критической ошибке, которая должна быть в свою 
  очередь подхвачена системой мониторинга).

Вот пример producer, который используя аргументы `x-max-length` и `x-overflow` реализовывает логику работа rabbitmq, 
которая была описана ранее. В данном примере для определения `max-length` и `overflow` используется параметры при 
создании очереди. Важно заметить, что это не единственный способ, можно сделать то же самое и через политики. Это 
описано в оф. документации, ссылка на которую прикреплена к заметке.

```python
import asyncio
import logging

import aio_pika
import aiormq

MAX_QUEUE_LEN = 3

logger = logging.getLogger(__name__)


async def main():
    connection = await aio_pika.connect_robust('amqp://admin:admin@127.0.0.1/', loop=asyncio.get_event_loop())

    async with connection:
        queue_name = 'test_queue'
        routing_key = 'test_queue'

        channel = await connection.channel(publisher_confirms=True)
        exchange = await channel.declare_exchange('direct')
        queue = await channel.declare_queue(
            queue_name,
            durable=True,
            arguments={'x-max-length': MAX_QUEUE_LEN, 'x-overflow': 'reject-publish'}
        )

        await queue.bind(exchange, routing_key)

        for i in range(MAX_QUEUE_LEN + 1):
            msg = f'Hello world {i}'
            try:
                await exchange.publish(aio_pika.Message(msg.encode()), routing_key)
                logger.debug(f'Сообщение "%s", отправлено', msg)
            except aiormq.exceptions.DeliveryError:
                # Здесь должна быть реализована система ретраев
                logger.error(f'Очередь переполнена, невозможно отправить сообщение: "%s"', msg)


if __name__ == '__main__':
    asyncio.run(main())
```


Полезные ссылки:

[Queue Length Limit - RabbitMQ](https://www.rabbitmq.com/maxlength.html#definition-using-x-args)
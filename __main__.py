import asyncio
import logging.config

from trade.managers import BarsManager
from connector.managers import Interval
from settings import LOGGING_CONFIG
from connector.events import Dispatcher, EventTypes


#Настройка логгера
logging.config.dictConfig(LOGGING_CONFIG)


async def listen_quik(dispatcher):
    await dispatcher.listen()
    asyncio.ensure_future(listen_quik(dispatcher))


def printer(response):
    print(response)


def populate_tasks():
    dispatcher = Dispatcher()
    dispatcher.subscribe(EventTypes.ON_QUOTE, callback=printer)

    mgr = BarsManager(class_code='QJSIM', sec_code='SBER', interval=Interval.M1)
    # asyncio.ensure_future(mgr.subscribe())

    asyncio.ensure_future(listen_quik(dispatcher))


def add_task(task):
    asyncio.ensure_future(task)


def start_event_loop():
    loop = asyncio.get_event_loop()
    try:
        populate_tasks()
        loop.run_forever()
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


def main():
    start_event_loop()


if __name__ == '__main__':
    main()



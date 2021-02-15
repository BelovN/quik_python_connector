import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable, List
from .connection import TypeConnection, QConnector, QConnection
from qlua.rpc import qlua_events_pb2, qlua_structures_pb2
from .utils import singleton


class EventTypes:
    EVENT_TYPE_UNKNOWN = str(qlua_events_pb2.EVENT_TYPE_UNKNOWN).encode('ascii')
    PUBLISHER_ONLINE = str(qlua_events_pb2.PUBLISHER_ONLINE).encode('ascii')
    ON_STOP = str(qlua_events_pb2.ON_STOP).encode('ascii')
    ON_CLOSE = str(qlua_events_pb2.ON_CLOSE).encode('ascii')
    ON_CONNECTED = str(qlua_events_pb2.ON_CONNECTED).encode('ascii')
    ON_DISCONNECTED = str(qlua_events_pb2.ON_DISCONNECTED).encode('ascii')
    ON_FIRM = str(qlua_events_pb2.ON_FIRM).encode('ascii')
    ON_ALL_TRADE = str(qlua_events_pb2.ON_ALL_TRADE).encode('ascii')
    ON_TRADE = str(qlua_events_pb2.ON_TRADE).encode('ascii')
    ON_ORDER = str(qlua_events_pb2.ON_ORDER).encode('ascii')
    ON_ACCOUNT_BALANCE = str(qlua_events_pb2.ON_ACCOUNT_BALANCE).encode('ascii')
    ON_FUTURES_LIMIT_CHANGE = str(qlua_events_pb2.ON_FUTURES_LIMIT_CHANGE).encode('ascii')
    ON_FUTURES_LIMIT_DELETE = str(qlua_events_pb2.ON_FUTURES_LIMIT_DELETE).encode('ascii')
    ON_FUTURES_CLIENT_HOLDING = str(qlua_events_pb2.ON_FUTURES_CLIENT_HOLDING).encode('ascii')
    ON_MONEY_LIMIT = str(qlua_events_pb2.ON_MONEY_LIMIT).encode('ascii')
    ON_MONEY_LIMIT_DELETE = str(qlua_events_pb2.ON_MONEY_LIMIT_DELETE).encode('ascii')
    ON_DEPO_LIMIT = str(qlua_events_pb2.ON_DEPO_LIMIT).encode('ascii')
    ON_DEPO_LIMIT_DELETE = str(qlua_events_pb2.ON_DEPO_LIMIT_DELETE).encode('ascii')
    ON_ACCOUNT_POSITION = str(qlua_events_pb2.ON_ACCOUNT_POSITION).encode('ascii')
    ON_NEG_DEAL = str(qlua_events_pb2.ON_NEG_DEAL).encode('ascii')
    ON_NEG_TRADE = str(qlua_events_pb2.ON_NEG_TRADE).encode('ascii')
    ON_STOP_ORDER = str(qlua_events_pb2.ON_STOP_ORDER).encode('ascii')
    ON_TRANS_REPLY = str(qlua_events_pb2.ON_TRANS_REPLY).encode('ascii')
    ON_PARAM = str(qlua_events_pb2.ON_PARAM).encode('ascii')
    ON_QUOTE = str(qlua_events_pb2.ON_QUOTE).encode('ascii')
    ON_CLEAN_UP = str(qlua_events_pb2.ON_CLEAN_UP).encode('ascii')
    ON_DATA_SOURCE_UPDATE = str(qlua_events_pb2.ON_DATA_SOURCE_UPDATE).encode('ascii')


@dataclass
class Event:
    data_type: Any
    is_subscribed: bool
    callbacks: List[Callable] = field(default_factory=list)


EVENTS = {
    EventTypes.EVENT_TYPE_UNKNOWN: None,
    EventTypes.ON_STOP: Event(
        data_type=qlua_structures_pb2.StopEventInfo,
        is_subscribed=False,
        callbacks=[],
    ),
    EventTypes.ON_CLOSE: Event(
        data_type=qlua_structures_pb2.StopEventInfo,
        is_subscribed=False,
        callbacks=[],
    ),
    EventTypes.ON_CONNECTED: Event(
        data_type=qlua_structures_pb2.ConnectedEventInfo,
        is_subscribed=False,
        callbacks=[],
    ),
    EventTypes.ON_DISCONNECTED: Event(
        data_type=None,
        is_subscribed=False,
        callbacks=[],
    ),
    EventTypes.ON_FIRM: Event(
        data_type=qlua_structures_pb2.Firm,
        is_subscribed=False,
        callbacks=[],
    ),
    EventTypes.ON_ALL_TRADE: Event(
        data_type=qlua_structures_pb2.AllTrade,
        is_subscribed=False,
        callbacks=[],
    ),
    EventTypes.ON_TRADE: Event(
        data_type=qlua_structures_pb2.Trade,
        is_subscribed=False,
        callbacks=[],
    ),
    EventTypes.ON_ORDER: Event(
        data_type=qlua_structures_pb2.Order,
        is_subscribed=False,
        callbacks=[],
    ),
    EventTypes.ON_ACCOUNT_BALANCE: Event(
        data_type=qlua_structures_pb2.AccountBalance,
        is_subscribed=False,
        callbacks=[],
    ),
    EventTypes.ON_FUTURES_LIMIT_CHANGE: Event(
        data_type=qlua_structures_pb2.FuturesLimit,
        is_subscribed=False,
        callbacks=[],
    ),
    EventTypes.ON_FUTURES_LIMIT_DELETE: Event(
        data_type=qlua_structures_pb2.FuturesLimitDelete,
        is_subscribed=False,
        callbacks=[],
    ),
    EventTypes.ON_FUTURES_CLIENT_HOLDING: Event(
        data_type=qlua_structures_pb2.FuturesClientHolding,
        is_subscribed=False,
        callbacks=[],
    ),
    EventTypes.ON_MONEY_LIMIT: Event(
        data_type=qlua_structures_pb2.MoneyLimit,
        is_subscribed=False,
        callbacks=[],
    ),
    EventTypes.ON_MONEY_LIMIT_DELETE: Event(
        data_type=qlua_structures_pb2.MoneyLimitDelete,
        is_subscribed=False,
        callbacks=[],
    ),
    EventTypes.ON_DEPO_LIMIT: Event(
        data_type=qlua_structures_pb2.DepoLimit,
        is_subscribed=False,
        callbacks=[],
    ),
    EventTypes.ON_DEPO_LIMIT_DELETE: Event(
        data_type=qlua_structures_pb2.DepoLimitDelete,
        is_subscribed=False,
        callbacks=[],
    ),
    EventTypes.ON_ACCOUNT_POSITION: Event(
        data_type=qlua_structures_pb2.AccountPosition,
        is_subscribed=False,
        callbacks=[],
    ),
    EventTypes.ON_NEG_DEAL: Event(
        data_type=qlua_structures_pb2.NegDeal,
        is_subscribed=False,
        callbacks=[],
    ),
    EventTypes.ON_NEG_TRADE: Event(
        data_type=qlua_structures_pb2.NegTrade,
        is_subscribed=False,
        callbacks=[],
    ),
    EventTypes.ON_STOP_ORDER: Event(
        data_type=qlua_structures_pb2.StopOrder,
        is_subscribed=False,
        callbacks=[],
    ),
    EventTypes.ON_TRANS_REPLY: Event(
        data_type=qlua_structures_pb2.Transaction,
        is_subscribed=False,
        callbacks=[],
    ),
    EventTypes.ON_PARAM: Event(
        data_type=qlua_structures_pb2.ParamEventInfo,
        is_subscribed=False,
        callbacks=[],
    ),
    EventTypes.ON_QUOTE: Event(
        data_type=qlua_structures_pb2.QuoteEventInfo,
        is_subscribed=False,
        callbacks=[],
    ),
    EventTypes.ON_CLEAN_UP: Event(
        data_type=None,
        is_subscribed=False,
        callbacks=[],
    ),
    EventTypes.ON_DATA_SOURCE_UPDATE: Event(
        data_type=qlua_structures_pb2.DataSourceUpdateInfo,
        is_subscribed=False,
        callbacks=[],
    ),
}


@singleton
class Dispatcher:
    """Класс для работы с callback функциями с помощью PUB/SUB"""

    def __init__(self):
        self.event_handler = EventHandler()
        connection = QConnection(_type=TypeConnection.SUB)
        self.connector = QConnector(connection=connection)

    async def listen(self) -> None:
        while True:
            message = await self.connector.listen()
            await self.event_handler.handle(message)

    def subscribe(self, event_type: EventTypes = None, callback: Callable = None) -> None:
        event = EVENTS[event_type]
        if callback is not None:
            event.callbacks.append(callback)
        if not event.is_subscribed:
            event.is_subscribed = True
            self.connector.qconnection.subscribe(event_type)


class EventHandler:
    MSG_TYPE = 0
    MSG_DATA = 1

    @staticmethod
    async def add_callbacks(event: Event, response) -> None:
        for cb in event.callbacks:
            cb(response)

    async def handle(self, message: Any) -> None:
        message_type = message[self.MSG_TYPE]
        message_data = message[self.MSG_DATA]

        event = EVENTS[message_type]
        response = None
        if event.data_type is not None:
            response = event.data_type()
            response.ParseFromString(message_data)

        await self.add_callbacks(event, response)

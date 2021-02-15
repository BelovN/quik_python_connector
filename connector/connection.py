import asyncio
import sys
import time
import zmq
import zmq.asyncio

from enum import Enum
from google.protobuf.internal.containers import BaseContainer, MutableMapping
from qlua.rpc import RPC_pb2
from .settings import USERS


# Для корректной работы zmq.asyncio с win на Python 3.8
if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class TypeConnection(Enum):
    """Тип соединения клиента"""
    REQ = 1 # Отправка запросов Request/Response
    SUB = 2 # Подписка на события Publisher/Subscriber


class QConnection:
    """Соединение с QUIK"""
    # TODO: Must be async
    is_open: bool = False
    is_busy = False

    def __init__(self, _type: TypeConnection):
        self.ctx = zmq.asyncio.Context.instance()
        user = USERS[_type.name]

        self.socket = self.ctx.socket(getattr(zmq, _type.name))
        self.socket.plain_username = user['username'].encode('utf8')
        self.socket.plain_password = user['password'].encode('utf8')
        self.url = user['url']

        self.listening = False
        self.sending = False

    def open(self) -> None:
        self.socket.connect(self.url)
        self.is_open = True

    async def send(self, data: bytes) -> None:
        self.sending = True
        await self.socket.send(data)
        self.sending = False

    async def listen(self) -> bytes:
        self.listening = True
        response = await self.socket.recv_multipart()
        # await asyncio.sleep(0.5)
        self.listening = False
        return response

    def subscribe(self, event):
        self.socket.subscribe(event)

    def close(self) -> None:
        self.socket.close()
        self.ctx.destroy()
        self.is_open = False

    def __del__(self):
        if self.is_open:
            self.close()


class ProtobufED:
    """Статический класс для кодирования и декодирования в Protocol Buffers"""

    @staticmethod
    def _fill_args(_args, **kwargs) -> None:
        for key, value in kwargs.items():
            attr = getattr(_args, key)
            if isinstance(attr, MutableMapping): # For map field
                attr.update(value)
            elif isinstance(attr, BaseContainer): # For repeated field
                attr.extend(value)
            else:
                setattr(_args, key, value)

    @classmethod
    def _encode_args(cls, _function, **kwargs) -> bytes:
        _args = _function.Args()
        cls._fill_args(_args=_args, **kwargs)
        encoded_args = _args.SerializeToString()
        return encoded_args

    @staticmethod
    def _encode_request(encoded_args: bytes, function_type: str):
        request = RPC_pb2.Request()
        request.type = getattr(RPC_pb2, function_type)
        request.args = encoded_args
        encoded_request = request.SerializeToString()
        return encoded_request

    @classmethod
    def encode(cls, _function, function_type, **kwargs) -> bytes:
        encoded_args = cls._encode_args(_function=_function, **kwargs)
        encoded_request = cls._encode_request(function_type=function_type,
                                              encoded_args=encoded_args)
        return encoded_request

    @staticmethod
    def _decode_response(_response):
        response = RPC_pb2.Response()
        response.ParseFromString(_response)
        return response

    @staticmethod
    def _decode_args(_function, _decoded_response):
        _result = _function.Result()
        _result.ParseFromString(_decoded_response)
        return _result

    @classmethod
    def decode(cls, response, _function):
        decoded_response = cls._decode_response(_response=response)
        decoded_args = cls._decode_args(_function=_function,
                                        _decoded_response=decoded_response.result)
        return decoded_args


class QConnector:
    qconnection: QConnection

    def __init__(self, connection):
        self.qconnection = connection
        self.qconnection.open()

    async def run_on_quik(self, _function, function_type, **kwargs):
        encoded_request = ProtobufED.encode(_function=_function, function_type=function_type, **kwargs)

        await self.send(data=encoded_request)

        time.sleep(0.1) # - Для того, чтобы QUIK успел ответить

        response = await self.listen()

        if isinstance(response, list):
            response = response[0]

        decoded_response = ProtobufED.decode(response=response, _function=_function)

        return decoded_response

    async def send(self, data):
        while self.qconnection.listening or self.qconnection.sending:
            await asyncio.sleep(0.01)
        await self.qconnection.send(data=data)

    async def listen(self):
        while self.qconnection.listening or self.qconnection.sending:
            await asyncio.sleep(0.01)
        response = await self.qconnection.listen()
        return response

    async def subscribe(self, event):
        await self.qconnection.subscribe(event)

    def __del__(self):
        self.qconnection.close()

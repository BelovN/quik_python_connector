import pytest
import zmq

from connection import QConnection, ProtobufED, QConnector
from managers import Interval
from qlua import rpc
from qlua.rpc import datasource as ds

# ----------------- TEST QConnection -----------------

@pytest.fixture
def qconnection():

    def sock_send(data):
        print('SENDED')

    def sock_recv():
        data = 'some string'.encode('utf8')
        print('RECEIVED')
        return data

    preset_connection = QConnection()
    preset_connection.socket = type('socket', (object,), {})()

    setattr(preset_connection.socket, 'connect', lambda url: None)
    setattr(preset_connection.socket, 'send', sock_send)
    setattr(preset_connection.socket, 'recv', sock_recv)
    setattr(preset_connection.socket, 'close', lambda: None)

    yield preset_connection

    del preset_connection


def test_qconnection_singleton(qconnection):
    _qconnection = QConnection()
    assert id(_qconnection) == id(qconnection)


def test_qconnection_constructor(qconnection):
    assert qconnection.is_open == False
    assert qconnection.ctx is not None
    assert qconnection.socket is not None


def test_qconnection_open(qconnection):
    qconnection.open(url='url', user='user', password='password')
    assert qconnection.is_open == True


def test_qconnection_send(qconnection):
    data = 'some string'.encode('utf8')
    qconnection.send(data)


def test_qconnection_listen(qconnection):
    data = qconnection.listen()
    print(data)


def test_qconnection_close(qconnection):
    qconnection.close()
    assert not qconnection.is_open


@pytest.mark.parametrize('_function', [ds.CreateDataSource_pb2])
@pytest.mark.parametrize('function_type', ['CREATE_DATA_SOURCE'])
@pytest.mark.parametrize('kwargs', [{'class_code': 'SBER', 'sec_code': 'SJNQ', 'interval': Interval.TICK},
                                    {'class_code': 'GAZP', 'sec_code': 'ASD', 'interval': Interval.UNDEFINED},
                                    {'class_code': 'CLASS CODE', 'sec_code': 'SEC CODE', 'interval': Interval.M1},
                                    {'class_code': '', 'sec_code': '', 'interval': 123123},
                                    {'sec_code': 'SEC CODE', 'interval': Interval.M1},
                                    {'interval': Interval.M1},
                                    {}])
def test_encode(_function, function_type, kwargs):
    encoded_data = ProtobufED.encode(_function=_function, function_type=function_type, **kwargs)
    assert isinstance(encoded_data, (bytes, bytearray))


@pytest.mark.parametrize('_function', [ds.CreateDataSource_pb2])
@pytest.mark.parametrize('function_type', ['CREATE_DATA_SOURCE'])
@pytest.mark.parametrize('kwargs', [{'class_code': None, 'sec_code': 'SJNQ', 'interval': Interval.TICK},
                                    {'class_code': 'GAZP', 'sec_code': 123, 'interval': Interval.UNDEFINED},
                                    {'class_code': 'CLASS CODE', 'sec_code': 'SEC CODE', 'interval': [1, 2, 3]}])
def test_encode_fails(_function, function_type, kwargs):
    with pytest.raises(TypeError):
        encoded_data = ProtobufED.encode(_function=_function, function_type=function_type, **kwargs)


@pytest.fixture
def preset_functions():
    _function = ds.CreateDataSource_pb2
    function_type = 'CREATE_DATA_SOURCE'
    kwargs = {
        'class_code': 'GAZP',
        'sec_code': 'SQWFG',
        'interval': Interval.M1,
    }
    return _function, function_type, kwargs


def test_encode_decode_args(preset_functions):
    _function, function_type, kwargs = preset_functions

    encoded_args = ProtobufED._encode_args(_function=_function, **kwargs)
    decoded_args = ProtobufED._decode_args(_function=_function, _decoded_response=encoded_args)

    assert hasattr(decoded_args, 'datasource_uuid')


@pytest.mark.parametrize('function_type', ['', 'asdasdasd'])
def test_encode_fails(preset_functions, function_type):
    _function, _, kwargs = preset_functions
    with pytest.raises(AttributeError):
        encoded_data = ProtobufED.encode(_function=_function, function_type=function_type, **kwargs)


def test_encode_decode(preset_functions):
    _function, function_type, kwargs = preset_functions
    encoded_data = ProtobufED.encode(_function=_function, function_type=function_type, **kwargs)
    decoded_data = ProtobufED.decode(_function=_function, response=encoded_data)
    assert encoded_data
    assert decoded_data


# ----------------- END TEST ProtobufZMQ -----------------


# ----------------- END TEST ProtobufZMQ -----------------


@pytest.fixture
def preset_qconnector():
    qconnector = QConnector()
    return qconnector


def test_qconnector_singleton(preset_qconnector):
    qconnector = QConnector()
    assert id(preset_qconnector) == id(qconnector)


# ----------------- END TEST ProtobufZMQ -----------------

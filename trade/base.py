from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from .utils import TemplateList


@dataclass
class Bar:
    open: float
    high: float
    low: float
    close: float
    dtime: datetime
    volume: int
    index: int

    def __post_init__(self):
        # TODO: Check attributes types
        values = [self.open, self.high, self.low, self.close]

        if min(values) != self.low:
            raise ValueError('Attribute "low" is not a lowest value')

        if max(values) != self.high:
            raise ValueError('Attribute "high" is not a highest value')

        if self.volume <= 0:
            raise ValueError('Attribute "value" must be greater than 0!')

    @staticmethod
    def _convert_time(time):
        dtime = datetime(time.year, time.month, time.day, time.hour, time.min, time.sec)
        return dtime

    @staticmethod
    def _convert_from_quik(response):
        dtime = Bar._convert_time(response.time)
        args_dict = {
            'open': float(response.open),
            'high': float(response.high),
            'low': float(response.low),
            'close': float(response.close),
            'volume': int(float(response.volume)),
            'index': int(response.index),
            'dtime': dtime,
        }
        return args_dict

    @staticmethod
    def from_quik(response):
        args_dict = Bar._convert_from_quik(response)
        bar = Bar(**args_dict)
        return bar

    def update_from_quik(self, response):
        args_dict = Bar._convert_from_quik(response)
        self.close = args_dict['close']
        self.high = args_dict['high']
        self.low = args_dict['low']
        self.volume = args_dict['volume']


@dataclass
class BarsList(TemplateList):
    """Базовый класс списка свечей"""
    type_value = Bar
    sec_code: str
    class_code: str
    interval: int

    def __post_init__(self):
        self._items = []
        if self.interval <= 0:
            raise ValueError('Attribute "interval" must be greater than 0!')

    def copy(self):
        new_instance = BarsList(sec_code=self.sec_code, class_code=self.class_code, interval=self.interval)
        new_instance._items = self._items
        return new_instance


class Transaction:
    CLASSCODE: str
    SECCODE: str
    ACTION: str
    OPERATION: str = None
    QUANTITY: str = None
    PRICE: str = None
    FIRM_ID: str = None
    ACCOUNT: str = None
    CLIENT_CODE: str = None
    TYPE: str = None
    MARKET_MAKER_ORDER: str = None
    EXECUTION_CONDITION: str = None
    REPOVALUE: str = None
    START_DISCOUNT: str = None
    LOWER_DISCOUNT: str = None
    UPPER_DISCOUNT: str = None
    STOPPRICE: str = None
    STOP_ORDER_KIND: str = None
    STOPPRICE_CLASSCODE: str = None
    STOPPRICE_SECCODE: str = None
    STOPPRICE_CONDITION: str = None
    LINKED_ORDER_PRICE: str = None
    EXPIRY_DATE: str = None
    STOPPRICE2: str = None
    CONDITION: str = None
    MARKET_STOP_LIMIT: str = None
    MARKET_TAKE_PROFIT: str = None
    IS_ACTIVE_IN_TIME: str = None
    ACTIVE_FROM_TIME: str = None
    ACTIVE_TO_TIME: str = None
    PARTNER: str = None
    ORDER_KEY: str = None
    STOP_ORDER_KEY: str = None
    TRANS_ID: str = None
    SETTLE_CODE: str = None
    PRICE2: str = None
    REPOTERM: str = None
    REPORATE: str = None
    BLOCK_SECURITIES: str = None
    REFUNDRATE: str = None
    COMMENT: str = None
    LARGE_TRADE: str = None
    CURR_CODE: str = None
    FOR_ACCOUNT: str = None
    SETTLE_DATE: str = None
    KILL_IF_LINKED_ORDER_PARTLY_FILLED: str = None
    OFFSET: str = None
    OFFSET_UNITS: str = None
    SPREAD: str = None
    SPREAD_UNITS: str = None
    BASE_ORDER_KEY: str = None
    USE_BASE_ORDER_BALANCE: str = None
    ACTIVATE_IF_BASE_ORDER_PARTLY_FILLED: str = None
    BASE_CONTRACT: str = None
    MODE: str = None
    FIRST_ORDER_NUMBER: str = None
    FIRST_ORDER_NEW_QUANTITY: str = None
    FIRST_ORDER_NEW_PRICE: str = None
    SECOND_ORDER_NUMBER: str = None
    SECOND_ORDER_NEW_QUANTITY: str = None
    SECOND_ORDER_NEW_PRICE: str = None
    KILL_ACTIVE_ORDERS: str = None
    NEG_TRADE_OPERATION: str = None
    NEG_TRADE_NUMBER: str = None
    VOLUMEMN: str = None
    VOLUMEPL: str = None
    KFL: str = None
    KGO: str = None
    USE_KGO: str = None
    CHECK_LIMITS: str = None
    MATCHREF: str = None
    CORRECTION: str = None

    def __check_required_is_not_empty(self, required_values):
        error_message = ''
        for value in required_values:
            attribute = getattr(self, value, None)
            if attribute == '' or attribute is None:
                error_message += value + ' must not be empty or None! \n'

        return error_message

    def __check_all_attributes_is_string(self, required_values):
        error_message = ''
        for key_attr, value_attr in self.__dict__.items():
            if not (isinstance(value_attr, str) or (value_attr is None and key_attr not in required_values)):
                error_message += key_attr + ' must be string! \n'

        return error_message

    def __check_errors(self, required_values):
        error_message = ''

        error_message += self.__check_required_is_not_empty(required_values)
        error_message += self.__check_all_attributes_is_string(required_values)

        if error_message:
            raise ValueError(error_message)

    def __post_init__(self):
        required_values = [
            'CLASSCODE',
            'SECCODE',
            'ACTION',
            'OPERATION',
            'QUANTITY',
            'PRICE',
            'TYPE',
            'CLIENT_CODE',
        ]
        self.__check_errors(required_values)

    def to_dict(self):
        result = {}
        attrs = [
            'CLASSCODE', 'OPERATION', 'SECCODE', 'ACTION', 'OPERATION', 'QUANTITY', 'PRICE', 'FIRM_ID', 'ACCOUNT', 'CLIENT_CODE',
            'TYPE', 'MARKET_MAKER_ORDER', 'EXECUTION_CONDITION', 'REPOVALUE', 'START_DISCOUNT', 'LOWER_DISCOUNT',
            'UPPER_DISCOUNT', 'STOPPRICE', 'STOP_ORDER_KIND', 'STOPPRICE_CLASSCODE', 'STOPPRICE_SECCODE', 'CONDITION',
            'STOPPRICE_CONDITION', 'LINKED_ORDER_PRICE', 'EXPIRY_DATE', 'STOPPRICE2', 'MARKET_STOP_LIMIT',
            'MARKET_TAKE_PROFIT', 'IS_ACTIVE_IN_TIME', 'ACTIVE_FROM_TIME', 'ACTIVE_TO_TIME', 'PARTNER', 'ORDER_KEY',
            'STOP_ORDER_KEY', 'TRANS_ID', 'SETTLE_CODE', 'PRICE2', 'REPOTERM', 'REPORATE', 'BLOCK_SECURITIES',
            'REFUNDRATE', 'COMMENT', 'LARGE_TRADE', 'CURR_CODE', 'FOR_ACCOUNT', 'SETTLE_DATE',
            'KILL_IF_LINKED_ORDER_PARTLY_FILLED', 'OFFSET', 'OFFSET_UNITS', 'SPREAD', 'SPREAD_UNITS',
            'BASE_ORDER_KEY', 'USE_BASE_ORDER_BALANCE', 'ACTIVATE_IF_BASE_ORDER_PARTLY_FILLED', 'BASE_CONTRACT', 'MODE',
            'FIRST_ORDER_NUMBER', 'FIRST_ORDER_NEW_QUANTITY', 'FIRST_ORDER_NEW_PRICE', 'SECOND_ORDER_NUMBER',
            'SECOND_ORDER_NEW_QUANTITY', 'SECOND_ORDER_NEW_PRICE', 'KILL_ACTIVE_ORDERS', 'NEG_TRADE_OPERATION',
            'NEG_TRADE_NUMBER', 'VOLUMEMN', 'VOLUMEPL', 'KFL', 'KGO', 'USE_KGO', 'CHECK_LIMITS', 'MATCHREF',
            'CORRECTION',
        ]
        for attr in attrs:
            instance_attr = getattr(self, attr)
            if instance_attr is not None and instance_attr != '':
                result[attr] = str(instance_attr)

        return result

    class Meta:
        is_complished = False


@dataclass
class TransactionsList(TemplateList):
    type_value = Transaction

    def __post_init__(self):
        self._items = []

    def copy(self):
        new_instance = TransactionsList()
        new_instance._items = self._items
        return new_instance
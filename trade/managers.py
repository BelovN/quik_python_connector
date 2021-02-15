from base import Bar, BarsList, Transaction, TransactionsList
from connector.managers import QDataSourceManager, QTradeManager, QPortfolioManager, Interval
from datetime import datetime
from settings import USER_SETTINGS, ACCOUNTS, FIRM_ID


class BarsManager:
    """Класс обертка для QDataSourceManager. Создает datasource и возвращает BarsList"""
    datasource_manager: QDataSourceManager

    def __init__(self):
        self.datasource_manager = QDataSourceManager()

    async def _get_single_bar(self, datasource_uuid: str, index: int) -> Bar:
        O = float(await self.datasource_manager._O(datasource_uuid=datasource_uuid, candle_index=index))
        H = float(await self.datasource_manager._H(datasource_uuid=datasource_uuid, candle_index=index))
        L = float(await self.datasource_manager._L(datasource_uuid=datasource_uuid, candle_index=index))
        C = float(await self.datasource_manager._C(datasource_uuid=datasource_uuid, candle_index=index))
        T = await self.datasource_manager._T(datasource_uuid=datasource_uuid, candle_index=index)
        dtime = datetime(T.year, T.month, T.day, T.hour, T.min, T.sec)
        V = int(float(await self.datasource_manager._V(datasource_uuid=datasource_uuid, candle_index=index)))

        if O == 0 and H == 0 and L == 0 and C == 0:
            raise ValueError('Candle with params: datasource_uuid=' + datasource_uuid +
                             ' index=' + str(index) + 'does not exist!')

        single_bar = Bar(O, H, L, C, dtime, V)
        return single_bar

    async def get_bars(self, class_code: str, sec_code: str, interval: int, count: int = None) -> BarsList:
        datasource_uuid = await self.datasource_manager._create_data_source(class_code=class_code,
                                                                            sec_code=sec_code,
                                                                            interval=interval)

        size = await self.datasource_manager._size(datasource_uuid=datasource_uuid)
        if count is not None:
            _count = min(size, count)
        else:
            _count = size

        bars = BarsList(ticker=sec_code, period=interval)

        for i in range(_count):
            single_bar = self._get_single_bar(datasource_uuid=datasource_uuid, index=i + 1)
            bars.append(single_bar)

        return bars


class TransactionsManager:
    """Класс обертка для QDataSourceManager. Упрощает работу с заявками"""
    trade_manager: QTradeManager

    def __init__(self, account, class_code, sec_code):
        '''
        CLASSCODE: QJSIM,
        SECCODE: SBER
        '''
        self.trade_manager = QTradeManager()
        self.transactions = TransactionsList()

        self.account = ACCOUNTS[account]
        self.client_code = USER_SETTINGS['CLIENT_CODE']
        self.sec_code = sec_code
        self.class_code = class_code

    def __get_transaction(self):
        transaction = Transaction()

        transaction.ACCOUNT = self.account
        transaction.CLIENT_CODE = self.client_code
        transaction.SECCODE = self.sec_code
        transaction.CLASSCODE = self.class_code

        self.transactions.append(transaction)
        return transaction

    async def send_order(self, _type, price, operation, quantity):
        transaction = self.__get_transaction()
        transaction.TYPE = _type

        if _type == 'M':
            transaction.PRICE = '0'
        else:
            transaction.PRICE = str(price)

        transaction.TRANS_ID = str(len(self.transactions))
        transaction.ACTION = "NEW_ORDER"
        transaction.QUANTITY = str(quantity)
        transaction.OPERATION = operation

        return await self.trade_manager._send_transaction(transaction.to_dict())

    async def send_stoploss_order(self,  price, stop_price, operation, quantity):
        transaction = self.__get_transaction()
        transaction.ACTION = "NEW_STOP_ORDER"
        transaction.PRICE = str(price)
        transaction.EXPIRY_DATE = str("TODAY") # Поправить "GTC"
        transaction.TRANS_ID = str(len(self.transactions))
        transaction.OPERATION = operation
        transaction.STOPPRICE = str(stop_price)
        transaction.QUANTITY = str(quantity)
        transaction.IS_ACTIVE_IN_TIME = 'NO'

        return await self.trade_manager._send_transaction(transaction.to_dict())

    async def send_takeprofit_order(self, take_price, operation, quantity, spread, offset):
        transaction = self.__get_transaction()
        transaction.ACTION = "NEW_STOP_ORDER"
        transaction.EXPIRY_DATE = str("TODAY")
        transaction.TRANS_ID = str(len(self.transactions))
        transaction.OPERATION = str(operation)
        transaction.STOP_ORDER_KIND = "TAKE_PROFIT_STOP_ORDER"
        transaction.STOPPRICE = str(take_price)
        transaction.QUANTITY = quantity
        transaction.IS_ACTIVE_IN_TIME = 'NO'
        transaction.SPREAD = str(spread)
        transaction.SPREAD_UNITS = 'PRICE_UNITS'
        transaction.OFFSET = str(offset)
        transaction.OFFSET_UNITS = 'PRICE_UNITS'

        return await self.trade_manager._send_transaction(transaction.to_dict())

    async def send_stoploss_takeprofit_order(self, price, stop_price, take_price, operation, quantity, spread, offset):
        transaction = self.__get_transaction()
        transaction.ACTION = "NEW_STOP_ORDER"
        transaction.EXPIRY_DATE = str("TODAY")
        transaction.TRANS_ID = str(len(self.transactions))
        transaction.OPERATION = str(operation)
        transaction.STOP_ORDER_KIND = "TAKE_PROFIT_AND_STOP_LIMIT_ORDER"
        transaction.PRICE = str(price)
        transaction.STOPPRICE = str(take_price)
        transaction.STOPPRICE2 = str(stop_price)
        transaction.QUANTITY = quantity
        transaction.IS_ACTIVE_IN_TIME = 'NO'
        transaction.SPREAD = str(spread)
        transaction.SPREAD_UNITS = 'PRICE_UNITS'
        transaction.OFFSET = str(offset)
        transaction.OFFSET_UNITS = 'PRICE_UNITS'

        self.trade_manager._send_transaction(transaction.to_dict())

    async def kill_stop_order(self, order_id):
        transaction = self.__get_transaction()
        transaction.ACTION = "KILL_STOP_ORDER"
        transaction.TRANS_ID = str(len(self.transactions))
        transaction.STOP_ORDER_KEY = str(order_id)

        return await self.trade_manager._send_transaction(transaction.to_dict())

    async def kill_order(self, order_id):
        transaction = self.__get_transaction()
        transaction.ACTION = "KILL_ORDER"
        transaction.TRANS_ID = str(len(self.transactions))
        transaction.ORDER_KEY = str(order_id)

        return await self.trade_manager._send_transaction(transaction.to_dict())


class ProtfolioManager:
    portfolio_manager: QPortfolioManager

    def __init__(self):
        self.portfolio_manager = QPortfolioManager()

        self.client_code = USER_SETTINGS['CLIENT_CODE']

        self.fixed_term = None
        self.stock = None
        self.currency = None

    async def update_stock(self, response=None):
        self.stock = await self.portfolio_manager._get_portfolio_info(firm_id=FIRM_ID['stock'],
                                                                      client_code=self.client_code)
        print(self.stock)

    async def update_currency(self, response=None):
        self.currency = await self.portfolio_manager._get_portfolio_info(firm_id=FIRM_ID['currency'],
                                                                         client_code=self.client_code)
        print(self.currency)

    # Для подвязки на событие OnFuturesClientHolding
    async def update_fixed_term(self, response=None):
        self.fixed_term = response
        print(self.fixed_term)



import asyncio

# mgr = TransactionsManager(account, class_code, sec_code)
#
# mgr.send_stoploss_takeprofit_order(price, stop_price, take_price, operation, quantity, spread, offset)
# # ds = '009031cf-957a-49e5-c9bf-2cdbb5834d03'
#
# async def get_ds():
#     # b = await mgr._create_data_source(class_code="QJSIM", sec_code="SBER", interval=Interval.TICK)
#     await mgr._set_update_callback(datasource_uuid=ds)

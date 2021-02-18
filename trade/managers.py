import asyncio
from .base import Bar, BarsList, Transaction, TransactionsList, Order, OrdersList, StopOrder, StopOrdersList

from connector.managers import QDataSourceManager, QTradeManager, QPortfolioManager
from settings import USER_SETTINGS, ACCOUNTS, FIRM_ID
from connector.events import Dispatcher, EventTypes


class BarsManager:
    """Класс обертка для QDataSourceManager. Создает datasource и возвращает BarsList"""
    datasource_manager: QDataSourceManager

    def __init__(self, class_code: str, sec_code: str, interval: int):
        self.datasource_manager = QDataSourceManager()
        self.class_code = class_code
        self.sec_code = sec_code
        self.interval = interval
        self.bars = BarsList(class_code=class_code, sec_code=sec_code, interval=interval)

    def add_updated_bar(self, response):
        if int(response.index) != self.bars[-1].index:
            bar = Bar.from_quik(response=response)
            self.bars.append(bar)
        else:
            self.bars[-1].update_from_quik(response=response)

    async def subscribe(self):
        datasource_uuid = await self.datasource_manager._create_data_source(
            class_code=self.class_code, sec_code=self.sec_code, interval=self.interval
        )
        
        await self.datasource_manager._set_update_callback(datasource_uuid=datasource_uuid)

        Dispatcher().subscribe(event_type=EventTypes.ON_DATA_SOURCE_UPDATE, callback=self.add_updated_bar)


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
    """Класс для работы с портфолио"""
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

    def update_client_holding(self, response):
        self.client_holding = response

    async def async_update_limit(self, response):
        self.futures_limit = await self.portfolio_manager._get_futures_limit(
            firmid=response.firmid,
            trdaccid=ACCOUNTS['fixed_term'],
            limit_type=0,
            currcode='SUR'
        )

    def update_limit_change(self, response):
        asyncio.ensure_future(self.async_update_limit(response=response))
    
    async def subscribe_futures(self):
        dispatcher = Dispatcher()
        dispatcher.subscribe(event_type=EventTypes.ON_FUTURES_CLIENT_HOLDING, callback=self.update_client_holding)
        dispatcher.subscribe(event_type=EventTypes.ON_FUTURES_LIMIT_CHANGE, callback=self.update_limit_change)


class OrdersManager:
    transactions_manager: TransactionsManager

    def __init__(self, account, sec_code, class_code):
        self.transactions_manager = TransactionsManager(
            account=account, sec_code=sec_code, class_code=class_code
        )
        self.orders = OrdersList()
        self.stop_orders = StopOrdersList()

    def update_orders(self, response):
        order = Order.from_quik(response) # --------TODO
        self.orders.append(order)

    def update_stop_orders(self, response):
        stop_order = StopOrder.from_quik(response) # --------TODO
        self.stop_orders.append(stop_order)

    async def subscribe(self):
        Dispatcher().subscribe(event_type=EventTypes.ON_ORDER, callback=self.update_orders)
        Dispatcher().subscribe(event_type=EventTypes.ON_STOP_ORDER, callback=self.update_stop_orders)

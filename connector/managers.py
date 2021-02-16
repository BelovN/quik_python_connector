import logging
from connector.connection import QConnector, QConnection, TypeConnection
from datetime import datetime

from qlua import rpc
from qlua.rpc import datasource as ds
from .utils import singleton, log_method

logger = logging.getLogger('connector')


# Вынес для удобства
class Interval:
    """Интервалы для получения свечей через _create_data_source"""
    UNDEFINED = ds.CreateDataSource_pb2.UNDEFINED
    TICK = ds.CreateDataSource_pb2.INTERVAL_TICK
    M1 = ds.CreateDataSource_pb2.INTERVAL_M1
    M2 = ds.CreateDataSource_pb2.INTERVAL_M2
    M3 = ds.CreateDataSource_pb2.INTERVAL_M3
    M4 = ds.CreateDataSource_pb2.INTERVAL_M4
    M5 = ds.CreateDataSource_pb2.INTERVAL_M5
    M6 = ds.CreateDataSource_pb2.INTERVAL_M6
    M10 = ds.CreateDataSource_pb2.INTERVAL_M10
    M15 = ds.CreateDataSource_pb2.INTERVAL_M15
    M20 = ds.CreateDataSource_pb2.INTERVAL_M20
    M30 = ds.CreateDataSource_pb2.INTERVAL_M30
    H1 = ds.CreateDataSource_pb2.INTERVAL_H1
    H2 = ds.CreateDataSource_pb2.INTERVAL_H2
    H4 = ds.CreateDataSource_pb2.INTERVAL_H4
    D1 = ds.CreateDataSource_pb2.INTERVAL_D1
    W1 = ds.CreateDataSource_pb2.INTERVAL_W1
    MN1 = ds.CreateDataSource_pb2.INTERVAL_MN1


@singleton
class ManagerConnection:
    """Родитель для менеджеров"""
    connector: QConnector

    def __init__(self, type_connection: TypeConnection = None, connector_: QConnector = None):
        if connector_ is None:
            connection = QConnection(_type=type_connection)
            self.connector = QConnector(connection=connection)
        else:
            self.connector = connector_


class BaseManager:
    def __init__(self):
        self.manager_connection = ManagerConnection(type_connection=TypeConnection.REQ)

    def __repr__(self):
        return ' ,'.join([self.__class__.__name__, str(id(self))])


class QDataSourceManager(BaseManager):
    """Класс для получения свечей из Qiuk через REQ/REP"""

    @log_method(logger)
    async def _create_data_source(self, class_code: str, sec_code: str, interval: int) -> str:

        response = await self.manager_connection.connector.run_on_quik(
            function_type='CREATE_DATA_SOURCE', _function=ds.CreateDataSource_pb2,
            class_code=class_code, sec_code=sec_code, interval=interval)

        if hasattr(response, 'error_desc') and response.error_desc != '':
            raise ValueError(response.error_desc)

        if response.datasource_uuid == '':
            raise ValueError('Empty value datasource_uuid!')

        return response.datasource_uuid

    @log_method(logger)
    async def _O(self, datasource_uuid: str, candle_index: int) -> float:
        response = await self.manager_connection.connector.run_on_quik(
            function_type='DS_O', _function=ds.O_pb2, datasource_uuid=datasource_uuid, candle_index=candle_index)

        return response.value

    @log_method(logger)
    async def _C(self, datasource_uuid: str, candle_index: int) -> float:
        response = await self.manager_connection.connector.run_on_quik(
            function_type='DS_C', _function=ds.C_pb2, datasource_uuid=datasource_uuid, candle_index=candle_index)

        return response.value

    @log_method(logger)
    async def _H(self, datasource_uuid: str, candle_index: int) -> float:
        response = await self.manager_connection.connector.run_on_quik(
            function_type='DS_H', _function=ds.H_pb2, datasource_uuid=datasource_uuid, candle_index=candle_index)

        return response.value

    @log_method(logger)
    async def _L(self, datasource_uuid: str, candle_index: int) -> float:
        response = await self.manager_connection.connector.run_on_quik(
            function_type='DS_L', _function=ds.L_pb2, datasource_uuid=datasource_uuid, candle_index=candle_index)

        return response.value

    @log_method(logger)
    async def _T(self, datasource_uuid: str, candle_index: int) -> datetime:
        response = await self.manager_connection.connector.run_on_quik(
            function_type='DS_T', _function=ds.T_pb2, datasource_uuid=datasource_uuid, candle_index=candle_index)

        return response.time

    @log_method(logger)
    async def _V(self, datasource_uuid: str, candle_index: int) -> int:
        response = await self.manager_connection.connector.run_on_quik(
            function_type='DS_V', _function=ds.V_pb2, datasource_uuid=datasource_uuid, candle_index=candle_index)

        return response.value

    @log_method(logger)
    async def _size(self, datasource_uuid: str) -> int:
        response = await self.manager_connection.connector.run_on_quik(
            function_type='DS_SIZE', _function=ds.Size_pb2, datasource_uuid=datasource_uuid)

        return response.value

    @log_method(logger)
    async def _close(self, datasource_uuid: str) -> int:
        response = await self.manager_connection.connector.run_on_quik(
            function_type='DS_CLOSE', _function=ds.Close_pb2, datasource_uuid=datasource_uuid)
        return response.result

    @log_method(logger)
    async def _set_empty_callback(self, datasource_uuid: str) -> int:
        response = await self.manager_connection.connector.run_on_quik(
            function_type='DS_SET_EMPTY_CALLBACK', _function=ds.SetEmptyCallback_pb2, datasource_uuid=datasource_uuid)
        return response.result

    @log_method(logger)
    async def _set_update_callback(
            self, datasource_uuid: str, f_cb_def: str = '', watching_O: bool = False,
            watching_H: bool = False, watching_L: bool = False, watching_C: bool = False,
            watching_V: bool = False, watching_T: bool = False, watching_Size: bool = False) -> int:

        response = await self.manager_connection.connector.run_on_quik(
            function_type='DS_SET_UPDATE_CALLBACK', _function=ds.SetUpdateCallback_pb2, datasource_uuid=datasource_uuid,
            watching_H=watching_H, watching_L=watching_L, watching_C=watching_C, watching_V=watching_V,
            watching_T=watching_T, watching_O=watching_O, watching_Size=watching_Size, f_cb_def=f_cb_def)

        return response.result

    @log_method(logger)
    async def _get_candles_by_index(self, tag: str, line: int, first_candle: int, count: int):

        response = await self.manager_connection.connector.run_on_quik(
            function_type='GET_CANDLES_BY_INDEX', _function=rpc.getCandlesByIndex_pb2,
            tag=tag, first_candle=first_candle, line=line, count=count)

        return response


class QPortfolioManager(BaseManager):
    """Класс для получения информации по портфелю через REQ/REP"""

    @log_method(logger)
    async def _get_money(self, client_code: str, firmid: str, tag: str, currcode: str):

        response = await self.manager_connection.connector.run_on_quik(
            function_type='GET_MONEY', _function=rpc.getMoney_pb2, client_code=client_code,
            firmid=firmid, tag=tag, currcode=currcode)

        return response.money

    @log_method(logger)
    async def _get_money_ex(self, client_code: str, firmid: str, tag: str, currcode: str, limit_kind: int):

        response = await self.manager_connection.connector.run_on_quik(
            function_type='GET_MONEY_EX', _function=rpc.getMoneyEx_pb2, client_code=client_code,
            firmid=firmid, tag=tag, currcode=currcode, limit_kind=limit_kind)

        return response.money_ex

    @log_method(logger)
    async def _get_portfolio_info(self, firm_id: str, client_code: str):
        response = await self.manager_connection.connector.run_on_quik(
            function_type='GET_PORTFOLIO_INFO', _function=rpc.getPortfolioInfo_pb2,
            firm_id=firm_id, client_code=client_code)

        return response.portfolio_info

    @log_method(logger)
    async def _get_portfolio_info_ex(self, firm_id: str, client_code: str, limit_kind: int):

        response = await self.manager_connection.connector.run_on_quik(
            function_type='GET_PORTFOLIO_INFO_EX', _function=rpc.getPortfolioInfoEx_pb2,
            firm_id=firm_id, client_code=client_code, limit_kind=limit_kind)

        return response.portfolio_info_ex

    @log_method(logger)
    async def _get_futures_limit(self, firmid: str, trdaccid: str, limit_type: int, currcode: str):

        response = await self.manager_connection.connector.run_on_quik(
            function_type='GET_FUTURES_LIMIT', _function=rpc.getFuturesLimit_pb2,
            firmid=firmid, trdaccid=trdaccid, limit_type=limit_type, currcode=currcode)

        return response.futures_limit

    @log_method(logger)
    async def _get_futures_holding(self, firmid: str, trdaccid: str, sec_code: str, _type: int):

        response = await self.manager_connection.connector.run_on_quik(
            function_type='GET_FUTURES_HOLDING', _function=rpc.getFuturesHolding_pb2,
            firmid=firmid, trdaccid=trdaccid, sec_code=sec_code, type=_type)

        return response.futures_holding

    @log_method(logger)
    async def _get_depo(self, firmid: str, client_code: str, sec_code: str, trdaccid: str):

        response = await self.manager_connection.connector.run_on_quik(
            function_type='GET_DEPO', _function=rpc.getDepo_pb2, firmid=firmid,
            client_code=client_code, sec_code=sec_code, trdaccid=trdaccid)

        return response.depo

    @log_method(logger)
    async def _get_depo_ex(self, firmid: str, client_code: str, sec_code: str, trdaccid: str, limit_kind: int):

        response = await self.manager_connection.connector.run_on_quik(
            function_type='GET_DEPO_EX', _function=rpc.getDepoEx_pb2, firmid=firmid,
            client_code=client_code, sec_code=sec_code, trdaccid=trdaccid, limit_kind=limit_kind)

        return response.depo_ex


class QTradeManager(BaseManager):
    """Класс для работы с заявками через REQ/REP"""

    @log_method(logger)
    async def _get_buy_sell_info(self, firm_id: str, client_code: str, class_code: str, sec_code: str, price: str):

        response = await self.manager_connection.connector.run_on_quik(
            function_type='GET_BUY_SELL_INFO', _function=rpc.getBuySellInfo_pb2, firm_id=firm_id,
            client_code=client_code, class_code=class_code, sec_code=sec_code, price=price)

        return response.buy_sell_info

    @log_method(logger)
    async def _get_buy_sell_info_ex(self, firm_id: str, client_code: str, class_code: str, sec_code: str, price: str):

        response = await self.manager_connection.connector.run_on_quik(
            function_type='GET_BUY_SELL_INFO_EX', _function=rpc.getBuySellInfoEx_pb2, firm_id=firm_id,
            client_code=client_code, class_code=class_code, sec_code=sec_code, price=price)

        return response.buy_sell_info_ex

    @log_method(logger)
    async def _calc_buy_sell(
            self, class_code: str, sec_code: str, client_code: str,
            account: str, price: str, is_buy: bool, is_market: bool):

        response = await self.manager_connection.connector.run_on_quik(
            function_type='CALC_BUY_SELL', _function=rpc.CalcBuySell_pb2, class_code=class_code, sec_code=sec_code,
            client_code=client_code, account=account, price=price, is_buy=is_buy, is_market=is_market)

        return response

    @log_method(logger)
    async def _send_transaction(self, transaction: dict):

        response = await self.manager_connection.connector.run_on_quik(
            function_type='SEND_TRANSACTION', _function=rpc.sendTransaction_pb2, transaction=transaction)

        return response.result


class QSecurityManager(BaseManager):
    """Класс для получения информации по активам через REQ/REP"""

    @log_method(logger)
    async def _get_security_info(self, class_code: str, sec_code: str):

        response = await self.manager_connection.connector.run_on_quik(
            function_type='GET_SECURITY_INFO', _function=rpc.getSecurityInfo_pb2,
            class_code=class_code, sec_code=sec_code)

        return response.security_info

    @log_method(logger)
    async def _get_quote_level2(self, class_code: str, sec_code: str):

        response = await self.manager_connection.connector.run_on_quik(
            function_type='GET_QUOTE_LEVEL2', _function=rpc.getQuoteLevel2_pb2,
            class_code=class_code, sec_code=sec_code)

        return response

    @log_method(logger)
    async def _get_param_ex(self, class_code: str, sec_code: str, param_name: str):

        response = await self.manager_connection.connector.run_on_quik(
            function_type='GET_PARAM_EX', _function=rpc.getParamEx_pb2,
            class_code=class_code, sec_code=sec_code, param_name=param_name)

        return response.param_ex

    @log_method(logger)
    async def _get_param_ex2(self, class_code: str, sec_code: str, param_name: str):

        response = await self.manager_connection.connector.run_on_quik(
            function_type='GET_PARAM_EX_2', _function=rpc.getParamEx2_pb2,
            class_code=class_code, sec_code=sec_code, param_name=param_name)

        return response.param_ex

    @log_method(logger)
    async def _subscribe_level_II_quotes(self, class_code: str, sec_code: str):

        response = await self.manager_connection.connector.run_on_quik(
            function_type='SUBSCRIBE_LEVEL_II_QUOTES', _function=rpc.Subscribe_Level_II_Quotes_pb2,
            class_code=class_code, sec_code=sec_code)

        return response

    @log_method(logger)
    async def _unsubscribe_level_II_quotes(self, class_code: str, sec_code: str):

        response = await self.manager_connection.connector.run_on_quik(
            function_type='UNSUBSCRIBE_LEVEL_II_QUOTES', _function=rpc.Unsubscribe_Level_II_Quotes_pb2,
            class_code=class_code, sec_code=sec_code)

        return response

    @log_method(logger)
    async def _is_subscribed_level_II_quotes(self, class_code: str, sec_code: str):

        response = await self.manager_connection.connector.run_on_quik(
            function_type='IS_SUBSCRIBED_LEVEL_II_QUOTES', _function=rpc.IsSubscribed_Level_II_Quotes_pb2,
            class_code=class_code, sec_code=sec_code)

        return response

    @log_method(logger)
    async def _param_request(self, class_code: str, sec_code: str, db_name: str):

        response = await self.manager_connection.connector.run_on_quik(
            function_type='PARAM_REQUEST', _function=rpc.ParamRequest_pb2,
            class_code=class_code, sec_code=sec_code, db_name=db_name)

        return response

    @log_method(logger)
    async def _cancel_param_request(self, class_code: str, sec_code: str, db_name: str):

        response = await self.manager_connection.connector.run_on_quik(
            function_type='CANCEL_PARAM_REQUEST', _function=rpc.CancelParamRequest_pb2,
            class_code=class_code, sec_code=sec_code, db_name=db_name)

        return response

import datetime
import pytest
from base import Bar, BarsList
from managers import (QDataSourceManager, QPortfolioManager, QTradeManager,
                      QSecurityManager, Interval)


# # ----------------- TEST QDataSourceManager -----------------
#
#
# @pytest.fixture(scope='session')
# def datasource_manager():
#     manager = QDataSourceManager()
#
#     return manager
#
#
# @pytest.mark.parametrize('class_code, sec_code, interval', [
#                         # ('QJSIM', 'SBER', Interval.TICK),
#                         ('QJSIM', 'SBER', Interval.M1),
#                         # ('QJSIM', 'MGNT', Interval.M3),
#                         # ('QJSIM', 'ROSN', Interval.H2),
# ])
# def test_create_close_data_source(datasource_manager, class_code, sec_code, interval):
#     uuid = datasource_manager._create_data_source(class_code=class_code,
#                                                   sec_code=sec_code,
#                                                   interval=interval)
#
#     assert uuid is not None
#     assert uuid != ''
#
#     closed = datasource_manager._close(uuid)
#     assert closed
#
#
# @pytest.mark.parametrize('class_code, sec_code, interval', [
#                         # --------------------------------- BE CAREFUL -----------------------------
#                         # ('QJSIM123', 'SBER', Interval.M3), # It does not raise ValueError !@!!
#                         # ('QJSIM', 'SBER123', Interval.M3), # It does not raise ValueError !@!!
#                         ('QJSIM', 'SBER', 777),
# ])
# def test_create_close_data_source_fails(datasource_manager, class_code, sec_code, interval):
#     with pytest.raises(ValueError):
#         uuid = datasource_manager._create_data_source(class_code=class_code,
#                                                       sec_code=sec_code,
#                                                       interval=interval)
#
#
# @pytest.fixture(scope='session')
# def preset_uuid(datasource_manager):
#     uuid = datasource_manager._create_data_source(class_code='QJSIM',
#                                                   sec_code='SBER',
#                                                   interval=Interval.M1)
#
#     yield uuid
#
#     # datasource_manager._close(uuid)
#
#
# def test_size(datasource_manager, preset_uuid):
#     value = datasource_manager._size(datasource_uuid=preset_uuid)
#
#     size = int(value)
#     assert size is not None
#
#
# @pytest.fixture(scope='session')
# def size(datasource_manager, preset_uuid):
#     value = datasource_manager._size(datasource_uuid=preset_uuid)
#     size = int(value)
#     return value
#
#
# @pytest.mark.parametrize('candle_index', [0, 1, 20, 100, 800])
# def test_O(datasource_manager, size, preset_uuid, candle_index):
#     index = min(candle_index, size)
#     value = datasource_manager._O(datasource_uuid=preset_uuid, candle_index=index)
#
#     open = float(value)
#     assert open is not None
#
#
# @pytest.mark.parametrize('candle_index', [0, 1, 20, 100, 800])
# def test_C(datasource_manager, size, preset_uuid, candle_index):
#     index = min(candle_index, size)
#     value = datasource_manager._C(datasource_uuid=preset_uuid, candle_index=index)
#
#     close = float(value)
#     assert close is not None
#
#
# @pytest.mark.parametrize('candle_index', [0, 1, 20, 100, 800])
# def test_H(datasource_manager, size, preset_uuid, candle_index):
#     index = min(candle_index, size)
#     value = datasource_manager._H(datasource_uuid=preset_uuid, candle_index=index)
#
#     high = float(value)
#     assert high is not None
#
#
# @pytest.mark.parametrize('candle_index', [0, 1, 20, 100, 800])
# def test_L(datasource_manager, size, preset_uuid, candle_index):
#     index = min(candle_index, size)
#     value = datasource_manager._L(datasource_uuid=preset_uuid, candle_index=index)
#
#     low = float(value)
#     assert low is not None
#
#
# @pytest.mark.parametrize('candle_index', [0, 1, 20, 100, 800])
# def test_T(datasource_manager, size, preset_uuid, candle_index):
#     index = min(candle_index, size)
#     value = datasource_manager._T(datasource_uuid=preset_uuid, candle_index=index)
#
#     assert int(value.year) is not None
#     assert int(value.month) is not None
#     assert int(value.day) is not None
#     assert int(value.hour) is not None
#     assert int(value.min) is not None
#     assert int(value.sec) is not None
#
#
# @pytest.mark.parametrize('candle_index', [0, 1, 20, 100, 800])
# def test_V(datasource_manager, size, preset_uuid, candle_index):
#     index = min(candle_index, size)
#     value = datasource_manager._V(datasource_uuid=preset_uuid, candle_index=index)
#
#     volume = int(float(value))
#     assert volume is not None
#
#
# @pytest.mark.parametrize('tag, line, first_candle, count', [('SOMEIND', 0, 0, 10)])
# def test_get_candles_by_index(datasource_manager, tag, line, first_candle, count):
#     candles = datasource_manager._get_candles_by_index(tag=tag, line=line,
#                                                        first_candle=first_candle,
#                                                        count=count)
#     assert candles.t
#     assert candles.n
#     assert candles.l
#
#
# # ----------------- END TEST QDataSourceManager -------------
#
# # ----------------- TEST BarsManager -----------------
#
#
# def test_bars_manager_constructor():
#     bars_manager = BarsManager()
#     assert bars_manager.datasource_manager is not None
#     assert isinstance(bars_manager.datasource_manager, QDataSourceManager)
#
#
# @pytest.fixture
# def bars_manager_fixture():
#     return BarsManager()
#
#
# @pytest.mark.parametrize('index', [1, 2, 3])
# def test_get_single_bar(bars_manager_fixture, preset_uuid, index):
#     bar = bars_manager_fixture._get_single_bar(datasource_uuid=preset_uuid,
#                                                index=index)
#
#     assert isinstance(bar, Bar)
#     assert bar.open
#     assert bar.high
#     assert bar.low
#     assert bar.close
#     assert bar.volume
#     assert bar.dtime
#     assert isinstance(bar.dtime, datetime.datetime)
#
#
# @pytest.mark.parametrize('index', [-100, 0, 999999999999999999999])
# def test_get_single_bar_fails(bars_manager_fixture, preset_uuid, index):
#     with pytest.raises(ValueError):
#         bar = bars_manager_fixture._get_single_bar(datasource_uuid=preset_uuid,
#                                                    index=index)
#
#
# @pytest.mark.parametrize('class_code, sec_code, interval, count', [
#                         ('QJSIM', 'SBER', Interval.TICK, 100),
#                         ('QJSIM', 'SBER', Interval.M20, 2),
#                         ('QJSIM', 'ROSN', Interval.H1, None),
#                         ('QJSIM', 'MGNT', Interval.M3, 77777),
# ])
# def test_get_bars(bars_manager_fixture, class_code, sec_code, interval, count):
#     bars = bars_manager_fixture.get_bars(class_code=class_code, sec_code=sec_code, interval=interval, count=count)
#
#     assert isinstance(bars, BarsList)
#     if count is not None:
#         assert len(bars) <= count
#
#     assert bars.ticker == sec_code
#     assert bars.period == interval
#     assert bars._bars is not None
#
#
# @pytest.mark.parametrize('class_code, sec_code, interval, count', [
#                         ('QJSIM', 'ROSN', 777, None),
# ])
# def test_get_bars_fails(bars_manager_fixture, class_code, sec_code, interval, count):
#     with pytest.raises(ValueError):
#         bars = bars_manager_fixture.get_bars(class_code=class_code, sec_code=sec_code, interval=interval, count=count)
#
# # ----------------- END TEST BarsManager -----------------
#
#
# # ----------------- TEST QPortfolioManager -----------------
#
# @pytest.fixture
# def portfolio_manager():
#     return QPortfolioManager()
#
#
# @pytest.mark.parametrize('client_code, firmid, tag, currcode', [
#                         ('10273', 'MB1000100000', 'RTOD', 'SUR'),
#                         # ('10273', 'NC0011100000', 'EQTV', 'SUR'),
# ])
# def test_get_money(portfolio_manager, client_code, firmid, tag, currcode):
#     result = portfolio_manager._get_money(client_code=client_code, firmid=firmid,
#                                           tag=tag, currcode=currcode)
#
#     assert hasattr(result, 'money_open_limit')
#     assert hasattr(result, 'money_limit_locked_nonmarginal_value')
#     assert hasattr(result, 'money_limit_locked')
#     assert hasattr(result, 'money_open_balance')
#     assert hasattr(result, 'money_current_limit')
#     assert hasattr(result, 'money_current_balance')
#     assert hasattr(result, 'money_limit_available')
#
# #
# @pytest.mark.parametrize('client_code, firmid, tag, currcode, limit_kind', [
#                         # ('10273', 'MB1000100000', 'RTOD', 'SUR', 0),
#                         ('10273', 'NC0011100000', 'EQTV', 'SUR', 0),
# ])
# def test_get_money_ex(portfolio_manager, client_code, firmid, tag, currcode, limit_kind):
#     result = portfolio_manager._get_money_ex(client_code=client_code, firmid=firmid,
#                                           tag=tag, currcode=currcode, limit_kind=limit_kind)
#
#     assert hasattr(result, 'currcode')
#     assert result.currcode == currcode
#     assert hasattr(result, 'tag')
#     assert result.tag == tag
#     assert hasattr(result, 'firmid')
#     assert result.firmid == firmid
#     assert hasattr(result, 'client_code')
#     assert result.client_code == client_code
#     assert hasattr(result, 'openbal')
#     assert hasattr(result, 'openlimit')
#     assert hasattr(result, 'currentbal')
#     assert hasattr(result, 'currentlimit')
#     assert hasattr(result, 'locked')
#     assert hasattr(result, 'locked_value_coef')
#     assert hasattr(result, 'locked_margin_value')
#     assert hasattr(result, 'leverage')
#     assert hasattr(result, 'limit_kind')
#
#
# @pytest.mark.parametrize('client_code, firm_id', [
#                         ('10273', 'MB1000100000'),
#                         ('10273', 'NC0011100000'),
# ])
# def test_get_portfolio_info(portfolio_manager, client_code, firm_id):
#     result = portfolio_manager._get_portfolio_info(client_code=client_code, firm_id=firm_id)
#     assert hasattr(result, 'is_leverage')
#     assert hasattr(result, 'in_assets')
#     assert hasattr(result, 'leverage')
#     assert hasattr(result, 'open_limit')
#     assert hasattr(result, 'val_short')
#     assert hasattr(result, 'val_long')
#     assert hasattr(result, 'val_long_margin')
#     assert hasattr(result, 'val_long_asset')
#     assert hasattr(result, 'assets')
#     assert hasattr(result, 'cur_leverage')
#     assert hasattr(result, 'margin')
#     assert hasattr(result, 'lim_all')
#     assert hasattr(result, 'av_lim_all')
#     assert hasattr(result, 'locked_buy')
#     assert hasattr(result, 'locked_buy_margin')
#     assert hasattr(result, 'locked_buy_asset')
#     assert hasattr(result, 'locked_sell')
#     assert hasattr(result, 'locked_value_coef')
#     assert hasattr(result, 'in_all_assets')
#     assert hasattr(result, 'all_assets')
#     assert hasattr(result, 'profit_loss')
#     assert hasattr(result, 'rate_change')
#     assert hasattr(result, 'lim_buy')
#     assert hasattr(result, 'lim_sell')
#     assert hasattr(result, 'lim_non_margin')
#     assert hasattr(result, 'lim_buy_asset')
#     assert hasattr(result, 'val_short_net')
#     assert hasattr(result, 'val_long_net')
#     assert hasattr(result, 'total_money_bal')
#     assert hasattr(result, 'total_locked_money')
#     assert hasattr(result, 'haircuts')
#     assert hasattr(result, 'assets_without_hc')
#     assert hasattr(result, 'status_coef')
#     assert hasattr(result, 'varmargin')
#     assert hasattr(result, 'go_for_positions')
#     assert hasattr(result, 'go_for_orders')
#     assert hasattr(result, 'rate_futures')
#     assert hasattr(result, 'is_qual_client')
#     assert hasattr(result, 'is_futures')
#     assert hasattr(result, 'curr_tag')
#
#
# @pytest.mark.parametrize('client_code, firm_id, limit_kind', [
#                         ('10273', 'MB1000100000', 0),
# ])
# def test_get_portfolio_info_ex(portfolio_manager, client_code, firm_id, limit_kind):
#     result = portfolio_manager._get_portfolio_info_ex(firm_id=firm_id, client_code=client_code, limit_kind=limit_kind)
#
#     assert hasattr(result, 'init_margin')
#     assert hasattr(result, 'min_margin')
#     assert hasattr(result, 'corrected_margin')
#     assert hasattr(result, 'client_type')
#     assert hasattr(result, 'portfolio_value')
#     assert hasattr(result, 'start_limit_open_pos')
#     assert hasattr(result, 'total_limit_open_pos')
#     assert hasattr(result, 'limit_open_pos')
#     assert hasattr(result, 'used_lim_open_pos')
#     assert hasattr(result, 'acc_var_margin')
#     assert hasattr(result, 'cl_var_margin')
#     assert hasattr(result, 'opt_liquid_cost')
#     assert hasattr(result, 'fut_asset')
#     assert hasattr(result, 'fut_total_asset')
#     assert hasattr(result, 'fut_debt')
#     assert hasattr(result, 'fut_rate_asset')
#     assert hasattr(result, 'fut_rate_asset_open')
#     assert hasattr(result, 'fut_rate_go')
#     assert hasattr(result, 'planed_rate_go')
#     assert hasattr(result, 'cash_leverage')
#     assert hasattr(result, 'fut_position_type')
#     assert hasattr(result, 'fut_accured_int')
#     assert hasattr(result, 'portfolio_info')
#
#
# @pytest.mark.parametrize('client_code, firmid, sec_code, trdaccid', [
#                         ('10273', 'MB1000100000', 'GAZP', 'EQTV'),
# ])
# def test_get_depo(portfolio_manager, client_code, firmid, sec_code, trdaccid):
#     result = portfolio_manager._get_depo(client_code=client_code, firmid=firmid, sec_code=sec_code, trdaccid=trdaccid)
#
#     assert hasattr(result, 'depo_limit_locked_buy_value')
#     assert hasattr(result, 'depo_current_balance')
#     assert hasattr(result, 'depo_limit_locked_buy')
#     assert hasattr(result, 'depo_limit_locked')
#     assert hasattr(result, 'depo_limit_available')
#     assert hasattr(result, 'depo_current_limit')
#     assert hasattr(result, 'depo_open_balance')
#     assert hasattr(result, 'depo_open_limit')
#
#
# @pytest.mark.parametrize('firmid, client_code, sec_code, trdaccid, limit_kind', [
#                         ('MB1000100000', '10273', 'GAZP', 'EQTV', 0),
# ])
# def test_get_depo_ex(portfolio_manager, firmid, client_code, sec_code, trdaccid, limit_kind):
#     result = portfolio_manager._get_depo_ex(client_code=client_code, firmid=firmid, sec_code=sec_code,
#                                             trdaccid=trdaccid, limit_kind=limit_kind)
#
#     assert hasattr(result, 'sec_code')
#     assert hasattr(result, 'trdaccid')
#     assert hasattr(result, 'firmid')
#     assert hasattr(result, 'client_code')
#     assert hasattr(result, 'openbal')
#     assert hasattr(result, 'openlimit')
#     assert hasattr(result, 'currentbal')
#     assert hasattr(result, 'currentlimit')
#     assert hasattr(result, 'locked_sell')
#     assert hasattr(result, 'locked_buy')
#     assert hasattr(result, 'locked_buy_value')
#     assert hasattr(result, 'locked_sell_value')
#     assert hasattr(result, 'wa_position_price')
#     assert hasattr(result, 'limit_kind')
#
#
# # ----------------- END TEST QPortfolioManager -------------
#
#
# # ----------------- TEST QTradeManager -----------------
#
@pytest.fixture
def trade_manager():
    manager = QTradeManager()
    return manager


#
#
# @pytest.mark.parametrize('firm_id, client_code, class_code, sec_code, price', [
#                         ('MB1000100000', '10273', 'QJSIM', 'SBER', '0')
# ])
# def test_get_buy_sell_info(trade_manager, firm_id, client_code, class_code, sec_code, price):
#     result = trade_manager._get_buy_sell_info(firm_id=firm_id, client_code=client_code,
#                                               class_code=class_code, sec_code=sec_code, price=price)
#     assert hasattr(result, 'is_margin_sec')
#     assert hasattr(result, 'is_asset_sec')
#     assert hasattr(result, 'balance')
#     assert hasattr(result, 'can_buy')
#     assert hasattr(result, 'can_sell')
#     assert hasattr(result, 'position_valuation')
#     assert hasattr(result, 'value')
#     assert hasattr(result, 'open_value')
#     assert hasattr(result, 'lim_long')
#     assert hasattr(result, 'long_coef')
#     assert hasattr(result, 'lim_short')
#     assert hasattr(result, 'short_coef')
#     assert hasattr(result, 'value_coef')
#     assert hasattr(result, 'open_value_coef')
#     assert hasattr(result, 'share')
#     assert hasattr(result, 'short_wa_price')
#     assert hasattr(result, 'long_wa_price')
#     assert hasattr(result, 'profit_loss')
#     assert hasattr(result, 'spread_hc')
#     assert hasattr(result, 'can_buy_own')
#     assert hasattr(result, 'can_sell_own')
#
#
# @pytest.mark.parametrize('firm_id, client_code, class_code, sec_code, price', [
#                         ('MB1000100000', '10273', 'QJSIM', 'SBER', '0'),
# ])
# def test_get_buy_sell_info_ex(trade_manager, firm_id, client_code, class_code, sec_code, price):
#     result = trade_manager._get_buy_sell_info_ex(firm_id=firm_id, client_code=client_code, class_code=class_code,
#                                                  sec_code=sec_code, price=price)
#
#     assert hasattr(result, 'buy_sell_info')
#     assert hasattr(result, 'limit_kind')
#     assert hasattr(result, 'd_long')
#     assert hasattr(result, 'd_min_long')
#     assert hasattr(result, 'd_short')
#     assert hasattr(result, 'd_min_short')
#     assert hasattr(result, 'client_type')
#     assert hasattr(result, 'is_long_allowed')
#     assert hasattr(result, 'is_short_allowed')
#
#
# @pytest.mark.parametrize('class_code, sec_code, client_code, account, price, is_buy, is_market', [
#                         ('QJSIM', 'SBER', '10273', 'NL0011100043', '0', True, False),
# ])
# def test_calc_buy_sell(trade_manager, class_code, sec_code, client_code, account, price, is_buy, is_market):
#
#     result = trade_manager._calc_buy_sell(class_code=class_code, sec_code=sec_code, client_code=client_code,
#                                           account=account, price=price, is_buy=is_buy, is_market=is_market)
#
#     assert hasattr(result, 'qty')
#     assert hasattr(result, 'comission')
#
#

def test_send_transaction(trade_manager):
    transaction = {
        'ACCOUNT': 'NL0011100043',
        'CLIENT_CODE': '10273',
        'TYPE': 'M',
        'TRANS_ID': '7',
        'CLASSCODE': 'QJSIM',
        'SECCODE': 'SBER',
        'ACTION': 'NEW_ORDER',
        'OPERATION': 'B',
        'PRICE': '0',
        'QUANTITY': '10',
    }
    trade_manager._send_transaction(transaction=transaction)


# ----------------- END TEST QTradeManager -------------


# ----------------- TEST QSecurityManager -----------------
#
# @pytest.fixture
# def security_manager():
#     manager = QSecurityManager()
#     return manager
#
#
# @pytest.mark.parametrize('firmid, trdaccid, limit_type, currcode', [
#                         ('MB1000100000', 'EQTV', 0, 'SUR'),
#                         ('MB1000100000', 'EQTV', 0, ''),
# ])
# def test_get_futures_limit(security_manager, firmid, trdaccid, limit_type, currcode):
#     result = security_manager._get_futures_limit(firmid=firmid, trdaccid=trdaccid,
#                                                  limit_type=limit_type, currcode=currcode)
#     assert hasattr(result, 'firmid')
#     assert hasattr(result, 'trdaccid')
#     assert hasattr(result, 'limit_type')
#     assert hasattr(result, 'liquidity_coef')
#     assert hasattr(result, 'cbp_prev_limit')
#     assert hasattr(result, 'cbplimit')
#     assert hasattr(result, 'cbplused')
#     assert hasattr(result, 'cbplplanned')
#     assert hasattr(result, 'varmargin')
#     assert hasattr(result, 'accruedint')
#     assert hasattr(result, 'cbplused_for_orders')
#     assert hasattr(result, 'cbplused_for_positions')
#     assert hasattr(result, 'ts_comission')
#     assert hasattr(result, 'kgo')
#     assert hasattr(result, 'currcode')
#     assert hasattr(result, 'real_varmargin')
#
#
# @pytest.mark.parametrize('firmid, trdaccid, sec_code, _type', [
#                         ('MB1000100000', 'EQTV', 'SBER', 0),
#                         ('MB1000100000', 'EQTV', 'SBER', 1),
# ])
# def test_get_futures_holding(security_manager, firmid, trdaccid, sec_code, _type):
#     result = security_manager._get_futures_holding(firmid=firmid, trdaccid=trdaccid, sec_code=sec_code, _type=_type)
#
#     assert hasattr(result, 'firmid')
#     assert hasattr(result, 'trdaccid')
#     assert hasattr(result, 'sec_code')
#     assert hasattr(result, 'type')
#     assert hasattr(result, 'startbuy')
#     assert hasattr(result, 'startsell')
#     assert hasattr(result, 'startnet')
#     assert hasattr(result, 'todaybuy')
#     assert hasattr(result, 'todaysell')
#     assert hasattr(result, 'totalnet')
#     assert hasattr(result, 'openbuys')
#     assert hasattr(result, 'opensells')
#     assert hasattr(result, 'cbplplanned')
#     assert hasattr(result, 'varmargin')
#     assert hasattr(result, 'avrposnprice')
#     assert hasattr(result, 'positionvalue')
#     assert hasattr(result, 'real_varmargin')
#     assert hasattr(result, 'total_varmargin')
#     assert hasattr(result, 'session_status')
#
#
# @pytest.mark.parametrize('class_code, sec_code', [
#                         ('QJSIM', 'SBER'),
#                         ('QJSIM', 'MGNT'),
# ])
# def test_get_security_info(security_manager, class_code, sec_code):
#     result = security_manager._get_security_info(class_code=class_code, sec_code=sec_code)
#
#     assert hasattr(result, 'code')
#     assert hasattr(result, 'name')
#     assert hasattr(result, 'short_name')
#     assert hasattr(result, 'class_code')
#     assert hasattr(result, 'class_name')
#     assert hasattr(result, 'face_value')
#     assert hasattr(result, 'face_unit')
#     assert hasattr(result, 'scale')
#     assert hasattr(result, 'mat_date')
#     assert hasattr(result, 'lot_size')
#     assert hasattr(result, 'isin_code')
#     assert hasattr(result, 'min_price_step')
#
#
# @pytest.mark.parametrize('class_code, sec_code', [
#                         ('QJSIM', 'SBER'),
#                         ('QJSIM', 'MGNT'),
# ])
# def test_get_quote_level2(security_manager, class_code, sec_code):
#     result = security_manager._get_quote_level2(class_code=class_code, sec_code=sec_code)
#
#     assert hasattr(result, 'bid_count')
#     assert hasattr(result, 'offer_count')
#     assert hasattr(result, 'bids')
#     assert hasattr(result, 'offers')
#
#
# @pytest.mark.parametrize('class_code, sec_code, param_name', [
#                         ('SPBFUT', 'SiH9', 'BUYDEPO'),
#                         ('SPBFUT', 'SiH9', 'SELLDEPO'),
# ])
# def test_get_param_ex(security_manager, class_code, sec_code, param_name):
#     result = security_manager._get_param_ex(class_code=class_code,
#                                             sec_code=sec_code,
#                                             param_name=param_name)
#
#     assert hasattr(result, 'param_type')
#     assert hasattr(result, 'param_value')
#     assert hasattr(result, 'param_image')
#     assert hasattr(result, 'result')
#
#
# @pytest.mark.parametrize('class_code, sec_code, param_name', [
#                         ('SPBFUT', 'SiH9', 'BUYDEPO'),
#                         ('SPBFUT', 'SiH9', 'SELLDEPO'),
# ])
# def test_get_param_ex2(security_manager, class_code, sec_code, param_name):
#     result = security_manager._get_param_ex2(class_code=class_code,
#                                              sec_code=sec_code,
#                                              param_name=param_name)
#     assert hasattr(result, 'param_type')
#     assert hasattr(result, 'param_value')
#     assert hasattr(result, 'param_image')
#     assert hasattr(result, 'result')
#
#
# @pytest.mark.parametrize('class_code, sec_code', [
#                         ('SPBFUT', 'SiH9'),
#                         ('QJSIM', 'SBER'),
#                         ('QJSIM', 'MGNT'),
# ])
# def test_subscribe_level_II_quotes(security_manager, class_code, sec_code):
#     result = security_manager._subscribe_level_II_quotes(class_code=class_code, sec_code=sec_code)
#
#     assert hasattr(result, 'result')
#
#
# @pytest.mark.parametrize('class_code, sec_code', [
#                         ('SPBFUT', 'SiH9'),
#                         ('QJSIM', 'SBER'),
#                         ('QJSIM', 'MGNT'),
# ])
# def test_unsubscribe_level_II_quotes(security_manager, class_code, sec_code):
#     result = security_manager._unsubscribe_level_II_quotes(class_code=class_code, sec_code=sec_code)
#
#     assert hasattr(result, 'result')
#
#
# @pytest.mark.parametrize('class_code, sec_code', [
#                         ('SPBFUT', 'SiH9'),
#                         ('QJSIM', 'SBER'),
#                         ('QJSIM', 'MGNT'),
# ])
# def test_is_subscribed_level_II_quotes(security_manager, class_code, sec_code):
#     result = security_manager._is_subscribed_level_II_quotes(class_code=class_code, sec_code=sec_code)
#
#     assert hasattr(result, 'result')
#
#
# @pytest.mark.parametrize('class_code, sec_code, db_name', [
#                         ('SPBFUT', 'SiZ8', 'BUYDEPO'),
#                         ('SPBFUT', 'SiZ8', 'SELLDEPO'),
# ])
# def test_param_request(security_manager, class_code, sec_code, db_name):
#     result = security_manager._param_request(class_code=class_code, sec_code=sec_code, db_name=db_name)
#
#     assert hasattr(result, 'result')
#
#
# @pytest.mark.parametrize('class_code, sec_code, db_name', [
#                         ('SPBFUT', 'SiZ8', 'BUYDEPO'),
#                         ('SPBFUT', 'SiZ8', 'SELLDEPO'),
# ])
# def test_cancel_param_request(security_manager, class_code, sec_code, db_name):
#     result = security_manager._cancel_param_request(class_code=class_code, sec_code=sec_code, db_name=db_name)
#
#     assert hasattr(result, 'result')


# ----------------- END TEST QSecurityManager -------------


# ----------------- TEST QDataSourceManager -----------------


# ----------------- END TEST QDataSourceManager -------------

import pytest
import dataclasses
import random
from datetime import datetime
from base import Bar, BarsList, Transaction


# ----------------- TEST BARS -----------------

def test_empty_arguments():
    with pytest.raises(TypeError):
        b = Bar()


@pytest.mark.parametrize('volume', [1, 5000, 800000])
@pytest.mark.parametrize("open, high, low, close, dtime", [(7, 321321123, 2.1123213, 10, datetime.now())])
def test_bar_constructor(open, high, low, close, dtime, volume):
    b = Bar(open=open,
            high=high,
            low=low,
            close=close,
            dtime=dtime,
            volume=volume)

    assert open == b.open
    assert high == b.high
    assert low == b.low
    assert close == b.close
    assert dtime == b.dtime
    assert volume == b.volume


@pytest.mark.parametrize('volume', [0, -100])
@pytest.mark.parametrize('dtime', [datetime.now()])
@pytest.mark.parametrize("open, high, low, close", [(10, 7, 2, 3),
                                                    (10, 20, 30, 10),
                                                    (7, 321123323, 2.11232, 10)
                                                   ])
def test_bar_constructor_fails(open, high, low, close, dtime, volume):
    with pytest.raises(ValueError):
        b = Bar(open=open,
               high=high,
               low=low,
               close=close,
               dtime=dtime,
               volume=volume)


def test_bar_change():
    with pytest.raises(dataclasses.FrozenInstanceError):
        b = Bar(open=5, high=7, low=2, close=3,
                dtime=datetime.now(), volume=10)
        b.open = 10

# ----------------- END TEST BARS -----------------

# ----------------- TEST BARS LIST ----------------

def test_bars_list_constructor():
    with pytest.raises(TypeError):
        bars = BarsList()


@pytest.mark.parametrize('ticker', ['123', 'SBER'])
@pytest.mark.parametrize("period", [1, 10, 60])
def test_bars_list_constructor(ticker, period):
    bars = BarsList(ticker=ticker, period=period)
    assert ticker == bars.ticker
    assert period == bars.period


@pytest.mark.parametrize('ticker', ['SBER'])
@pytest.mark.parametrize("period", [-1, 0])
def test_bars_list_constructor_fails(ticker, period):
    with pytest.raises(ValueError):
        bars = BarsList(ticker=ticker, period=period)


@pytest.fixture
def preset_bars():
    ticker = 'ticker'
    period = 10
    bars = []
    for i in range(random.randint(100, 1000)):
        O = random.randint(500, 1000)
        C = random.randint(500, 1000)
        H = random.randint(1000, 1500)
        L = random.randint(10, 500)
        V = random.randint(10, 100)
        bars.append(
            Bar(O, H, L, C, datetime.now(), V),
        )
    return ticker, period, bars


def test_append_bars_list(preset_bars):
    ticker, period, _bars = preset_bars
    bars = BarsList(ticker=ticker, period=period)
    for b in _bars:
        bars.append(b)

    for i, b in enumerate(bars):
        assert _bars[i] == b


def test_len_bars_list(preset_bars):
    ticker, period, _bars = preset_bars
    bars = BarsList(ticker=ticker, period=period)
    _length = 0
    for b in _bars:
        bars.append(b)
        _length += 1

    assert len(bars) == _length


def test_insert_bars_list(preset_bars):
    ticker, period, _bars = preset_bars
    index = random.randint(5, len(_bars)-5)
    bars = BarsList(ticker=ticker, period=period, _bars=_bars[:index])

    for i in range(index + 1, len(_bars)):
        rand_index = random.randint(0, len(bars))
        bars.insert(rand_index, _bars[i])
        assert bars[rand_index] == _bars[i]


@pytest.mark.parametrize('value', [123, '', {}, (123,)])
def test_insert_bars_list_fails(preset_bars, value):
    ticker, period, _bars = preset_bars
    bars = BarsList(ticker=ticker, period=period)
    rand_index = random.randint(0, len(bars))

    with pytest.raises(ValueError):
        bars.insert(rand_index, value)


def test_setitem_bars_list(preset_bars):
    ticker, period, _bars = preset_bars
    index = random.randint(5, len(_bars)-5)
    bars = BarsList(ticker=ticker, period=period, _bars=_bars[:index])

    for i in range(index + 1, len(_bars)):
        index = random.randint(0, len(bars)-1)
        bars[index] = _bars[i]
        assert bars[index] == _bars[i]


@pytest.mark.parametrize('value', [123, '', {}, (123,)])
def test_setitem_bars_list_fails(preset_bars, value):
    ticker, period, _bars = preset_bars
    bars = BarsList(ticker=ticker, period=period, _bars=preset_bars)
    index = random.randint(0, len(bars)-1)

    with pytest.raises(ValueError):
        bars[index] = value


def test_delitem_bars_list(preset_bars):
    ticker, period, _bars = preset_bars
    bars = BarsList(ticker=ticker, period=period, _bars=_bars)

    for i in range(int(len(bars)/2)):
        index = random.randint(0, len(bars)-1)
        b = bars[index]
        bars.remove(b)
        assert b not in bars


# ----------------- END TEST BARS LIST ---------------


# ----------------- TEST TRANSACTION -----------------


@pytest.mark.parametrize('CLASSCODE',   ['GAZP', 'SBER'])
@pytest.mark.parametrize('SECCODE',     ['ASDF', 'ASDF'])
@pytest.mark.parametrize('CLIENT_CODE', ['XXX', 'YYY'])
@pytest.mark.parametrize('TYPE',        ['M', 'L'])
@pytest.mark.parametrize('ACTION',      ['NEW_ORDER', 'KILL_ORDER'])
@pytest.mark.parametrize('OPERATION',   ['S', 'B'])
@pytest.mark.parametrize('QUANTITY',    ['1', '20'])
@pytest.mark.parametrize('PRICE',       ['0', '123'])
def test_transaction_constructor(CLASSCODE, CLIENT_CODE, TYPE, ACTION,
                                 OPERATION, QUANTITY, PRICE, SECCODE):
    transaction = Transaction(CLASSCODE=CLASSCODE, CLIENT_CODE=CLIENT_CODE, TYPE=TYPE, SECCODE=SECCODE,
                              ACTION=ACTION, OPERATION=OPERATION, QUANTITY=QUANTITY, PRICE=PRICE)


def test_transaction_constructor_fails():
    with pytest.raises(TypeError):
        transaction = Transaction()


@pytest.mark.parametrize("CLASSCODE, SECCODE, CLIENT_CODE, TYPE, ACTION, OPERATION, QUANTITY, PRICE",
                         [
                             ('', 'ASDF', 'XXX', 'M', 'NEW_ORDER', 'S', '20', '0'),
                             ('GAZP', None, 'XXX', 'M', 'NEW_ORDER', 'S', '20', '0'),
                             ('GAZP', 'ASDF', 123, 'M', 'NEW_ORDER', 'S', '20', '0'),
                             ('GAZP', 'ASDF', 'XXX', [], 'NEW_ORDER', 'S', '20', '0'),
                             ('GAZP', 'ASDF', 'XXX', 'M', {}, 'S', '20', '0'),
                             ('GAZP', 'ASDF', 'XXX', 'M', 'NEW_ORDER', None, '20', '0'),
                             ('GAZP', 'ASDF', 'XXX', 'M', 'NEW_ORDER', 'S', '', '0'),
                             ('GAZP', 'ASDF', 'XXX', 'M', 'NEW_ORDER', 'S', '20', None),
                         ])
def test_transaction__check_errors_fails(CLASSCODE, CLIENT_CODE, TYPE, ACTION,
                                         OPERATION, QUANTITY, PRICE, SECCODE):
    with pytest.raises(ValueError):
        transaction = Transaction(CLASSCODE=CLASSCODE, CLIENT_CODE=CLIENT_CODE,
                                  TYPE=TYPE, SECCODE=SECCODE, ACTION=ACTION,
                                  OPERATION=OPERATION, QUANTITY=QUANTITY, PRICE=PRICE)

# ----------------- END TEST TRANSACTION -------------

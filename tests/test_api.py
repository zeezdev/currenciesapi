import pytest


@pytest.mark.parametrize('first', ('BTC', 'USD', 'ETH', 'XMR', 'WAVES', 'ZEC', 'XRP', 'DASH', 'ETC', 'BCH', 'LTC'))
@pytest.mark.parametrize('second', ('BTC', 'USD', 'ETH', 'XMR', 'WAVES', 'ZEC', 'XRP', 'DASH', 'ETC', 'BCH', 'LTC'))
def test_current_rate(client, first, second):
    """Test of request the current rate"""
    ticker = '%s/%s' % (first, second)
    response = client.get('/api/rates?ticker=%s' % ticker)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert 'rate' in response.json
    assert 'ticker' in response.json
    assert response.json['ticker'] == ticker


def test_current_rate_missed_ticker(client):
    """Ticker is mandatory argument"""
    response = client.get('/api/rates')
    assert response.status_code == 400


@pytest.mark.parametrize('tikcer', ('btc/usd', 'BTC', 'BTC/', '', '1'))
def test_current_rate_invalid_ticker(client, tikcer):
    """Ticker must have following format (<FIRST>/<SECOND>)"""
    response = client.get('/api/rates?ticker=%s' % tikcer)
    assert response.status_code == 400


@pytest.mark.parametrize('first', (
        'BTC', 'USD', 'ETH', 'XMR', 'WAVES', 'ZEC', 'XRP', 'DASH', 'ETC', 'BCH', 'LTC'))
@pytest.mark.parametrize('second', (
        'BTC', 'USD', 'ETH', 'XMR', 'WAVES', 'ZEC', 'XRP', 'DASH', 'ETC', 'BCH', 'LTC'))
@pytest.mark.parametrize('ts', (
        '2018-01-01 00:00:00', '2018-12-31 23:59:59', '2018-07-04 02:00:00'))
def test_historical_rate(client, first, second, ts):
    """Test of request the historical rate"""
    ticker = '%s/%s' % (first, second)
    response = client.get('/api/rates?ticker=%s&ts=%s' % (ticker, ts))
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert 'rate' in response.json
    assert 'ticker' in response.json
    assert 'ts' in response.json
    assert response.json['ticker'] == ticker


@pytest.mark.parametrize('ts', (
        '2018-01-01 00:00',
        '2018-12-31', '2018-07', '', '2018', 'just text'))
def test_historical_invalid_ts(client, ts):
    """Ts argument must have following date & time format: YYYY-MM-DD hh:mm:ss"""
    response = client.get('/api/rates?ticker=BTC/USD&ts=%s' % ts)
    assert response.status_code == 400


@pytest.mark.parametrize('ts', ('2017-12-31 23:49:59', '2019-01-01 00:10:00'))
def test_historical_ts_out_of_range(client, ts):
    """We know that DB contains data for 2018 year only"""
    response = client.get('/api/rates?ticker=BTC/USD&ts=%s' % ts)
    assert response.status_code == 400

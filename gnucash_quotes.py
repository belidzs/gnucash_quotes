from piecash import *
from alpha_vantage.foreignexchange import ForeignExchange
from alpha_vantage.timeseries import TimeSeries
from os import environ
import dateutil.parser
from decimal import *
from time import time, sleep

ALPHAVANTAGE_API_KEY = environ['ALPHAVANTAGE_API_KEY']
API_MAX_CALLS_PER_INTERVAL = 5
API_MAX_CALLS_INTERVAL = 60
NAMESPACE_CURRENCY = {
    'Amsterdam': 'EUR',
    'NASDAQ': 'USD',
    'London': 'GBP'
}
NAMESPACE_SKIP = {
    'template',
    'ÁK'
}

forex = ForeignExchange(key=ALPHAVANTAGE_API_KEY)
stockexchange = TimeSeries(key=ALPHAVANTAGE_API_KEY)

start = time()
call_counter = 0


def add_price(commodity, currency, date, value):
    try:
        price = book.get(Price, commodity=commodity, currency=currency, date=date)
        print('Az árfolyam már létezik: {0}'.format(price))
    except ValueError:
        price = Price(commodity=commodity, currency=currency, date=date, value=value)
        print('Új árfolyam: {0}'.format(price))


with open_book(uri_conn='postgresql://postgres@localhost/gnucash', readonly=False, do_backup=False) as book:  # type: Book
    for commodity in book.commodities:  # type: Commodity
        if commodity != book.default_currency and commodity.namespace not in NAMESPACE_SKIP:
            print('Letöltés: {0}'.format(commodity.mnemonic))
            if call_counter >= API_MAX_CALLS_PER_INTERVAL and time() - start < API_MAX_CALLS_INTERVAL:
                print('Alvás {0} másodpercig'.format(int(API_MAX_CALLS_INTERVAL - (time() - start))))
                sleep(API_MAX_CALLS_INTERVAL - (time() - start))
                call_counter = 0
                start = time()
            mnemonic = commodity.mnemonic
            if commodity.namespace == 'CURRENCY':
                factor = Decimal(1.0)
                if commodity.mnemonic == 'XXX':
                    mnemonic = 'BTC'
                    factor = Decimal(0.001)
                price_av, meta = forex.get_currency_exchange_rate(mnemonic, book.default_currency.mnemonic)
                price_date = dateutil.parser.parse(timestr=price_av['6. Last Refreshed']).date()
                price_value = round(Decimal(price_av['5. Exchange Rate']) * factor, 8)
                add_price(commodity, book.default_currency, price_date, price_value)
            else:
                price_av, meta = stockexchange.get_daily(commodity.mnemonic)
                price_date = dateutil.parser.parse(meta['3. Last Refreshed']).date()
                price_value = Decimal(price_av[meta['3. Last Refreshed']]['4. close'])
                price_currency = book.get(Commodity, mnemonic=NAMESPACE_CURRENCY[commodity.namespace])
                add_price(commodity, price_currency, price_date, price_value)
            call_counter = call_counter + 1
    book.save()

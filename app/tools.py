
DTFORMAT = '%Y-%m-%d %H:%M:%S'

class ParseError(Exception):
    pass


class Ticker(object):

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __str__(self):
        return '%s/%s' % (self.first, self.second)

    @classmethod
    def from_string(cls, ticker, supported_currencies=None):
        ticker = ticker.split('/')
        if len(ticker) != 2:
            raise ParseError('ticker must contain two currencies (for example BTC/USD)')

        # get existing currencies
        if supported_currencies is not None:
            unsupported = set(ticker) - set(supported_currencies)
            if unsupported:
                raise ParseError('Unsupported currency! (%s)' % ', '.join(unsupported))

        return cls(*ticker)

    def to_list(self):
        return [self.first, self.second]

    @property
    def is_same(self):
        return self.first == self.second


from copy import deepcopy
from datetime import datetime

from flask import jsonify, request
from flask_restplus import Resource

from app import api, app
from app.models import Currency, Rate, RateHistory
from app.tools import Ticker, ParseError, DTFORMAT


# FOR FUN

@app.route('/')
def index():
    return 'Hello!'


@api.route('/currencies/')
class ApiCurrencies(Resource):

    def get(self):
        result = Currency.objects().to_json()
        return app.response_class(
            response=result,
            mimetype='application/json'
        )


@api.route('/currencies/<code>')
class ApiCurrenciesDetail(Resource):

    @api.response(200, 'Success')
    @api.response(404, 'Currency not found')
    def get(self, code):
        result = Currency.objects.get(code=code).to_json()
        return app.response_class(
            response=result,
            mimetype='application/json'
        )

# API

parser = api.parser()
parser.add_argument('ticker', type=str, help='Interested ticker, for example: BTC/USD', required=True)
parser.add_argument('ts', type=datetime, help='Timestamp (YYYY-MM-DD hh:mm:ss) to get a historical value in the particular date and time')

@api.route('/rates')
class ApiRates(Resource):

    @api.doc(description='Get value of currencies.')
    @api.expect(parser)
    @api.response(200, 'Success')
    @api.response(400, 'Bad request. Argument "ticker" was not specified or has invalid format. Argument "ts" has an invalid format or out of range')
    def get(self):
        args = deepcopy(request.args)

        ticker = args.get('ticker')
        if ticker is None:
            return 'ticker argument required', 400

        currencies = Currency.objects.distinct('code')  # TODO: implement method
        try:
            ticker = Ticker.from_string(ticker, currencies)
        except ParseError as ex:
            return str(ex), 400

        ts = None
        if 'ts' in args:
            try:
                ts = datetime.strptime(args['ts'], DTFORMAT)
            except ValueError:
                return 'Invalid timestamp format. Expected YYYY-MM-DD hh:mm:ss', 400

        if ts:
            rates = list(RateHistory.find(ts, ticker))
            if len(rates) != 2:
                if len(rates) == 1:
                    if ticker.is_same or 'USD' in ticker.to_list():
                        pass  # OK  (BTC/USD)
                    else:
                        return 'Timestamp out of range', 400
                elif len(rates) == 0:
                    if ticker.is_same and ticker.first == 'USD':
                        pass  # OK  (USD/USD)
                    else:
                        return 'Timestamp out of range', 400
                else:
                    return 'Unknown error', 500
        else:
            rates = list(Rate.find(ticker))

        if 'USD' in ticker.to_list():
            rates.append({'currency': 'USD', 'value': 1.0})
        rates = {r['currency']: r['value'] for r in rates}

        response = {
            'ticker': str(ticker),
            'rate': round(rates[ticker.first] / rates[ticker.second], 8),
        }
        if ts:
            response['ts'] = ts

        return jsonify(response)

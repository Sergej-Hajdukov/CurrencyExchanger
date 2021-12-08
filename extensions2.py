import requests
import json
from config import currency


class APIException(Exception):
    pass


class CurrencyExchanger:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        # if quote == base:
        #     raise APIException('Заданы одинаковые валюты')

        try:
            base_ticker = currency[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту ({base})')

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту ({quote})')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не корректно указано количество валюты ({amount})')

        r = requests.get(
            f'https://free.currconv.com/api/v7/convert?q={base_ticker}_{quote_ticker}&compact=ultra&apiKey=f385bdfa0e1d16ea058d')
        total_base = json.loads(r.content)['_'.join([base_ticker, quote_ticker])]

        return total_base
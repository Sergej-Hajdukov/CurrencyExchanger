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
            raise APIException(f'Не удалось обработать валюту ({base})\nСмотреть список доступных валют /values')

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту ({quote})\nСмотреть список доступных валют /values')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не корректно указано количество валюты ({amount})')

        if base_ticker == 'EUR':
            r = requests.get(
                f'http://api.exchangeratesapi.io/v1/latest?access_key=fb92c97cd81323ff76daec60c968eb94&base={base_ticker}&symbols={quote_ticker}&format=1')
            total_base = json.loads(r.content)["rates"][quote_ticker]
        elif quote_ticker == 'EUR':
            r = requests.get(
                f'http://api.exchangeratesapi.io/v1/latest?access_key=fb92c97cd81323ff76daec60c968eb94&base={quote_ticker}&symbols={base_ticker}&format=1')
            total_base = str(1 / float(json.loads(r.content)["rates"][base_ticker]))
        elif base_ticker != 'EUR' and quote_ticker != 'EUR':
            r1 = requests.get(
                f'http://api.exchangeratesapi.io/v1/latest?access_key=fb92c97cd81323ff76daec60c968eb94&base=EUR&symbols={base_ticker}&format=1')
            r2 = requests.get(
                f'http://api.exchangeratesapi.io/v1/latest?access_key=fb92c97cd81323ff76daec60c968eb94&base=EUR&symbols={quote_ticker}&format=1')
            total_base = str(float(json.loads(r2.content)["rates"][quote_ticker]) / float(json.loads(r1.content)["rates"][base_ticker]))

        return total_base

import requests
import json
from datetime import datetime

from src.utils import read_excel

api_key = 'MV7UDI58N2N2F6MF'
json_file_path = 'C:/Users/79200/PycharmProjects/Курсовая/user_settings.json'

present_time = datetime.now().time()
end_date = datetime.now().date()

transaction_list = read_excel()

# Приветствие
def welcome():
    """Функция ПРИВЕТСТВИЕ, где приветствие выбирается в зависимости от
    текущего времени."""
    present_hour = present_time.hour
    if 5 <= present_hour < 12:
        return 'Доброе утро'
    elif 12 <= present_hour < 18:
        return 'Добрый день'
    elif 18 <= present_hour:
        return 'Добрый вечер'
    else:
        return 'Доброй ночи'


# По каждой карте
def get_card_info(transaction_list):
    """ Функция принимает на вход список транзакций и возвращает информацию
по каждой карте: последние 4 цифры карты, общая сумма расходов, кешбэк (1 рубль на каждые 100 рублей)."""
    card_info = {}
    for transaction in transaction_list:
        card_number = transaction.get('card_number')
        # Если карта уже есть в card_info, то обновляем информацию по ней
        if card_number in card_info:
            # Добавляем сумму транзакции к общей сумме потраченного по крате
            card_info[card_number]['total_spent'] += transaction.get('amount', 0)
        # Если карты нет в словаре, добавляем новую запись
        else:
            card_info[card_number] = {
                'lost_digits': card_number[-4:],
                'total_spent': transaction.get('amount', 0),
                'cashback': ''
            }
        card_info[card_number]['cashback'] = (transaction.get('amount', 0) // 100) * 1
        card_list = list(card_info.values())
    return card_list


# Топ-5 транзакций по сумме платежа
def top_five(transaction_list):
    """ Функция возвращает топ 5 транзакций """
    sorted_list = sorted(transaction_list, key = lambda x: abs(x['amount']), reverse = True)
    # Получаем из отсортированного списка 5 первых значений
    top_5 = sorted_list[:5]
    # Выводим информацию о каждой из топ-5 транзакций
    for transaction in top_5:
        date = transaction.get('date', 'Дата не указана')
        amount = transaction.get('amount', 'Сумма не указана')
        category = transaction.get('category', 'Категория не указана')
        description = transaction.get('description', 'Описание не указано')
        print(f"Дата: {date}, Сумма: {amount}, Категория: {category}, Описание: {description}")
    return top_5


# Курс валют
def value_course():
    """" Функция читает список валют из JSON файла и возвращает данные об их курсах"""
    # Адрес API для получения данных от ЦБ РФ
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    # Отправляем GET-запрос к API и получаем ответ в формате JSON
    response = requests.get(url)
    data = response.json()
    # Чтение валют из JSON файла
    with open(json_file_path, 'r') as file:
        currency_data = json.load(file)
        currencies = currency_data.get("user_currencies", [])
    currency_rates = []
    for currency in currencies:
        if currency in data['Valute']:
            # Получаем курс
            rate = data['Valute'][currency]['Value']
            currency_rates.append({'currency': currency, 'rate': rate})
    return currency_rates



# Стоимость акций из S&P 500
def get_stock_prices():
    """ Функция возвращает информацию по акциям: название и цену"""
    # Чтение акций из JSON файла
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        stocks = data.get("user_stocks", [])

    stock_prices = []

    # URL для запроса к API
    url = "https://www.alphavantage.co/query"

    for stock in stocks:
        # Параметры для запроса
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': stock,
            'interval': '1min',
            'apikey': api_key }

        # Отправка запроса к API
        response = requests.get(url, params=params)
        data = response.json()

        # Получение последней цены акции
        try:
            last_refreshed = data['Meta Data']['3. Last Refreshed']
            last_price = data['Time Series (1min)'][last_refreshed]['1. open']
            stock_prices.append({'stock': stock, 'price': last_price})
        except KeyError:
            print(f"Не удалось получить данные для {stock}")
    return stock_prices


def filter_transactions(transaction_list, end_date):
    """Фильтрует транзакции с начала месяца до указанной даты"""
    start_date = end_date.replace(day=1)
    filtered_transactions = [
        transaction for transaction in transaction_list
        if start_date <= transaction['date'] <= end_date
    ]
    return filtered_transactions


def main_page():
    """Основная функция, объединяющая все функции и выводящая результаты"""
    # Фильтрация транзакций
    filtered_transactions = filter_transactions(transaction_list, end_date)

    # Приветствие
    greeting = welcome()
    print(greeting)

    # Информация по каждой карте
    card_info = get_card_info(filtered_transactions)
    print("Информация по картам:")
    for card in card_info:
        print(f"Последние 4 цифры: {card['lost_digits']}, Общая сумма расходов: {card['total_spent']}, Кешбэк: {card['cashback']}")

    # Топ-5 транзакций
    top_transactions = top_five(filtered_transactions)
    print("\nТоп-5 транзакций:")
    for transaction in top_transactions:
        print(transaction)

    # Курсы валют
    currency_rates = value_course()
    print("\nКурсы валют:")
    for rate in currency_rates:
        print(f"Валюта: {rate['currency']}, Курс: {rate['rate']}")

    # Стоимость акций из S&P 500
    stock_prices = get_stock_prices()
    print("\nСтоимость акций из S&P 500:")
    for stock in stock_prices:
        print(f"Акция: {stock['stock']}, Цена: {stock['price']}")

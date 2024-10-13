import json

from src.utils import read_excel


transaction_list = read_excel()


# Простой поиск
def easy_search(search_string):
    """ Функция принимает на вход строку для поиска, возвращается JSON-ответ
со всеми транзакциями, содержащими запрос в описании или категории."""
    # Приводим строку поиска к нижнему регистру для нечувствительности к регистру
    search_string_lower = search_string.lower()
    # Фильтруем транзакции, которые содержат строку поиска в описании или категории
    matching_transactions = [
        transaction for transaction in transaction_list
        if search_string_lower in transaction.get('description', '').lower() or
           search_string_lower in transaction.get('category', '').lower()
    ]

    # Возвращаем список подходящих транзакций в формате JSON
    return json.dumps(matching_transactions, ensure_ascii=False, indent=4)

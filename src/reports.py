from turtle import pd
from typing import Optional


import pandas as pd
import logging
from datetime import datetime, timedelta
from functools import wraps
import json

from src.views import transaction_list

# Создаем DataFrame
df = pd.DataFrame(transaction_list)
df['date'] = pd.to_datetime(df['date'])

# Настройка логирования
logging.basicConfig(level=logging.INFO)

def save_report_to_file(filename=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Выполняем функцию и получаем результат
            result = func(*args, **kwargs)
            # Определяем имя файла
            report_filename = filename if filename else f"отчет_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            # Записываем результат в файл
            with open(report_filename, 'w', encoding='utf-8') as file:
                json.dump(result, file, ensure_ascii=False, indent=4)
            logging.info(f"Отчет сохранен в {report_filename}")
            return result
        return wrapper
    return decorator


def spending_by_category(df: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
       Функция возвращает траты по заданной категории за последние три месяца от переданной даты.
       """
    # Используем текущую дату, если дата не передана
    if date is None:
        date = datetime.now()
    else:
        date = pd.to_datetime(date)

    # Определяем дату три месяца назад
    three_months_ago = date - timedelta(days=90)

    # Фильтруем транзакции по категории и дате
    filtered_transactions = df[
   (df['category'] == category) &
   (df['date'] >= three_months_ago) &
   (df['date'] <= date)
    ]

    # Суммируем траты по категории
    total_expenses = filtered_transactions['amount'].sum()

    # Формируем отчет
    report = {
    "category": category,
    "date": date.strftime('%Y-%m-%d'),
    "total_expenses": total_expenses

}

    return report

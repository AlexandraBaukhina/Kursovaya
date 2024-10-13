import pandas as pd
import pytest

from src.reports import spending_by_category

# Пример данных транзакций
mock_transactions = [
    {'date': '2023-01-15', 'category': 'Food', 'amount': 150.0},
    {'date': '2023-02-10', 'category': 'Food', 'amount': 200.0},
    {'date': '2023-03-05', 'category': 'Transport', 'amount': 50.0},
    {'date': '2023-03-20', 'category': 'Food', 'amount': 100.0},
    {'date': '2023-04-01', 'category': 'Food', 'amount': 250.0},
]

# Создаем DataFrame
df = pd.DataFrame(mock_transactions)
df['date'] = pd.to_datetime(df['date'])


def test_spending_by_category():
    # Устанавливаем тестовую дату
    test_date = '2023-04-01'
    # Ожидаемый результат для категории 'Food'
    expected_report = {
        "category": "Food",
        "date": "2023-04-01",
        "total_expenses": 550.0}  # Сумма за последние три месяца: 200.0 + 100.0 + 250.0 }

    # Вызов функции
    report = spending_by_category(df, 'Food', test_date)

    # Проверка результата
    assert report == expected_report


def test_spending_by_category_no_expenses():
    # Устанавливаем тестовую дату
    test_date = '2023-01-01'
    # Ожидаемый результат для категории 'Food' без расходов
    expected_report = {
        "category": "Food",
        "date": "2023-01-01",
        "total_expenses": 0.0}  # Нет расходов за последние три месяца }

    # Вызов функции
    report = spending_by_category(df, 'Food', test_date)

    # Проверка результата
    assert report == expected_report

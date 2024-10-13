from datetime import datetime
from unittest.mock import patch
import pytest
from src.views import (welcome, get_card_info, top_five)

@pytest.mark.parametrize("mock_hour, expected_greeting", [
    (9, 'Доброе утро'),
    (14, 'Добрый день'),
    (19, 'Добрый вечер'),
    (3, 'Доброй ночи'),
])
def test_welcome(mock_hour, expected_greeting):
    with patch('your_module_name.present_time', new=datetime(2023, 10, 25, mock_hour, 0)):
        assert welcome() == expected_greeting


def test_get_card_info():
    transactions = [
        {"card_number": "1234567890123456", "amount": 150},
        {"card_number": "1234567890123456", "amount": 200},
        {"card_number": "9876543210987654", "amount": 300}
    ]
    expected_result = [
        {"lost_digits": "3456", "total_spent": 350, "cashback": 3},
        {"lost_digits": "7654", "total_spent": 300, "cashback": 3}
    ]
    assert get_card_info(transactions) == expected_result


def test_top_five():
    transactions = [
        {"amount": 150, "date": "2023-08-01", "category": "Food", "description": "Lunch"},
        {"amount": 500, "date": "2023-09-15", "category": "Transport", "description": "Taxi ride"},
        {"amount": 300, "date": "2023-10-10", "category": "Electronics", "description": "New phone"},
        {"amount": 400, "date": "2023-10-25", "category": "Food", "description": "Dinner"},
        {"amount": 50, "date": "2023-08-05", "category": "Misc", "description": "Coffee"},
        {"amount": 600, "date": "2023-09-20", "category": "Health", "description": "Doctor"}
    ]
    expected_result = [
        {"amount": 600, "date": "2023-09-20", "category": "Health", "description": "Doctor"},
        {"amount": 500, "date": "2023-09-15", "category": "Transport", "description": "Taxi ride"},
        {"amount": 400, "date": "2023-10-25", "category": "Food", "description": "Dinner"},
        {"amount": 300, "date": "2023-10-10", "category": "Electronics", "description": "New phone"},
        {"amount": 150, "date": "2023-08-01", "category": "Food", "description": "Lunch"}
    ]
    assert top_five(transactions) == expected_result


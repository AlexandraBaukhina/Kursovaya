import json
import pytest
from unittest.mock import patch

# Импортируем функцию для тестирования
from src.services import easy_search


# Пример данных транзакций
mock_transactions = [
    {'description': 'Grocery shopping', 'category': 'Food'},
    {'description': 'Monthly subscription', 'category': 'Entertainment'},
    {'description': 'Gas station', 'category': 'Transport'},
    {'description': 'Restaurant dinner', 'category': 'Food'},
]

# Тестируем функцию easy_search
@patch('your_module.read_excel', return_value=mock_transactions)
def test_easy_search(mock_read_excel):
    # Тестируем поиск по описанию
    result = easy_search('grocery')
    expected_result = json.dumps([{'description': 'Grocery shopping', 'category': 'Food'}], ensure_ascii=False, indent=4)
    assert result == expected_result

    # Тестируем поиск по категории
    result = easy_search('food')
    expected_result = json.dumps([
        {'description': 'Grocery shopping', 'category': 'Food'},
        {'description': 'Restaurant dinner', 'category': 'Food'}
    ], ensure_ascii=False, indent=4)
    assert result == expected_result

    # Тестируем поиск с нечувствительностью к регистру
    result = easy_search('GAS')
    expected_result = json.dumps([{'description': 'Gas station', 'category': 'Transport'}], ensure_ascii=False, indent=4)
    assert result == expected_result

    # Тестируем случай, когда нет совпадений
    result = easy_search('nonexistent')
    expected_result = json.dumps([], ensure_ascii=False, indent=4)
    assert result == expected_result

# Запуск тестов с помощью pytest
if __name__ == '__main__':
    pytest.main()

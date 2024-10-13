from src.reports import spending_by_category
from src.services import easy_search
from src.views import main_page


def main():
    while True:
        print("\nВыберите действие:")
        print("1. Главная страница")
        print("2. Поиск транзакций")
        print("3. Траты по категории")
        print("4. Выход")
        choice = input("Введите номер действия: ")

        if choice == '1':
            main_page()
        elif choice == '2':
            search_string = input("Введите строку для поиска: ")
            results = easy_search(search_string)
            print("Результаты поиска:")
            print(results)
        elif choice == '3':
            category = input("Введите категорию: ")
            date = input("Введите дату (YYYY-MM-DD) или оставьте пустым для текущей даты: ")
            if not date:
                date = None
            report = spending_by_category(category, date)
            print("Отчет по тратам:")
            print(report)
        elif choice == '4':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == '__main__':
    main()
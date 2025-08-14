from src.api_classes import HeadHunterAPI
from src.savers import JSONSaver
from src.vacancy import Vacancy


def user_interaction():
    """
    Функция для взаимодействия с пользователем через консоль.
    """
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()

    search_query = input("Введите поисковый запрос для поиска вакансий на hh.ru: ")

    # Получение вакансий с API
    hh_vacancies_json = hh_api.get_vacancies(search_query)
    if not hh_vacancies_json:
        print("Не удалось получить вакансии. Попробуйте позже или измените запрос.")
        return

    # Преобразование в объекты Vacancy
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies_json)

    # Сохранение вакансий
    json_saver.add_vacancies(vacancies_list)
    print(f"Найдено и сохранено {len(vacancies_list)} вакансий.")

    while True:
        print("\nВыберите действие:")
        print("1 - Показать топ N вакансий по зарплате")
        print("2 - Показать вакансии с ключевым словом в описании")
        print("3 - Выход")

        choice = input("Ваш выбор: ")

        if choice == "1":
            try:
                top_n = int(input("Введите количество вакансий для вывода: "))
                sorted_vacancies = sorted(vacancies_list, reverse=True)
                for i, vacancy in enumerate(sorted_vacancies[:top_n]):
                    print(f"\n--- Вакансия #{i + 1} ---")
                    print(vacancy)
            except ValueError:
                print("Некорректный ввод. Введите число.")

        elif choice == "2":
            keyword = input("Введите ключевое слово для фильтрации: ")
            filtered_vacancies = json_saver.get_vacancies_by_criteria(keyword)
            if not filtered_vacancies:
                print("Вакансии с таким ключевым словом не найдены.")
            else:
                print(f"\n--- Найдено {len(filtered_vacancies)} вакансий с ключевым словом '{keyword}' ---")
                for vacancy in filtered_vacancies:
                    print(vacancy)

        elif choice == "3":
            print("Завершение работы.")
            break

        else:
            print("Некорректный выбор. Попробуйте снова.")

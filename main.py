import psycopg2
from src.api_classes import HeadHunterAPI
from src.config import config
from src.db_manager import DBManager
from src.db_create import create_database, create_tables


def save_data_to_database(params, employers_data, vacancies_data):
    """Сохраняет данные о компаниях и вакансиях в базу данных."""
    conn = psycopg2.connect(**params)
    with conn.cursor() as cur:
        for employer in employers_data:
            cur.execute("""
                INSERT INTO companies (employer_id, name, url)
                VALUES (%s, %s, %s)
                ON CONFLICT (employer_id) DO NOTHING;
            """, (employer['id'], employer['name'], employer.get('alternate_url')))

        for vacancy in vacancies_data:
            salary_from = vacancy.get('salary', {}).get('from') if vacancy.get('salary') else None
            salary_to = vacancy.get('salary', {}).get('to') if vacancy.get('salary') else None

            # Пропускаем вакансии без ID, чтобы избежать ошибок
            if 'id' in vacancy:
                cur.execute("""
                    INSERT INTO vacancies (vacancy_id, name, salary_from, salary_to, url, employer_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (vacancy_id) DO NOTHING;
                """, (vacancy['id'], vacancy['name'], salary_from, salary_to, vacancy['alternate_url'],
                      vacancy['employer']['id']))
    conn.commit()
    conn.close()


def main():
    # Список ID интересных компаний
    employer_ids = [
        '1740',  # Яндекс
        '3529',  # Сбер
        '78638',  # VK
        '15478',  # Ozon
        '2180',  # Tinkoff
        '84585',  # Avito
        '3776',  # MTC
        '4181',  # Альфа-Банк
        '64174',  # 2ГИС
        '1122462',  # Skyeng
    ]

    db_name = "hh_vacancies"
    params = config()

    # Создание БД и таблиц
    create_database(db_name, params)
    create_tables(params)

    # Получение данных с API
    hh_api = HeadHunterAPI()
    employers_data = hh_api.get_employers(employer_ids)

    all_vacancies_data = []
    for employer_id in employer_ids:
        all_vacancies_data.extend(hh_api.get_vacancies_by_employer(employer_id))

    # Сохранение данных в БД
    save_data_to_database(params, employers_data, all_vacancies_data)

    # Работа с пользователем через DBManager
    db_manager = DBManager(params)

    while True:
        print("\nВыберите действие:")
        print("1 - Показать список всех компаний и количество вакансий")
        print("2 - Показать список всех вакансий")
        print("3 - Показать среднюю зарплату по вакансиям")
        print("4 - Показать вакансии с зарплатой выше средней")
        print("5 - Найти вакансии по ключевому слову")
        print("0 - Выход")

        choice = input("Ваш выбор: ")
        if choice == '1':
            companies = db_manager.get_companies_and_vacancies_count()
            for company in companies:
                print(f"Компания: {company[0]}, Вакансий: {company[1]}")
        elif choice == '2':
            vacancies = db_manager.get_all_vacancies()
            for vac in vacancies:
                print(f"Компания: {vac[0]}, Вакансия: {vac[1]}, ЗП от: {vac[2]}, Ссылка: {vac[3]}")
        elif choice == '3':
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата: {avg_salary:.2f}" if avg_salary else "Нет данных о зарплате")
        elif choice == '4':
            vacancies = db_manager.get_vacancies_with_higher_salary()
            for vac in vacancies:
                print(f"Вакансия: {vac[0]}, ЗП от: {vac[1]}, Ссылка: {vac[2]}")
        elif choice == '5':
            keyword = input("Введите ключевое слово для поиска: ")
            vacancies = db_manager.get_vacancies_with_keyword(keyword)
            for vac in vacancies:
                print(f"Вакансия: {vac[0]}, ЗП от: {vac[1]}, Ссылка: {vac[2]}")
        elif choice == '0':
            break
        else:
            print("Неверный выбор, попробуйте снова.")

    db_manager.close_connection()


if __name__ == '__main__':
    main()

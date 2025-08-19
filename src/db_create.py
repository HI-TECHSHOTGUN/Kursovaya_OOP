import psycopg2
from src.config import config


def create_database(db_name: str, params: dict) -> None:
    """Создает новую базу данных."""
    params_for_creation = params.copy()
    params_for_creation.pop('database', None)

    conn = psycopg2.connect(dbname='postgres', **params_for_creation)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")

    cur.close()
    conn.close()
    print(f"База данных '{db_name}' успешно создана или пересоздана.")


def create_tables(params: dict) -> None:
    """Создает таблицы 'companies' и 'vacancies' в базе данных."""
    db_name = params['database']
    conn = psycopg2.connect(**params)

    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE companies (
                    employer_id INT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    url VARCHAR(255)
                );
            """)
            cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id INT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    salary_from INT,
                    salary_to INT,
                    url VARCHAR(255),
                    employer_id INT REFERENCES companies(employer_id) NOT NULL
                );
            """)
    finally:
        conn.commit()
        conn.close()

    print(f"Таблицы 'companies' и 'vacancies' созданы в '{db_name}'.")


if __name__ == '__main__':
    params = config()
    db_name = params['database']

    create_database(db_name, params)
    create_tables(params)